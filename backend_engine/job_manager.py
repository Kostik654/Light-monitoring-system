import asyncio
import time
from datetime import datetime

from logger import LogItOut

from url_module import UrlJob
from sip_module import SipJob
from mongo_module import MongoJob
from socket_module import SocketJob
from highlighter_module import highlighter

from ms_configs import ServiceData, TgBotPosterData
from common_methods import GetExpectedCodes

from export_app import DataCollector
from jobs_list import JobsList


class JobManager:
    # defaults in secs
    sip_timeout_default: int = 15
    curl_timeout_default: int = 5
    mongo_timeout_default: int = 5
    socket_timeout_default: int = 5

    sip_interval_default: int = 60
    curl_interval_default: int = 60
    mongo_interval_default: int = 60
    socket_interval_default: int = 60

    @staticmethod
    def add_url_job(job_splitted: list[str]):
        # expected_ans: str = job_splitted[4]
        # codes or *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[4])

        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = JobManager.curl_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = JobManager.curl_interval_default
        job = UrlJob(stype_=job_splitted[0],
                     url=job_splitted[1],
                     ssl_verify=job_splitted[2].__eq__("ssl"),
                     sname_=job_splitted[3],
                     exp_codes=expected_cds,
                     awtime=timeout,
                     interval_t=interval,
                     default_chat_id_=int(job_splitted[7]),
                     tg_tag_=job_splitted[8])

        JobsList.url_jobs.append(job)

    @staticmethod
    def add_burl_job(job_splitted: list[str]):

        # codes or *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[5])

        if job_splitted[6] != '*':
            timeout = int(job_splitted[6])
        else:
            timeout = JobManager.curl_timeout_default
        if job_splitted[7] != '*':
            interval = int(job_splitted[7])
        else:
            interval = JobManager.curl_interval_default
        job = UrlJob(stype_=job_splitted[0],
                     url=job_splitted[1],
                     ssl_verify=job_splitted[2].__eq__("ssl"),
                     sname_=job_splitted[3],
                     exp_answer_=job_splitted[4],
                     exp_codes=expected_cds,
                     awtime=timeout,
                     interval_t=interval,
                     default_chat_id_=int(job_splitted[8]),
                     tg_tag_=job_splitted[9])

        JobsList.backbone_jobs.append(job)

    @staticmethod
    def add_sip_job(job_splitted: list[str]):

        # codes of *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[4])

        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = JobManager.sip_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = JobManager.sip_interval_default
        job = SipJob(
            stype_=job_splitted[0],
            ipv4_address_=job_splitted[1],
            port_=int(job_splitted[2]),
            sname_=job_splitted[3],
            exp_codes=expected_cds,
            awtime=timeout,
            interval_t=interval,
            default_chat_id_=int(job_splitted[7]),
            tg_tag_=job_splitted[8])

        JobsList.sip_jobs.append(job)

    @staticmethod
    def add_mongo_job(job_splitted: list[str]):
        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = JobManager.mongo_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = JobManager.mongo_interval_default
        job = MongoJob(
            stype_=job_splitted[0],
            ipv4_address_=job_splitted[1],
            port_=int(job_splitted[2]),
            mrole=job_splitted[3],
            sname_=job_splitted[4],
            awtime=timeout,
            interval_t=interval,
            default_chat_id_=int(job_splitted[7]),
            tg_tag_=job_splitted[8])

        JobsList.mongo_jobs.append(job)

    @staticmethod
    def add_socket_job(job_splitted: list[str]):
        if job_splitted[4] != '*':
            timeout = int(job_splitted[4])
        else:
            timeout = JobManager.socket_timeout_default
        if job_splitted[5] != '*':
            interval = int(job_splitted[5])
        else:
            interval = JobManager.socket_interval_default
        job = SocketJob(
            stype_=job_splitted[0],
            ipv4_address_=job_splitted[1],
            ports_names=job_splitted[2],
            sname_=job_splitted[3],
            awtime=timeout,
            interval_t=interval,
            default_chat_id_=int(job_splitted[6]),
            tg_tag_=job_splitted[7])

        JobsList.socket_jobs.append(job)

    @staticmethod
    def add_job(job):

        job_splitted: list[str] = job.split('    ')

        if job_splitted[0].__eq__('[common_urls_module]'):
            try:
                JobManager.add_url_job(job_splitted)
                LogItOut(message_=f'url added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add URL job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)

        if job_splitted[0].__eq__('[backbones_module]'):
            try:
                JobManager.add_burl_job(job_splitted)
                LogItOut(message_=f'burl added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add B-URL job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)

        # elif job_splitted[0].__eq__('[backbones_module]'):
        #    return
        elif job_splitted[0].__eq__('[sip_module]'):
            try:
                JobManager.add_sip_job(job_splitted)
                LogItOut(message_=f'sip added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add SIP job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        elif job_splitted[0].__eq__('[mongo_module]'):
            try:
                JobManager.add_mongo_job(job_splitted)
                LogItOut(message_=f'mongo added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add MONGO job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        elif job_splitted[0].__eq__('[socket_module]'):
            try:
                JobManager.add_socket_job(job_splitted)
                LogItOut(message_=f'socket added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add SOCKET job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        else:
            return

    @staticmethod
    def start_jobs():
        for ujob in JobsList.url_jobs:
            asyncio.create_task(ujob.start_job())
            LogItOut(message_=f'URL job started: {ujob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for sjob in JobsList.sip_jobs:
            asyncio.create_task(sjob.start_job())
            LogItOut(message_=f'SIP job started: {sjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for bjob in JobsList.backbone_jobs:
            asyncio.create_task(bjob.start_job())
            LogItOut(message_=f'B-URL job started: {bjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for mjob in JobsList.mongo_jobs:
            asyncio.create_task(mjob.start_job())
            LogItOut(message_=f'MONGO job started: {mjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for sktjob in JobsList.socket_jobs:
            asyncio.create_task(sktjob.start_job())
            LogItOut(message_=f'SOCKET job started: {sktjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)

        # TG highligher
        if TgBotPosterData.is_highlighter_enabled:
            asyncio.create_task(highlighter(start_t=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")))
        # Prometheus exporter
        if ServiceData.is_export_enabled:
            asyncio.create_task(DataCollector(start_t=time.time()))
