from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.package import PackageType
from bot.locales.main import get_localization


def build_bonus_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT3_REQUESTS,
                callback_data=f'bonus:{PackageType.GPT3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT4_REQUESTS,
                callback_data=f'bonus:{PackageType.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).THEMATIC_CHATS,
                callback_data=f'bonus:{PackageType.CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3_REQUESTS,
                callback_data=f'bonus:{PackageType.DALLE3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_REQUESTS,
                callback_data=f'bonus:{PackageType.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACCESS_TO_CATALOG,
                callback_data=f'bonus:{PackageType.ACCESS_TO_CATALOG}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES,
                callback_data=f'bonus:{PackageType.VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FAST_ANSWERS,
                callback_data=f'bonus:{PackageType.FAST_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='bonus:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
