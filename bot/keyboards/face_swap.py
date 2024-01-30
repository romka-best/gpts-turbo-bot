from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.face_swap_package import FaceSwapPackage, FaceSwapPackageStatus
from bot.database.models.generation import GenerationReaction
from bot.database.models.user import UserGender
from bot.locales.main import get_localization


def build_face_swap_choose_keyboard(language_code: str, packages: List[FaceSwapPackage]) -> InlineKeyboardMarkup:
    buttons = []
    for package in packages:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=package.translated_names.get(language_code, package.name),
                    callback_data=f'face_swap_choose:{package.name}'
                )
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_face_swap_package_keyboard(language_code: str, quantities: List[int]) -> InlineKeyboardMarkup:
    buttons = []
    for quantity in quantities:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f'🔹 {quantity}',
                    callback_data=f'face_swap_package:{quantity}'
                )
            ]
        )

    buttons.extend([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='face_swap_package:back'
            )
        ],
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_face_swap_reaction_keyboard(language_code: str, generation_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="👍",
                callback_data=f'face_swap_reaction:{GenerationReaction.LIKED}:{generation_id}'
            ),
            InlineKeyboardButton(
                text="👎",
                callback_data=f'face_swap_reaction:{GenerationReaction.DISLIKED}:{generation_id}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='face_swap_reaction:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATE_PACKAGE,
                callback_data='fsm:create'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EDIT_PACKAGE,
                callback_data='fsm:edit'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='fsm:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_create_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='fsm_create:back'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='fsm_create:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_create_confirmation_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).APPROVE,
                callback_data='fsm_create_confirmation:approve'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='fsm_create_confirmation:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_choose_gender_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MALE,
                callback_data=f'fsm_edit_choose_gender:{UserGender.MALE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FEMALE,
                callback_data=f'fsm_edit_choose_gender:{UserGender.FEMALE}'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_choose_package_keyboard(language_code: str,
                                                        packages: List[FaceSwapPackage]) -> InlineKeyboardMarkup:
    buttons = []
    for package in packages:
        buttons.append([
            InlineKeyboardButton(
                text=f"{package.name} ({package.translated_names.get(language_code, package.name)})",
                callback_data=f"fsm_edit_choose_package:{package.name}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_MANAGE_CHANGE_STATUS,
                callback_data=f'fsm_edit:change_status'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_MANAGE_SHOW_PICTURES,
                callback_data=f'fsm_edit:show_pictures'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_MANAGE_ADD_NEW_PICTURE,
                callback_data=f'fsm_edit:add_new_picture'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='fsm_edit:back'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='fsm_edit:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_package_change_status_keyboard(language_code: str,
                                                               current_status: FaceSwapPackageStatus) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_PUBLIC + (
                    " ✅" if current_status == FaceSwapPackageStatus.PUBLIC else ""
                ),
                callback_data=f'fsm_edit_package_change_status:{FaceSwapPackageStatus.PUBLIC}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_PRIVATE + (
                    " ✅" if current_status == FaceSwapPackageStatus.PRIVATE else ""
                ),
                callback_data=f'fsm_edit_package_change_status:{FaceSwapPackageStatus.PRIVATE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='fsm_edit_package_change_status:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_picture_keyboard(language_code: str, file_name: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_MANAGE_CHANGE_STATUS,
                callback_data=f'fsm_edit_picture:change_status:{file_name}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_MANAGE_EXAMPLE_PICTURE,
                callback_data=f'fsm_edit_picture:example_picture:{file_name}'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_manage_face_swap_edit_picture_change_status_keyboard(language_code: str,
                                                               current_status: FaceSwapPackageStatus) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_PUBLIC + (
                    " ✅" if current_status == FaceSwapPackageStatus.PUBLIC else ""
                ),
                callback_data=f'fsm_edit_picture_change_status:{FaceSwapPackageStatus.PUBLIC}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_PRIVATE + (
                    " ✅" if current_status == FaceSwapPackageStatus.PRIVATE else ""
                ),
                callback_data=f'fsm_edit_picture_change_status:{FaceSwapPackageStatus.PRIVATE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='fsm_edit_picture_change_status:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
