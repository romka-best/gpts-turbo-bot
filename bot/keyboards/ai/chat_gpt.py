from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model, ChatGPTVersion
from bot.locales.main import get_localization


def build_chat_gpt_keyboard(language_code: str, model: Model, model_version: ChatGPTVersion) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4_OMNI_MINI + (
                    " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni_Mini else ""
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V4_Omni_Mini}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4_TURBO + (
                    " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Turbo else ""
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V4_Turbo}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4_OMNI + (
                    " ✅" if model == Model.CHAT_GPT and model_version == ChatGPTVersion.V4_Omni else ""
                ),
                callback_data=f'chat_gpt:{ChatGPTVersion.V4_Omni}'
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_chat_gpt_continue_generating_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTINUE_GENERATING,
                callback_data='chat_gpt_continue_generation:continue'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
