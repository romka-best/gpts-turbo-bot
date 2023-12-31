from bot.config import config


def is_admin(chat_id: str) -> bool:
    return chat_id in config.ADMIN_CHAT_IDS
