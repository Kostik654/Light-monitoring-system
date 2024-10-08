import time

from common_methods import toFixed


class Job:
    weird_codes = [403, 502, 503]
    ok_codes = range(200, 405)
    socket_error_descriptions: dict[int, str] = {
        0: "Connection was successful",
        11: "Resource temporarily unavailable (EAGAIN)",
        111: "Connection refused (ECONNREFUSED)",
        101: "Network unreachable (ENETUNREACH)",
        104: "Connection reset by peer (ECONNRESET)",
        113: "Host is unreachable (EHOSTUNREACH)",
        110: "Connection timed out (ETIMEDOUT)",
        19: "No such device (ENODEV)",
        2: "No such file or directory (ENOENT)",
    }
    all_occured_problems: int = 0

    def __init__(self, name_: str, type_: str, interval_time: int, awtime: int, exp_codes: list[int] = None, chat_id_:int = 0):
        self.job_name: str = name_
        self.job_type: str = type_
        self.req_interval_time: int = interval_time
        self.await_time: int = awtime
        self.expected_codes: list[int] = exp_codes
        self.default_chat_id: int = chat_id_

        self.last_failed: bool = False
        self.response_time: float = -1  # secs,ms
        self.last_request_time = None # Time of the last request
        self.last_status_code: int = -1
        self.last_error_type: int = -1 # no error
        self.running: bool = False
        self.occurred_problems_count: int = 0

    def is_for_tg(self, current_error_t) -> bool:
        if self.last_error_type == current_error_t:
            return False
        else:
            self.last_error_type = current_error_t
            return True

    def problems_counter(self, is_success: bool = False):
        if is_success:
            self.last_failed = False
        else:
            if not self.last_failed:
                self.occurred_problems_count += 1
                Job.all_occured_problems += 1

            self.last_failed = True

    def update_resp_time(self):
        self.response_time = time.perf_counter() - self.last_request_time
        self.response_time = toFixed(self.response_time, 4)
