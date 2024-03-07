from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.role import Role
from bot.locales.main import get_localization


def build_catalog_keyboard(language_code: str, current_role: str, roles: List[Role]) -> InlineKeyboardMarkup:
    buttons = []
    for role in roles:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=role.translated_names.get(language_code, role.name) + (
                        " ✅" if current_role == role.name else " ❌"
                    ),
                    callback_data=f'catalog:{role.name}'
                )
            ],
        )
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).BACK,
            callback_data='catalog:back'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
