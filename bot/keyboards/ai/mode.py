from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models.common import Model, GPTVersion
from bot.locales.main import get_localization


def build_mode_keyboard(language_code: str, model: Model, model_version: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT3 + (" ✅" if model == Model.CHAT_GPT and model_version == GPTVersion.V3 else ""),
                callback_data=f'mode:{Model.CHAT_GPT}:{GPTVersion.V3}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4 + (" ✅" if model == Model.CHAT_GPT and model_version == GPTVersion.V4 else ""),
                callback_data=f'mode:{Model.CHAT_GPT}:{GPTVersion.V4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALL_E + (" ✅" if model == Model.DALL_E else ""),
                callback_data=f'mode:{Model.DALL_E}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).MIDJOURNEY + (" ✅" if model == Model.MIDJOURNEY else ""),
                callback_data=f'mode:{Model.MIDJOURNEY}'
            ),
        ],
        [
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
            InlineKeyboardButton(
                text=get_localization(language_code).SUNO + (" ✅" if model == Model.SUNO else ""),
                callback_data=f'mode:{Model.SUNO}'
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
