import time
from asyncio import sleep

from quart import Quart

from problems_statistics import *
from job_manager_abc import JobManagerAbs

app = Quart(__name__)

metrics_data = {
    'occurred_problems_total': 0,
    'actual_problems': 0,
    'uptime_sec': 0
}


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


async def DataCollector(job_mgr: JobManagerAbs, start_t: time.time):

    # update each 3 seconds
    while (True):
        metrics_data['occurred_problems_total'] = get_occurred_problems_count()
        metrics_data['actual_problems'] = get_problems_count(job_mgr)
        metrics_data['uptime_sec'] = "%s" % (time.time() - start_t)
        await sleep(3)
