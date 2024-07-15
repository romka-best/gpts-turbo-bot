from bot.config import config


def is_developer(chat_id: str) -> bool:
    return chat_id in config.DEVELOPER_IDS
