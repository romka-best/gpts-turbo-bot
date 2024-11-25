import random
from typing import Optional

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import Model
from bot.database.models.face_swap_package import FaceSwapPackageStatus
from bot.database.models.generation import GenerationReaction
from bot.database.models.user import UserGender
from bot.database.operations.face_swap_package.getters import get_face_swap_packages_by_gender
from bot.locales.main import get_localization


def build_start_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).START_QUICK_GUIDE,
                callback_data='start:quick_guide'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).START_ADDITIONAL_FEATURES,
                callback_data='start:additional_features'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_start_chosen_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='start:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def build_recommendations_keyboard(
    current_model: Model,
    language_code: str,
    gender: Optional[UserGender] = UserGender.UNSPECIFIED,
) -> ReplyKeyboardMarkup:
    buttons = []
    if current_model == Model.CHAT_GPT or current_model == Model.CLAUDE or current_model == Model.GEMINI:
        recommendations = get_localization(language_code).requests_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif (
        current_model == Model.DALL_E or
        current_model == Model.MIDJOURNEY or
        current_model == Model.STABLE_DIFFUSION or
        current_model == Model.FLUX
    ):
        recommendations = get_localization(language_code).image_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])
    elif current_model == Model.FACE_SWAP:
        face_swap_packages = await get_face_swap_packages_by_gender(
            gender,
            status=FaceSwapPackageStatus.PUBLIC,
        )
        for face_swap_package in face_swap_packages:
            buttons.append(
                [
                    KeyboardButton(
                        text=face_swap_package.translated_names.get(language_code, face_swap_package.name),
                    )
                ],
            )
    elif current_model == Model.PHOTOSHOP_AI:
        for photoshop_ai_action in get_localization(language_code).photoshop_ai_actions():
            buttons.append(
                [
                    KeyboardButton(
                        text=photoshop_ai_action,
                    )
                ],
            )
    elif current_model == Model.MUSIC_GEN or current_model == Model.SUNO:
        recommendations = get_localization(language_code).music_recommendations()
        random.shuffle(recommendations)
        for recommendation in recommendations[:4]:
            buttons.append([
                KeyboardButton(
                    text=recommendation,
                )
            ])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def build_continue_generating_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTINUE_GENERATING,
                callback_data='continue_generation:continue'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_reaction_keyboard(generation_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='👍',
                callback_data=f'reaction:{GenerationReaction.LIKED}:{generation_id}'
            ),
            InlineKeyboardButton(
                text='👎',
                callback_data=f'reaction:{GenerationReaction.DISLIKED}:{generation_id}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_limit_exceeded_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_AI_MODEL,
                callback_data='limit_exceeded:change_ai_model'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BONUS_INFO,
                callback_data='limit_exceeded:open_bonus_info'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_SUBSCRIPTIONS_INFO,
                callback_data='limit_exceeded:open_buy_subscriptions_info'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_PACKAGES_INFO,
                callback_data='limit_exceeded:open_buy_packages_info'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_time_limit_exceeded_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).REMOVE_RESTRICTION,
                callback_data='time_limit_exceeded:remove_restriction'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_time_limit_exceeded_chosen_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BONUS_INFO,
                callback_data='limit_exceeded:open_bonus_info'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_SUBSCRIPTIONS_INFO,
                callback_data='limit_exceeded:open_buy_subscriptions_info'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).OPEN_BUY_PACKAGES_INFO,
                callback_data='limit_exceeded:open_buy_packages_info'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_cancel_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='common:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_error_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TECH_SUPPORT,
                url='https://t.me/roman_danilov',
                callback_data='error:tech_support'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
