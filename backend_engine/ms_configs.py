
class TgBotPosterData:

    is_tg_enabled: bool = True

    is_highlighter_enabled: bool = True

    telegram_bot_token: str = 'X'

    chats_list: list[int] = []

    postfix: str = '\n[MSio]'

    is_queue: bool = False
    pause_time: int = 2  # secs


class ServiceData:

    ms_version: str = "1.0.2 alfa"
    highlighter_pause: int = 7200
    highlighter_problems_pause: int = 900

    metrics_ipv4: str = "127.0.0.1"
    metrics_port: int = 65400

    is_export_enabled: bool = False
