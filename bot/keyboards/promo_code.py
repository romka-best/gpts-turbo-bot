from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.promo_code import PromoCodeType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod
from bot.locales.main import get_localization


def build_promo_code_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='promo_code:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SUBSCRIPTION,
                callback_data=f'create_promo_code:{PromoCodeType.SUBSCRIPTION}'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_subscription_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.STANDARD} ⭐",
                callback_data=f'create_promo_code_subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.VIP} 🔥",
                callback_data=f'create_promo_code_subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.PLATINUM} 💎",
                callback_data=f'create_promo_code_subscription:{SubscriptionType.PLATINUM}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_subscription:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_period_of_subscription_keyboard(language_code: str,
                                                            subscription_type: SubscriptionType) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1}",
                callback_data=f'create_promo_code_period_of_subscription:{SubscriptionPeriod.MONTH1}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3}",
                callback_data=f'create_promo_code_period_of_subscription:{SubscriptionPeriod.MONTHS3}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6}",
                callback_data=f'create_promo_code_period_of_subscription:{SubscriptionPeriod.MONTHS6}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_period_of_subscription:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_name_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_name:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_date_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_date:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
