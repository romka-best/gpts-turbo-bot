from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.chat import Chat
from bot.locales.main import get_localization


def build_chats_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_CHATS,
                callback_data=f'chat:show'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATE_CHAT,
                callback_data=f'chat:create'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SWITCH_CHAT,
                callback_data=f'chat:switch'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).RESET_CHAT,
                callback_data=f'chat:reset'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DELETE_CHAT,
                callback_data=f'chat:delete'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='chat:back'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_chat_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_chat:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_switch_chat_keyboard(language_code: str, current_chat_id: str, chats: List[Chat]) -> InlineKeyboardMarkup:
    buttons = []
    for chat in chats:
        buttons.append([
            InlineKeyboardButton(
                text=f"{chat.title}" + (" ✅" if current_chat_id == chat.id else " ❌"),
                callback_data=f"switch_chat:{chat.id}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).CANCEL,
            callback_data='switch_chat:cancel'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_delete_chat_keyboard(language_code: str, current_chat_id: str, chats: List[Chat]) -> InlineKeyboardMarkup:
    buttons = []
    for chat in chats:
        if current_chat_id != chat.id:
            buttons.append([
                InlineKeyboardButton(
                    text=chat.title,
                    callback_data=f"delete_chat:{chat.id}"
                )
            ])
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).CANCEL,
            callback_data='delete_chat:cancel'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_reset_chat_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).APPROVE,
                callback_data='reset_chat:approve'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='reset_chat:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
