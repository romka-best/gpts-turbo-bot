from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.product import Product
from bot.database.models.promo_code import PromoCodeType
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod
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
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data=f'create_promo_code:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_create_promo_code_subscription_keyboard(language_code: str) -> InlineKeyboardMarkup:
    emojis = Subscription.get_emojis()

    buttons = [
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.MINI} {emojis[SubscriptionType.MINI]}',
                callback_data=f'create_promo_code_subscription:{SubscriptionType.MINI}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}',
                callback_data=f'create_promo_code_subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}',
                callback_data=f'create_promo_code_subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.PREMIUM} {emojis[SubscriptionType.PREMIUM]}',
                callback_data=f'create_promo_code_subscription:{SubscriptionType.PREMIUM}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.UNLIMITED} {emojis[SubscriptionType.UNLIMITED]}',
                callback_data=f'create_promo_code_subscription:{SubscriptionType.UNLIMITED}'
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
                text=f'{get_localization(language_code).MONTH_1}',
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTH1}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_3}',
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_6}',
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS6}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_12}',
                callback_data=f'create_promo_code_period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS12}'
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


def build_create_promo_code_package_keyboard(language_code: str, products: list[Product]):
    buttons = []
    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=product.names.get(language_code),
                    callback_data=f'create_promo_code_package:{product.id}'
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
                text=f'5%',
                callback_data=f'create_promo_code_discount:5'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'10%',
                callback_data=f'create_promo_code_discount:10'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'20%',
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
