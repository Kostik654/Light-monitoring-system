import socket
import time
from asyncio import sleep

from job_module import Job
from logger import LogItOut
from common_methods import toFixed, generate_tag, generate_branch, generate_cseq, generate_call_id


class SipJob(Job):
    def __init__(self,
                 ipv4_address_: str,
                 port_: int,
                 sname_: str,
                 stype_: str,
                 awtime: int,
                 interval_t: int,
                 exp_codes: list[int] = None,
                 default_chat_id_: int = 0,
                 tg_tag_: str = "*"):

        super().__init__(name_=sname_,
                         type_=stype_,
                         interval_time=interval_t,
                         awtime=awtime,
                         exp_codes=exp_codes,
                         chat_id_=default_chat_id_,
                         tg_tag_=tg_tag_)

        self.remote_ipv4_address = ipv4_address_
        self.remote_port = port_

    def get_status_code(self, resp_str: str) -> int:
        first_line: str = resp_str.split("\r\n")[0]
        code: int = int(first_line.split(" ")[1])
        return code

    def send_sip_options(self,
                         to_server,
                         from_contact_sip_server="XXX",
                         sip_port=5060,
                         from_user="sip:8001@localhost",
                         to_user="sip:check@localhost") -> (bool, str, int):
        sip_request = (
            f"OPTIONS {to_user} SIP/2.0\r\n"
            f"Via: SIP/2.0/UDP {from_contact_sip_server}:{sip_port};rport;branch={generate_branch()}\r\n"
            f"Max-Forwards: 70\r\n"
            f"From: <{from_user}>;tag={generate_tag()}\r\n"
            f"To: <{to_user}>\r\n"
            f"Contact: <sip:8001@{from_contact_sip_server}:{sip_port}>\r\n"
            f"Call-ID: {generate_call_id()}\r\n"
            f"CSeq: {generate_cseq()} OPTIONS\r\n"
            f"User-Agent: FPBX-14.0.17(16.30.0)\r\n"
            f"Content-Length: 0\r\n\r\n"
        )

        is_success: bool = False
        out_message: str = ""
        current_error_type: int = -1
        serv_inf: str = f"SIP: {self.remote_ipv4_address}:{self.remote_port}"

        # Создаем UDP сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.await_time)

        try:

            self.last_request_time = time.perf_counter()
            # Отправляем запрос на SIP-сервер
            sock.sendto(sip_request.encode(), (to_server, sip_port))

            # Ждем ответа от сервера
            response, _ = sock.recvfrom(1024)
            response = response.decode()

            self.update_resp_time()

            self.last_status_code = self.get_status_code(response)

            # Проверяем код ответа
            if self.last_status_code in self.expected_codes:
                is_success = True
                out_message = f"✅ OK\tSIP\t{self.response_time}s\t{serv_inf}\t\t\t\tCODE: {self.last_status_code}\t[{self.job_name}]"
                current_error_type = -1
            else:
                is_success = False
                out_message = (f"❌ PROBLEM: {serv_inf}\t[{self.job_name}]\n"
                               f"Code [{self.last_status_code}] is not in expected codes: {self.expected_codes}\n"
                               f"Server response:\n{response}\n")
                current_error_type = 0
        except socket.timeout:
            self.update_resp_time()
            is_success = False
            out_message = f"❌ TIMEOUT error (> {self.await_time} sec): {serv_inf}\t[{self.job_name}]"
            current_error_type = 1
        except Exception as e:
            self.update_resp_time()
            is_success = False
            current_error_type = 2
            out_message = f"❌ SIP checking error occurred in job [{self.job_name}]: {e}"
        finally:
            sock.close()
            return is_success, out_message, current_error_type

    async def start_job(self):

        self.running = True

        while self.running:

            from_cont_server = "XXX"
            is_success, mess, curr_err_t = self.send_sip_options(from_contact_sip_server=from_cont_server,
                                                                 to_server=self.remote_ipv4_address,
                                                                 sip_port=self.remote_port)

            self.problems_counter(is_success)

            if not self.tg_tag.__eq__("*") and not is_success:
                mess += f"\n{self.tg_tag}"

            LogItOut(message_=mess,
                     for_tg=self.is_for_tg(curr_err_t),
                     add_timestamp=True,
                     chat_lvl_=self.default_chat_id)

            await sleep(self.req_interval_time)
