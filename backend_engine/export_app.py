import time
from asyncio import sleep

from quart import Quart

from problems_statistics import *
from jobs_list import JobsList

app = Quart(__name__)

metrics_data = {
    'occurred_problems_total': 0,
    'actual_problems': 0,
    'uptime_sec': 0
}


@app.route('/jobs_status')
async def get_jobs_status():

    url_logs: str = '\n'.join(job.last_log.get_structured_message() for job in JobsList.url_jobs)
    burl_logs: str = '\n'.join(job.last_log.get_structured_message() for job in JobsList.backbone_jobs)
    sip_logs: str = '\n'.join(job.last_log.get_structured_message() for job in JobsList.sip_jobs)
    mongo_logs: str = '\n'.join(job.last_log.get_structured_message() for job in JobsList.mongo_jobs)
    socket_logs: str = '\n'.join(job.last_log.get_structured_message() for job in JobsList.socket_jobs)

    items: str = f"""
    [URL] jobs:\n
    {url_logs}\n
    [B-URL] jobs:\n
    {burl_logs}\n
    [SIP] jobs:\n
    {sip_logs}\n
    [MONGO] jobs:\n
    {mongo_logs}\n
    [SOCKET] jobs:\n
    {socket_logs}\n
    """
    return items, 200, {'Content-Type': 'text/plain; version=0.0.4'}


@app.route('/monitoring')
async def metrics():
    prometheus_data = f"""
    # HELP occurred_problems_total  Occurred problems since start
    # TYPE occurred_problems_total counter
    occurred_problems_total {metrics_data['occurred_problems_total']}
    # HELP actual_problems Actual problems count
    # TYPE actual_problems counter
    actual_problems {metrics_data['actual_problems']}
    # HELP uptime Service uptime in seconds
    # TYPE uptime_sec counter
    uptime_sec {metrics_data['uptime_sec']}
    """
    return prometheus_data, 200, {'Content-Type': 'text/plain; version=0.0.4'}


async def DataCollector(start_t: time.time):
    # update each 3 seconds
    while (True):
        metrics_data['occurred_problems_total'] = get_occurred_problems_count()
        metrics_data['actual_problems'] = get_problems_count()
        metrics_data['uptime_sec'] = "%s" % (time.time() - start_t)
        await sleep(3)
