#import sys
import time
from asyncio import sleep

import pymongo

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from job_module import Job
from logger import LogItOut
from common_methods import toFixed


class MongoJob(Job):
    def __init__(self,
                 ipv4_address_: str,
                 port_: int,
                 #dbs_: list[str],
                 sname_: str,
                 stype_: str,
                 awtime: int = 5,
                 interval_t: int = 60,
                 mrole:str = 'primary',
                 default_chat_id_: int = 0
                 ):

        super().__init__(name_=sname_,
                         type_=stype_,
                         interval_time=interval_t,
                         awtime=awtime,
                         chat_id_=default_chat_id_)

        self.remote_ipv4_address = ipv4_address_
        self.remote_port = port_

        if mrole.__eq__('primary') or mrole.__eq__('secondary'):
            self.mongo_role = mrole
        else:
            self.mongo_role = 'primary'


    def start_test(self, test_name: str) -> (bool, str, str, int):
        is_passed: bool = False
        message_: str = "START TEST"
        last_request_time = time.time()
        response_time = None
        err_type = -1 # no error
        client = MongoClient()

        try:

            client = MongoClient(self.remote_ipv4_address, self.remote_port)

            db = client["test-database"]
            collection = db["test-collection"]
            coll_instance = {"name": "test-item"}

            with pymongo.timeout(self.await_time):
                if test_name.__eq__('insert'):
                    collection.insert_one(coll_instance)
                    is_passed = True
                elif test_name.__eq__('find'):
                    collection.find_one(coll_instance)
                    is_passed = True
                elif test_name.__eq__('delete'):
                    collection.delete_one(coll_instance)
                    is_passed = True
                else:
                    is_passed = False
                    raise Exception('Unknown test', f'{test_name}')

            response_time = toFixed(time.time() - last_request_time, 4)
            message_ = f"✅ OK: [{test_name}] test: {response_time}sec (max {self.await_time}sec)"
        except PyMongoError as exc:
            response_time = toFixed(time.time() - last_request_time, 4)
            if exc.timeout:
                message_ = f"❌ Timeout test [{test_name}] is failed: {response_time}sec (max {self.await_time}sec)"
                err_type = 0
            else:
                message_ = f"❌ Failed with non-timeout error [{test_name}]: {exc!r}"
                err_type = 1
        except Exception as e:
            response_time = toFixed(time.time() - last_request_time, 4)
            message_ = f"❌ PROBLEM: [{self.job_name}] testing error: {e.args[0]}: {e.args[1]}"
            err_type = 2
        finally:
            client.close()
            return is_passed, message_, response_time, err_type

    def start_testing(self) -> (bool, str):

        message_: str = f"Mongo DB revision {self.remote_ipv4_address}:{self.remote_port} <{self.mongo_role}> [{self.job_name}]\n"

        is_insertion_done, mess, resp_time, error_type = self.start_test('insert')
        message_ += f"{mess}\n"

        is_searching_done, mess, resp_time, error_type = self.start_test('find')
        message_ += f"{mess}\n"

        is_deletion_done, mess, resp_time, error_type = self.start_test('delete')
        message_ += f"{mess}\n"

        is_success: bool = is_insertion_done and is_searching_done and is_deletion_done

        return message_, is_success


    async def start_job(self):

        self.running = True

        while self.running:

            message_, is_success = self.start_testing()

            if is_success:
                is_for_tg = self.last_failed


                self.last_failed = False
                LogItOut(message_=message_,
                         for_tg=is_for_tg,
                         add_timestamp=not is_for_tg,
                         chat_lvl_=self.default_chat_id)
            else:

                prev_failed = self.last_failed

                self.problems_counter() #  self.last_failed = True

                LogItOut(message_=message_,
                         for_tg=not prev_failed,
                         add_timestamp=prev_failed,
                         chat_lvl_=self.default_chat_id)

            await sleep(self.req_interval_time)
