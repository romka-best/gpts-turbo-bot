from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model, ChatGPTVersion
from bot.locales.main import get_localization
from bot.locales.types import LanguageCode


def build_chat_gpt_keyboard(language_code: LanguageCode, model: Model, model_version: ChatGPTVersion) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHAT_GPT_4_OMNI_MINI + (
                    ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni_Mini else ''
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V4_Omni_Mini}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHAT_GPT_4_OMNI + (
                    ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni else ''
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V4_Omni}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHAT_GPT_O_1_MINI + (
                    ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O_Mini else ''
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V1_O_Mini}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHAT_GPT_O_1 + (
                    ' ✅' if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V1_O else ''
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V1_O}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
