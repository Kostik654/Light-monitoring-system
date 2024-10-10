import datetime

from tgbot_post import send_telegram_message
from ms_configs import TgBotPosterData

log_path: str = "/var/log/monsys/monitor.log"


def LogItOut(message_: str,
             for_tg: bool = False,
             just_for_tg: bool = False,
             add_timestamp: bool = True,
             chat_lvl_: int = 0):

    if message_ is None:
        return

    if TgBotPosterData.is_tg_enabled and (for_tg or just_for_tg):
        send_telegram_message(message=message_, chat_lvl=chat_lvl_)

    if not just_for_tg:
        message_ = message_.replace('\n', '\t')
        if add_timestamp:
            print(f"{message_}\t{datetime.datetime.now()}")
        else:
            print(message_ )

        # to file
        try:
            with open(log_path, 'a') as file:
                file.write(f"{message_}\t{datetime.datetime.now()}")
        except Exception as e:
            print(f"Exception occurred while reading {log_path} file [Adding strs]\n{e.__str__()}")
