from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model, GeminiGPTVersion
from bot.locales.main import get_localization


def build_gemini_keyboard(language_code: str, model: Model, model_version: GeminiGPTVersion) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GEMINI_1_FLASH + (
                    ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Flash else ''
                ),
                callback_data=f'gemini:{GeminiGPTVersion.V1_Flash}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GEMINI_1_PRO + (
                    ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Pro else ''
                ),
                callback_data=f'gemini:{GeminiGPTVersion.V1_Pro}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_gemini_continue_generating_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTINUE_GENERATING,
                callback_data='gemini_continue_generation:continue'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
