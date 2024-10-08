

class TgBotPosterData:

    is_tg_enabled: bool = True

    is_highlighter_enabled: bool = True

    telegram_bot_token: str = 'X'

    chats_list: list[int] = []

    postfix: str = '\n[MSio]'

    is_queue: bool = False
    pause_time: int = 2 #secs


class ServiceData:

    highlighter_pause: int = 7200
    highlighter_problems_pause: int = 900
