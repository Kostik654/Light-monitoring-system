import time

from common_methods import toFixed
from job_module_abc import JobBase
from log_item import log_item


class Job(JobBase):

    def __init__(self, name_: str, type_: str, interval_time: int, awtime: int, exp_codes: list[int] = None, chat_id_: int = 0, tg_tag_: str = "*"):
        super().__init__(name_, type_, interval_time, awtime, exp_codes, chat_id_, tg_tag_)

        self.last_log: log_item = log_item()

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

    def update_status_log(self, status_ind: int, message_inf: str):
        self.last_log = log_item(status_=status_ind, job_=self, message_info=message_inf)
