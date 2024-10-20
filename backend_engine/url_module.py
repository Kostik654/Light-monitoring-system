import asyncio
from asyncio import sleep

import aiohttp
import time
from job_module import Job
from logger import LogItOut
from common_methods import toFixed


class UrlJob(Job):

    def __init__(self,
                 url: str,
                 ssl_verify: bool,
                 sname_: str,
                 stype_: str,
                 awtime: int,
                 interval_t: int,
                 exp_answer_: str = None,
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

        self.url = url
        self.ssl_verification = ssl_verify
        self.expected_answer = exp_answer_

    #  IN DEVELOPMENT
    def scan_html_body(self, body: str) -> bool:
        try:
            if self.expected_answer in body:
                return True
            else:
                return False
        except Exception as e:
            print(f'Expected answer var is null?: [{self.expected_answer}]')
            return False

    async def send_burl(self) -> (str, bool, int):

        self.last_request_time = time.perf_counter()
        message_: str = '[empty message]'
        err_type: int = -1  # no error
        is_passed: bool = False

        timeout = aiohttp.ClientTimeout(
            total=self.await_time  # Total time for whole operations (in sec)
            #  connect=10,
            #  sock_connect=5,
            #  sock_read=30
        )

        try:

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.url, ssl=self.ssl_verification) as response:

                    self.update_resp_time()

                    self.last_status_code = response.status

                    if self.expected_codes is not None and self.last_status_code not in self.expected_codes and self.last_status_code != 200:
                        err_type = 0
                        message_ = f"❌ PROBLEM\t[{self.job_name}]\t({self.response_time} sec)\t\tURL: {self.url}\nIS NOT IN EXPECTED CODES: {self.last_status_code}\nExpected: {self.expected_codes}"
                        self.update_status_log(status_ind=1, message_inf=message_[2:])

                    elif self.last_status_code == 200:
                        resp = await response.text()
                        if self.scan_html_body(resp):
                            err_type = -1  # no error
                            is_passed = True
                            message_ = f"✅ OK\t[{self.job_name}]\t{self.response_time}s\tURL: {self.url}\tCODE: {self.last_status_code}\nRESP: {resp}"
                            self.update_status_log(status_ind=0, message_inf=message_[2:])

                        else:
                            err_type = 1  # bad response
                            message_ = f"⚠️ WARNING\t[{self.job_name}]\t{self.response_time}s\tURL: {self.url}\nCODE: {self.last_status_code}\nBAD RESP: {resp}"
                            self.update_status_log(status_ind=2, message_inf=message_[3:])

                    else:
                        err_type = 2
                        message_ = f"⚠️ ATTENTION\t[{self.job_name}]\t({self.response_time} sec)\tURL: {self.url}\tCODE: {self.last_status_code}"
                        self.update_status_log(status_ind=2, message_inf=message_[3:])

        except asyncio.TimeoutError as e:
            # resp_time = self.response_time
            self.response_time = None
            self.last_status_code = None
            err_type = 3
            message_ = f"❌ TIMEOUT\t[{self.job_name}]\t(> {self.await_time} sec)\tURL: {self.url}\n{e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        except aiohttp.ClientSSLError as e:
            self.update_resp_time()
            resp_time = self.response_time
            self.response_time = None
            self.last_status_code = None
            err_type = 4
            message_ = f"❌ SSL Error\t[{self.job_name}]\t({resp_time} sec)\tURL: {self.url}\n{e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        except Exception as e:
            self.update_resp_time()
            resp_time = self.response_time
            self.response_time = None
            self.last_status_code = None
            err_type = 5
            message_ = f"❌ REQUEST ERROR\t[{self.job_name}] ({resp_time} sec)\tURL\n: {self.url}: {e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        finally:
            return message_, is_passed, err_type

    async def send_url(self) -> (str, bool, int):

        self.last_request_time = time.perf_counter()
        message_: str = '[empty message]'
        err_type: int = -1  # no error
        is_passed: bool = False

        # timeout = aiohttp.ClientTimeout(connect=self.await_time, total=self.await_time)
        timeout = aiohttp.ClientTimeout(
            total=self.await_time  # Total time for whole operations (in sec)
            #  connect=10,
            #  sock_connect=5,
            #  sock_read=30
        )

        try:

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.url, ssl=self.ssl_verification) as response:

                    self.response_time = time.perf_counter() - self.last_request_time
                    self.response_time = toFixed(self.response_time, 4)
                    self.last_status_code = response.status

                    if self.expected_codes is not None and self.last_status_code not in self.expected_codes and self.last_status_code not in UrlJob.weird_codes:
                        err_type = 0
                        message_ = f"❌ PROBLEM\t[{self.job_name}] ({self.response_time} sec)\tURL: {self.url}\nIS NOT IN EXPECTED CODES: {self.last_status_code}\nExpected: {self.expected_codes}"
                        self.update_status_log(status_ind=1, message_inf=message_[2:])

                    elif self.last_status_code in UrlJob.weird_codes:
                        err_type = 1
                        message_ = f"⚠️ ATTENTION\t[{self.job_name}]\t({self.response_time} sec)\tURL: {self.url}\tWARNING CODE: {self.last_status_code}"
                        self.update_status_log(status_ind=2, message_inf=message_[3:])

                    elif self.last_status_code in UrlJob.ok_codes or (
                            self.expected_codes is not None and self.last_status_code in self.expected_codes):
                        err_type = -1  # no error
                        is_passed = True
                        message_ = f"✅ OK\t[{self.job_name}]\t{self.response_time}s\tURL: {self.url}\tCODE: {self.last_status_code}"
                        self.update_status_log(status_ind=0, message_inf=message_[2:])
                    else:
                        err_type = 2
                        message_ = f"⚠️ ATTENTION\t[{self.job_name}]\t({self.response_time} sec)\tURL: {self.url}\tCODE: {self.last_status_code}"
                        self.update_status_log(status_ind=2, message_inf=message_[3:])

        except asyncio.TimeoutError as e:
            self.response_time = None
            self.last_status_code = None
            err_type = 3
            message_ = f"❌ TIMEOUT\t[{self.job_name}]\t(> {self.await_time} sec)\tURL: {self.url}\n{e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        except aiohttp.ClientSSLError as e:
            self.update_resp_time()
            resp_time = self.response_time
            self.response_time = None
            self.last_status_code = None
            err_type = 4
            message_ = f"❌ SSL Error\t[{self.job_name}]\t(Response time {resp_time} sec)\tURL: {self.url}\n{e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        except Exception as e:
            self.update_resp_time()
            resp_time = self.response_time
            self.response_time = None
            self.last_status_code = None
            err_type = 5
            message_ = f"❌ REQUEST ERROR\t[{self.job_name}]\t({resp_time} sec)\tURL\n: {self.url}: {e}"
            self.update_status_log(status_ind=1, message_inf=message_[2:])

        finally:
            return message_, is_passed, err_type

    async def start_job(self):

        self.running = True

        while self.running:

            if self.job_type.__eq__('[common_urls_module]'):
                message_, is_success, error_t = await self.send_url()
            elif self.job_type.__eq__('[backbones_module]'):
                message_, is_success, error_t = await self.send_burl()
            else:
                LogItOut(message_=f'Unknown job type: [{self.job_type}]', for_tg=False)
                return

            self.problems_counter(is_success)

            if not self.tg_tag.__eq__("*") and not is_success:
                message_ += f"\n{self.tg_tag}"

            LogItOut(message_=message_,
                     for_tg=self.is_for_tg(error_t),
                     add_timestamp=True,
                     chat_lvl_=self.default_chat_id)

            await sleep(self.req_interval_time)
