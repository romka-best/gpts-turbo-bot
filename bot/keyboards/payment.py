from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.package import PackageType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod
from bot.locales.main import get_localization


def build_subscriptions_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.STANDARD} ⭐",
                callback_data=f'subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.VIP} 🔥",
                callback_data=f'subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.PLATINUM} 💎",
                callback_data=f'subscription:{SubscriptionType.PLATINUM}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='subscription:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_period_of_subscription_keyboard(language_code: str,
                                          subscription_type: SubscriptionType) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1} ({get_localization(language_code).NO_DISCOUNT})",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTH1}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3} ({get_localization(language_code).DISCOUNT} 5%)",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6} ({get_localization(language_code).DISCOUNT} 10%)",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS6}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='period_of_subscription:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT3_REQUESTS,
                callback_data=f'package:{PackageType.GPT3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT4_REQUESTS,
                callback_data=f'package:{PackageType.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).THEMATIC_CHATS,
                callback_data=f'package:{PackageType.CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3_REQUESTS,
                callback_data=f'package:{PackageType.DALLE3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_REQUESTS,
                callback_data=f'package:{PackageType.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACCESS_TO_CATALOG,
                callback_data=f'package:{PackageType.ACCESS_TO_CATALOG}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES,
                callback_data=f'package:{PackageType.VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FAST_ANSWERS,
                callback_data=f'package:{PackageType.FAST_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLOSE,
                callback_data='package:close'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_quantity_of_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='quantity_of_package:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
