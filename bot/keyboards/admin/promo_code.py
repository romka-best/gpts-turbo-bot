from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.package import Package, PackageType
from bot.database.models.promo_code import PromoCodeType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod
from bot.locales.main import get_localization


def build_create_promo_code_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SUBSCRIPTION,
                callback_data=f'create_promo_code:{PromoCodeType.SUBSCRIPTION}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PACKAGE,
                callback_data=f'create_promo_code:{PromoCodeType.PACKAGE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DISCOUNT,
                callback_data=f'create_promo_code:{PromoCodeType.DISCOUNT}'
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


def build_create_promo_code_period_of_subscription_keyboard(
    language_code: str,
    subscription_type: SubscriptionType,
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1}",
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTH1}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3}",
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6}",
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS6}'
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


def build_create_promo_code_package_keyboard(language_code: str):
    buttons = []
    for package_type in PackageType.get_class_attributes_in_order():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=Package.get_translate_name_and_description(
                        get_localization(language_code),
                        package_type,
                    ).get('name'),
                    callback_data=f'create_promo_code_package:{package_type}'
                ),
            ],
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_package:cancel'
            )
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_discount_keyboard(language_code: str):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"5%",
                callback_data=f'create_promo_code_discount:5'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"10%",
                callback_data=f'create_promo_code_discount:10'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"20%",
                callback_data=f'create_promo_code_discount:20'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data='create_promo_code_discount:cancel'
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
