import asyncio
import time

import aiohttp

from ms_configs import TgBotPosterData


def GetTgBotUrl() -> str:
    return f"https://api.telegram.org/bot{TgBotPosterData.telegram_bot_token}/sendMessage"


async def send_telegram_message(message: str, chat_lvl: int = 0) -> bool:

    is_success: bool = False

    if chat_lvl < 0 or chat_lvl > len(TgBotPosterData.chats_list) - 1:
        print(f"Wrong chat ID: [{chat_lvl}] Check env-file")
        return is_success #  FALSE
    else:
        telegram_chat_id = TgBotPosterData.chats_list[chat_lvl]

    payload = {
        'chat_id': telegram_chat_id,
        'text': (message + TgBotPosterData.postfix)
    }

    while True:
        if not TgBotPosterData.is_queue:
            try:
                TgBotPosterData.is_queue = True
                async with aiohttp.ClientSession() as session:
                    async with session.post(GetTgBotUrl(), data=payload) as response:
                        if response.status != 200:
                            print(f"Sending error to Telegram: {response.status}, {await response.text()}")
                        else:
                            is_success = True
            except aiohttp.ClientError as e:
                print(f"Request error to Telegram API: {e}")
            finally:
                await asyncio.sleep(1)
                TgBotPosterData.is_queue = False
                break
        else:
            await asyncio.sleep(TgBotPosterData.pause_time)

    return is_success
