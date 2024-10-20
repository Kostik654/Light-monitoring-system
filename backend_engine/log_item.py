from job_module_abc import JobBase


class log_item:

    statuses: dict[int,str] = {
        0: "✅",
        1: "❌",
        2: "⚠️"
    }

    def __init__(self, status_: int = 1, job_: JobBase = None, message_info: str = "No messages"):
        self.status_index: int = status_
        self.job: JobBase = job_
        self.info_message = message_info

    def get_status_ico(self) -> str:
        return log_item.statuses[self.status_index]

    def get_structured_message(self, splitter: chr = '\t') -> str or None:

        if self.job.job_type.__eq__('[common_urls_module]'):
            return f"{self.get_status_ico()}" \
                   f"{splitter}" \
                   f"{self.get_status_code()}" \
                   f"{splitter}" \
                   f"{self.job.job_name}" \
                   f"{splitter}" \
                   f"{self.info_message}"
        else:
            return None

    def get_status_code(self) -> int:
        return self.job.last_status_code