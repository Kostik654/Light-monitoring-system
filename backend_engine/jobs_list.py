from url_module import UrlJob
from sip_module import SipJob
from mongo_module import MongoJob
from socket_module import SocketJob


class JobsList:

    url_jobs: list[UrlJob] = []
    backbone_jobs: list[UrlJob] = []
    sip_jobs: list[SipJob] = []
    mongo_jobs: list[MongoJob] = []
    socket_jobs: list[SocketJob] = []

    #  WILL BE DELETED
    @staticmethod
    def get_url_jobs() -> list[UrlJob]:
        return JobsList.url_jobs

    @staticmethod
    def get_backbone_jobs() -> list[UrlJob]:
        return JobsList.backbone_jobs

    @staticmethod
    def get_sip_jobs() -> list[SipJob]:
        return JobsList.sip_jobs

    @staticmethod
    def get_mongo_jobs() -> list[MongoJob]:
        return JobsList.mongo_jobs

    @staticmethod
    def get_socket_jobs() -> list[SocketJob]:
        return JobsList.socket_jobs
