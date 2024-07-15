from bot.config import config


def is_admin(chat_id: str) -> bool:
    return chat_id == config.SUPER_ADMIN_ID or chat_id in config.ADMIN_IDS
