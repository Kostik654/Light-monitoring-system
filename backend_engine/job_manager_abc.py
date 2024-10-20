from abc import ABC, abstractmethod

from url_module import UrlJob
from sip_module import SipJob
from mongo_module import MongoJob
from socket_module import SocketJob


class JobManagerAbs(ABC):

    def __init__(self):

        self.__url_jobs: list[UrlJob] = []
        self.__backbone_jobs: list[UrlJob] = []
        self.__sip_jobs: list[SipJob] = []
        self.__mongo_jobs: list[MongoJob] = []
        self.__socket_jobs: list[SocketJob] = []

        # defaults in secs
        self.sip_timeout_default = 15
        self.curl_timeout_default = 5
        self.mongo_timeout_default = 5
        self.socket_timeout_default = 5

        self.sip_interval_default = 60
        self.curl_interval_default = 60
        self.mongo_interval_default = 60
        self.socket_interval_default = 60

    @abstractmethod
    def get_url_jobs(self) -> list[UrlJob]:
        ...

    @abstractmethod
    def get_backbone_jobs(self) -> list[UrlJob]:
        ...

    @abstractmethod
    def get_sip_jobs(self) -> list[SipJob]:
        ...

    @abstractmethod
    def get_mongo_jobs(self) -> list[MongoJob]:
        ...

    @abstractmethod
    def get_socket_jobs(self) -> list[SocketJob]:
        ...
