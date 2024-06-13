from typing import Dict, Type

from aiogram.fsm.storage.base import BaseStorage

from . import en, ru
from .texts import Texts
from ..database.operations.user.updaters import update_user

localization_classes: Dict[str, Type[Texts]] = {
    'en': en.English,
    'ru': ru.Russian
}


async def set_user_language(user_id: str, language_code: str, storage: BaseStorage):
    if language_code not in localization_classes.keys():
        language_code = 'en'

    key = f"user:{user_id}:language"
    await storage.redis.set(key, language_code)

    await update_user(
        user_id,
        {
            "interface_language_code": language_code,
        }
    )


async def get_user_language(user_id: str, storage: BaseStorage) -> str:
    key = f"user:{user_id}:language"
    language_code = await storage.redis.get(key)
    if language_code is not None:
        language_code = language_code.decode()

    if language_code not in localization_classes.keys():
        return 'en'

    return language_code


def get_localization(language_code: str) -> Texts:
    localization_class = localization_classes.get(language_code, en.English)
    return localization_class()
