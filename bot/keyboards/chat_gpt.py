from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.locales.main import get_localization


def build_chat_gpt_continue_generating_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTINUE_GENERATING,
                callback_data='chat_gpt:continue_generating'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
