import asyncio

from logger import LogItOut

from url_module import UrlJob
from sip_module import SipJob
from mongo_module import MongoJob
from socket_module import SocketJob
from highlighter_module import highlighter

from ms_configs import TgBotPosterData
from common_methods import GetExpectedCodes

from job_manager_abc import JobManagerAbs



class JobManager(JobManagerAbs):

    def __init__(self, mx_workers: int = 0, job_prfx: str = 'sm_job-'):

        self.__url_jobs: list[UrlJob] = []
        self.__backbone_jobs: list[UrlJob] = []
        self.__sip_jobs: list[SipJob] = []
        self.__mongo_jobs: list[MongoJob] = []
        self.__socket_jobs: list[SocketJob] = []

        #defaults in secs
        self.sip_timeout_default = 15
        self.curl_timeout_default = 5
        self.mongo_timeout_default = 5
        self.socket_timeout_default = 5

        self.sip_interval_default = 60
        self.curl_interval_default = 60
        self.mongo_interval_default = 60
        self.socket_interval_default = 60


    def get_url_jobs(self) -> list[UrlJob]:
        return self.__url_jobs

    def get_backbone_jobs(self) -> list[UrlJob]:
        return self.__backbone_jobs

    def get_sip_jobs(self) -> list[SipJob]:
        return self.__sip_jobs

    def get_mongo_jobs(self) -> list[MongoJob]:
        return self.__mongo_jobs

    def get_socket_jobs(self) -> list[SocketJob]:
        return self.__socket_jobs

    def add_url_job(self, job_splitted: list[str]):

        #expected_ans: str = job_splitted[4]
        # codes or *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[4])

        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = self.curl_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = self.curl_interval_default
        job = UrlJob(stype_=job_splitted[0],
                     url=job_splitted[1],
                     ssl_verify=job_splitted[2].__eq__("ssl"),
                     sname_=job_splitted[3],
                     exp_codes=expected_cds,
                     awtime=timeout,
                     interval_t=interval,
                     default_chat_id_=int(job_splitted[7]),
                     tg_tag_=job_splitted[8])

        if job_splitted[0].__eq__('[common_urls_module]'):
            self.__url_jobs.append(job)
        if job_splitted[0].__eq__('[backbones_module]'):
            self.__backbone_jobs.append(job)


    def add_burl_job(self, job_splitted: list[str]):

        # codes or *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[5])

        if job_splitted[6] != '*':
            timeout = int(job_splitted[6])
        else:
            timeout = self.curl_timeout_default
        if job_splitted[7] != '*':
            interval = int(job_splitted[7])
        else:
            interval = self.curl_interval_default
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

        self.__backbone_jobs.append(job)


    def add_sip_job(self, job_splitted: list[str]):

        # codes of *
        expected_cds: list[int] = GetExpectedCodes(job_splitted[4])

        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = self.sip_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = self.sip_interval_default
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

        self.__sip_jobs.append(job)

    def add_mongo_job(self, job_splitted: list[str]):
        if job_splitted[5] != '*':
            timeout = int(job_splitted[5])
        else:
            timeout = self.mongo_timeout_default
        if job_splitted[6] != '*':
            interval = int(job_splitted[6])
        else:
            interval = self.mongo_interval_default
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

        self.__mongo_jobs.append(job)


    def add_socket_job(self, job_splitted: list[str]):
        if job_splitted[4] != '*':
            timeout = int(job_splitted[4])
        else:
            timeout = self.socket_timeout_default
        if job_splitted[5] != '*':
            interval = int(job_splitted[5])
        else:
            interval = self.socket_interval_default
        job = SocketJob(
                     stype_=job_splitted[0],
                     ipv4_address_=job_splitted[1],
                     ports_names=job_splitted[2],
                     sname_=job_splitted[3],
                     awtime=timeout,
                     interval_t=interval,
                     default_chat_id_=int(job_splitted[6]),
                     tg_tag_=job_splitted[7])

        self.__socket_jobs.append(job)


    def add_job(self, job):

        job_splitted: list[str] = job.split('    ')

        if job_splitted[0].__eq__('[common_urls_module]'):
            try:
                self.add_url_job(job_splitted)
                LogItOut(message_=f'url added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add URL job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)

        if job_splitted[0].__eq__('[backbones_module]'):
            try:
                self.add_burl_job(job_splitted)
                LogItOut(message_=f'burl added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add B-URL job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)

        #elif job_splitted[0].__eq__('[backbones_module]'):
        #    return
        elif job_splitted[0].__eq__('[sip_module]'):
            try:
                self.add_sip_job(job_splitted)
                LogItOut(message_=f'sip added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add SIP job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        elif job_splitted[0].__eq__('[mongo_module]'):
            try:
                self.add_mongo_job(job_splitted)
                LogItOut(message_=f'mongo added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add MONGO job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        elif job_splitted[0].__eq__('[socket_module]'):
            try:
                self.add_socket_job(job_splitted)
                LogItOut(message_=f'socket added: {job_splitted}',
                         for_tg=False,
                         add_timestamp=False)
            except Exception as e:
                LogItOut(message_=f'Failed to add SOCKET job {job_splitted}: {e}',
                         for_tg=False,
                         add_timestamp=False)
        else:
            return

    def start_jobs(self):
        for ujob in self.__url_jobs:
            asyncio.create_task(ujob.start_job())
            LogItOut(message_=f'URL job started: {ujob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for sjob in self.__sip_jobs:
            asyncio.create_task(sjob.start_job())
            LogItOut(message_=f'SIP job started: {sjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for bjob in self.__backbone_jobs:
            asyncio.create_task(bjob.start_job())
            LogItOut(message_=f'B-URL job started: {bjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for mjob in self.__mongo_jobs:
            asyncio.create_task(mjob.start_job())
            LogItOut(message_=f'MONGO job started: {mjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)
        for sktjob in self.__socket_jobs:
            asyncio.create_task(sktjob.start_job())
            LogItOut(message_=f'SOCKET job started: {sktjob.job_name}',
                     for_tg=False,
                     add_timestamp=True)

        if TgBotPosterData.is_highlighter_enabled:
            asyncio.create_task(highlighter(self))
