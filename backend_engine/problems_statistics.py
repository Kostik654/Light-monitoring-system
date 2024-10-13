from job_module import Job
from job_manager_abc import JobManagerAbs


def get_url_problems_count(job_mgr: JobManagerAbs, get_all: bool = False) -> int:
    if not get_all:
        return sum(job.last_failed is True for job in job_mgr.get_url_jobs())
    else:
        return sum(job.occurred_problems_count for job in job_mgr.get_url_jobs())


def get_burl_problems_count(job_mgr: JobManagerAbs, get_all: bool = False) -> int:
    if not get_all:
        return sum(job.last_failed is True for job in job_mgr.get_backbone_jobs())
    else:
        return sum(job.occurred_problems_count for job in job_mgr.get_backbone_jobs())


def get_sip_problems_count(job_mgr: JobManagerAbs, get_all: bool = False) -> int:
    if not get_all:
        return sum(job.last_failed is True for job in job_mgr.get_sip_jobs())
    else:
        return sum(job.occurred_problems_count for job in job_mgr.get_sip_jobs())


def get_socket_problems_count(job_mgr: JobManagerAbs, get_all: bool = False) -> int:
    if not get_all:
        return sum(job.last_failed is True for job in job_mgr.get_socket_jobs())
    else:
        return sum(job.occurred_problems_count for job in job_mgr.get_socket_jobs())


def get_mongo_problems_count(job_mgr: JobManagerAbs, get_all: bool = False) -> int:
    if not get_all:
        return sum(job.last_failed is True for job in job_mgr.get_mongo_jobs())
    else:
        return sum(job.occurred_problems_count for job in job_mgr.get_mongo_jobs())


def get_url_problems_str(job_mgr: JobManagerAbs) -> str:
    return ', '.join(job.job_name for job in job_mgr.get_url_jobs() if job.last_failed)


def get_burl_problems_str(job_mgr: JobManagerAbs) -> str:
    return ', '.join(job.job_name for job in job_mgr.get_backbone_jobs() if job.last_failed)


def get_sip_problems_str(job_mgr: JobManagerAbs) -> str:
    return ', '.join(job.job_name for job in job_mgr.get_sip_jobs() if job.last_failed)


def get_socket_problems_str(job_mgr: JobManagerAbs) -> str:
    return ', '.join(job.job_name for job in job_mgr.get_socket_jobs() if job.last_failed)


def get_mongo_problems_str(job_mgr: JobManagerAbs) -> str:
    return ', '.join(job.job_name for job in job_mgr.get_mongo_jobs() if job.last_failed)


def get_occurred_problems_count() -> int:
    return Job.all_occured_problems


def get_problems_count(job_mgr: JobManagerAbs) -> int:
    problems: int = (get_mongo_problems_count(job_mgr) +
                     get_sip_problems_count(job_mgr) +
                     get_url_problems_count(job_mgr) +
                     get_socket_problems_count(job_mgr) +
                     get_burl_problems_count(job_mgr))

    return problems
