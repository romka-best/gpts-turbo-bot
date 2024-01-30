from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.role import Role
from bot.locales.main import get_localization


def build_catalog_keyboard(language_code: str, current_role: str, roles: List[Role]) -> InlineKeyboardMarkup:
    buttons = []
    for role in roles:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=role.translated_names.get(language_code, role.name) + (
                        " ✅" if current_role == role.name else " ❌"
                    ),
                    callback_data=f'catalog:{role.name}'
                )
            ],
        )
    buttons.append([
        InlineKeyboardButton(
            text=get_localization(language_code).CLOSE,
            callback_data='catalog:close'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_catalog_keyboard(language_code: str, roles: List[Role]) -> InlineKeyboardMarkup:
    buttons = []
    for role in roles:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=role.translated_names.get(language_code, role.name),
                    callback_data=f'catalog_manage:{role.id}'
                )
            ],
        )
    buttons.extend([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATE_ROLE,
                callback_data='catalog_manage:create'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='catalog_manage:close'
            )
        ]
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_catalog_create_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='catalog_manage_create:back'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='catalog_manage_create:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_catalog_create_role_confirmation_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).APPROVE,
                callback_data='catalog_manage_create_role_confirmation:approve'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='catalog_manage_create_role_confirmation:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_catalog_edit_keyboard(language_code: str, system_role: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EDIT_ROLE_NAME,
                callback_data=f'catalog_manage_edit:name:{system_role}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EDIT_ROLE_DESCRIPTION,
                callback_data=f'catalog_manage_edit:description:{system_role}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EDIT_ROLE_INSTRUCTION,
                callback_data=f'catalog_manage_edit:instruction:{system_role}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='catalog_manage_edit:back'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
