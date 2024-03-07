from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model
from bot.locales.main import get_localization


def build_chat_gpt_keyboard(language_code: str, model: Model) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT3 + (" ✅" if model == Model.GPT3 else ""),
                callback_data=f'chat_gpt:{Model.GPT3}'
            ),
            InlineKeyboardButton(
                text=get_localization(language_code).CHATGPT4 + (" ✅" if model == Model.GPT4 else ""),
                callback_data=f'chat_gpt:{Model.GPT4}'
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
