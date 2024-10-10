#import time
from asyncio import sleep
from datetime import datetime

import psutil

import problems_statistics

from ms_configs import ServiceData
from logger import LogItOut
from common_methods import toFixed
from job_module import Job

from job_manager_abc import JobManagerAbs


async def highlighter(job_mgr: JobManagerAbs):

    start_time: str = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    prb_count: int = 0

    while True:

        if prb_count == 0:
            await sleep(ServiceData.highlighter_pause) #  2 hours
        else:
            await sleep(ServiceData.highlighter_problems_pause) # 15 min

        prb_count = problems_statistics.get_problems_count(job_mgr)

        problems_message: str = ""
        used_resources_info: str = ""

        if problems_statistics.get_url_problems_count(job_mgr) > 0:
            problems_message += f'[URL]: {problems_statistics.get_url_problems_str(job_mgr)}\n'
        if problems_statistics.get_burl_problems_count(job_mgr) > 0:
            problems_message += f'[B-URL]: {problems_statistics.get_burl_problems_str(job_mgr)}\n'
        if problems_statistics.get_sip_problems_count(job_mgr) > 0:
            problems_message += f'[SIP]: {problems_statistics.get_sip_problems_str(job_mgr)}\n'
        if problems_statistics.get_mongo_problems_count(job_mgr) > 0:
            problems_message += f'[MONGO]: {problems_statistics.get_mongo_problems_str(job_mgr)}\n'
        if problems_statistics.get_socket_problems_count(job_mgr) > 0:
            problems_message += f'[SOCKET]: {problems_statistics.get_socket_problems_str(job_mgr)}\n'

        used_resources_info += f"RAM used (MB): {toFixed(psutil.virtual_memory()[3]/1000000)}\n"

        LogItOut(message_=f'ℹ️ Monitoring system works fine\n'
                          f'Started {start_time}\n'
                          f'Actual problems count: {prb_count}\n'
                          f'Occurred problems since start: {Job.all_occured_problems}\n'
                          f'{problems_message}\n'
                          f'{used_resources_info}',
                 for_tg=True,
                 chat_lvl_=0)
