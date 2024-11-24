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
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GEMINI_1_ULTRA + (
                    ' ✅' if model == Model.GEMINI and model_version == GeminiGPTVersion.V1_Ultra else ''
                ),
                callback_data=f'gemini:{GeminiGPTVersion.V1_Ultra}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
