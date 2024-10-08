from abc import ABC, abstractmethod

from url_module import UrlJob
from sip_module import SipJob
from mongo_module import MongoJob
from socket_module import SocketJob

class JobManagerAbs(ABC):

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
