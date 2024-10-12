import signal
import sys
import asyncio
import uvicorn
from asyncio import sleep, AbstractEventLoop

from common_methods import GetExpectedCodes
from logger import LogItOut
from job_manager import JobManager
from ms_configs import TgBotPosterData, ServiceData
from export_app import app

urls_path = '/etc/monsys/jobs_list'
env_path = '/etc/monsys/.env'
wrong_chars = [' ', '#', '!']


def signal_handler(sig: int):
    LogItOut(message_=f'🔴 Emergency shutdown of the monitoring system with SIG: {signal.Signals(sig).name} [{sig}]\n',
             for_tg=True,
             add_timestamp=True)
    sys.exit(0)


def work_error(message_: str):
    LogItOut(message_=f'⭕️ Forced shutdown of the monitoring system with message: {message_}\n',
             for_tg=True,
             add_timestamp=True)
    sys.exit(0)


def enable_signals(loop: AbstractEventLoop):
    loop.add_signal_handler(signal.SIGINT, signal_handler, signal.SIGINT)
    loop.add_signal_handler(signal.SIGTERM, signal_handler, signal.SIGTERM)
    loop.add_signal_handler(signal.SIGQUIT, signal_handler, signal.SIGQUIT)
    loop.add_signal_handler(signal.SIGABRT, signal_handler, signal.SIGABRT)


def load_configuration(file_path: str = ".env") -> bool:
    LogItOut(message_=f'Uploading configuration...',
             for_tg=False,
             add_timestamp=False)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            conf_strs = file.read().splitlines()

        TgBotPosterData.telegram_bot_token = conf_strs[0].split('=')[1]
        TgBotPosterData.chats_list = GetExpectedCodes(conf_strs[1].split('=')[1], ' ')
        TgBotPosterData.postfix = f"\n{conf_strs[2].split('=')[1]}"
        TgBotPosterData.is_tg_enabled = conf_strs[3].split('=')[1].__eq__('True')

        TgBotPosterData.is_highlighter_enabled = conf_strs[4].split('=')[1].__eq__('True')

        ServiceData.highlighter_pause = int(conf_strs[5].split('=')[1])
        ServiceData.highlighter_problems_pause = int(conf_strs[6].split('=')[1])

        ServiceData.is_export_enabled = conf_strs[7].split('=')[1].__eq__('True')

        ServiceData.metrics_ipv4 = conf_strs[8].split('=')[1].split(':')[0]
        ServiceData.metrics_port = int(conf_strs[8].split('=')[1].split(':')[1])

        LogItOut(message_=f'Service configuration is loaded',
                 for_tg=False,
                 add_timestamp=False)

        return True
    except Exception as e:
        LogItOut(message_=f"Service configuration: Error reading file: {file_path}: {e}",
                 for_tg=False,
                 add_timestamp=False)
        return False


def get_urls(file_path: str = "urls.txt"):
    LogItOut(message_=f'Uploading monitoring modules...',
             for_tg=False,
             add_timestamp=False)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = file.read().splitlines()
        LogItOut(message_=f'Monitoring modules are loaded',
                 for_tg=False,
                 add_timestamp=False)
        return urls
    except Exception as e:
        LogItOut(message_=f"Monitoring modules: Error reading file: {file_path}: {e}",
                 for_tg=False,
                 add_timestamp=False)
        return []


async def main():
    loop = asyncio.get_event_loop()
    enable_signals(loop)

    LogItOut(message_=f'Creating job manager',
             for_tg=False,
             add_timestamp=False)

    manager = JobManager()

    for url_ in get_urls(urls_path):
        if url_.__eq__(''):
            continue
        if url_[0] not in wrong_chars:
            manager.add_job(url_)

    modules_: str = ""

    if len(manager.get_mongo_jobs()) > 0:
        modules_ += f"URL module loaded: {len(manager.get_url_jobs())}\n"
    if len(manager.get_sip_jobs()) > 0:
        modules_ += f"SIP module loaded: {len(manager.get_sip_jobs())}\n"
    if len(manager.get_backbone_jobs()) > 0:
        modules_ += f"B-URL module loaded: {len(manager.get_backbone_jobs())}\n"
    if len(manager.get_mongo_jobs()) > 0:
        modules_ += f"MONGO module loaded: {len(manager.get_mongo_jobs())}\n"
    if len(manager.get_socket_jobs()) > 0:
        modules_ += f"SOCKET module loaded: {len(manager.get_socket_jobs())}\n"

    sum_ = len(manager.get_url_jobs()) + len(manager.get_sip_jobs()) + len(manager.get_backbone_jobs()) + len(
        manager.get_mongo_jobs()) + len(manager.get_socket_jobs())

    if sum_ > 0:

        manager.start_jobs()

        LogItOut(message_=f'\n🟢 STARTED: {sum_} jobs\n{modules_}\nv{ServiceData.ms_version}',
                 for_tg=True,
                 chat_lvl_=0)

        if ServiceData.is_export_enabled:
            try:
                config = uvicorn.Config(app, host=ServiceData.metrics_ipv4, port=ServiceData.metrics_port)
                server = uvicorn.Server(config)
                asyncio.create_task(server.serve())
                LogItOut(message_=f"Exporter is running on {ServiceData.metrics_ipv4}:{ServiceData.metrics_port}",
                         for_tg=False)
            except Exception as e:
                LogItOut(message_=f"Exporter running exception: {e}", for_tg=False)

        while (True):
            await sleep(10)

    else:
        work_error(message_="No tasks")


if __name__ == '__main__':

    if not load_configuration(env_path):
        work_error(message_="Configuration uploading error. Check logs.")

    try:
        asyncio.run(main())
    except Exception as e:
        work_error(message_=e.__str__())
