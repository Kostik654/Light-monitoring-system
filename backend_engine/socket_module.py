import socket
import subprocess
from asyncio import sleep

from job_module import Job
from logger import LogItOut
from common_methods import GetPortsArray
from port_item import PortItem


class SocketJob(Job):


    def __init__(self,
                 ipv4_address_: str,
                 ports_names: str,
                 sname_: str,
                 stype_: str,
                 awtime: int = 5,
                 interval_t: int = 60,
                 default_chat_id_: int = 0
                 ):

        super().__init__(name_=sname_,
                         type_=stype_,
                         interval_time=interval_t,
                         awtime=awtime,
                         chat_id_=default_chat_id_)

        self.remote_ipv4_address = ipv4_address_

        # array or *
        self.remote_ports: list[PortItem] = GetPortsArray(ports_names)

        LogItOut(message_=f'socket ports array added: {self.remote_ports}',
                 for_tg=False,
                 add_timestamp=False)


    def check_host_availability(self, host: str, attempts: int = 5) -> (str, bool):

        success: bool = False
        mess: str = ''

        for i in range(attempts):
            try:
                output = subprocess.check_output(
                    ["ping", "-c", "1", "-W", str(self.await_time), self.remote_ipv4_address],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                mess = '✅ OK'
                success = True
                break
            except subprocess.CalledProcessError:
                mess = "❌ PROBLEM: All the packets were lost"
            except subprocess.TimeoutExpired:
                mess = f"❌ TIMEOUT: > {self.await_time}sec"
            except Exception as e:
                mess = f"❌ EXCEPTION: {e}"

        return mess, success


    def check_port(self, port_: PortItem) -> (str, bool, int):

        message_: str = ""
        is_passed: bool = False
        error_type: int = 0 # no error

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.await_time)

        try:
            result = sock.connect_ex((self.remote_ipv4_address, port_.Port))

            if port_.ExceptedCodes is None:
                if result == 0:
                    is_passed = True
                    message_ += f"✅ Port {port_.Port} [{port_.ServiceName}]: OPENED"
                else:
                    error_type = 1
                    message_ += f"⚠️ Port {port_.Port} [{port_.ServiceName}]: CLOSED [{result}: {Job.socket_error_descriptions[result]}]"
            else:
                if result == 0:
                    if not (result in port_.ExceptedCodes):
                        is_passed = False
                        error_type = 2
                        message_ += f"⚠️ Port {port_.Port} [{port_.ServiceName}]: OPENED [NOT EXPECTED]"
                    else:
                        is_passed = True
                        message_ += f"✅ Port {port_.Port} [{port_.ServiceName}]: OPENED"
                else:
                    if not (result in port_.ExceptedCodes):
                        is_passed = False
                        error_type = 3
                        message_ += f"❌ Port {port_.Port} [{port_.ServiceName}]: CLOSED [{result} - NOT EXPECTED]"
                    else:
                        is_passed = True
                        message_ += f"✅ Port {port_.Port} [{port_.ServiceName}]: CLOSED  [{result} - EXPECTED]"

        except Exception as e:
            error_type = 4
            message_ += f"❌ Port {port_.Port} [{port_.ServiceName}] revision ERROR: {e}"
        finally:
            sock.close()
            return message_, is_passed, error_type


    def start_testing(self) -> (str, bool):

        message_: str = f"Host {self.remote_ipv4_address} ports revision [{self.job_name}]\n"
        is_passed: bool = False
        errors: int = 0

        # check Host Ports
        if self.remote_ports is not None:
            for port_ in self.remote_ports:
                #print(f'Port {port_} revision started')
                mess, is_psd, err_t = self.check_port(port_)
                message_ += f"{mess}\n"
                if not is_psd:
                    errors += 1
        else:
        # check only Host (icmp)
            mess, is_psd = self.check_host_availability(self.remote_ipv4_address)
            message_ = (f"Host {self.remote_ipv4_address} [{self.job_name}] revision\n"
                        f"{mess}")
            if not is_psd:
                errors += 1

        if errors == 0:
            is_passed = True

        return message_, is_passed


    async def start_job(self):

        self.running = True

        while self.running:

            message_, is_success = self.start_testing()

            if is_success:
                is_for_tg = self.last_failed

                self.last_failed = False
                LogItOut(message_=message_,
                         for_tg=is_for_tg,
                         add_timestamp=not is_for_tg,
                         chat_lvl_=self.default_chat_id)
            else:

                prev_failed = self.last_failed

                self.problems_counter()  # self.last_failed = True

                LogItOut(message_=message_,
                         for_tg=not prev_failed,
                         add_timestamp=prev_failed,
                         chat_lvl_=self.default_chat_id)

            await sleep(self.req_interval_time)
