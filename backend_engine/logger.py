import datetime

from tgbot_post import send_telegram_message
from ms_configs import TgBotPosterData


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
            print(message_ + f"\t{datetime.datetime.now()}")
        else:
            print(message_ )
