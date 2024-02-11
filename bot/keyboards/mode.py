from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model
from bot.locales.main import get_localization


def build_mode_keyboard(language_code: str, model: Model) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT3 + (" ✅" if model == Model.GPT3 else ""),
                callback_data=f'mode:{Model.GPT3}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4 + (" ✅" if model == Model.GPT4 else ""),
                callback_data=f'mode:{Model.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3 + (" ✅" if model == Model.DALLE3 else ""),
                callback_data=f'mode:{Model.DALLE3}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP + (" ✅" if model == Model.FACE_SWAP else ""),
                callback_data=f'mode:{Model.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MUSIC_GEN + (" ✅" if model == Model.MUSIC_GEN else ""),
                callback_data=f'mode:{Model.MUSIC_GEN}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='mode:close'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
