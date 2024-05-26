from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import PaymentType
from bot.database.models.package import Package, PackageType
from bot.database.models.subscription import SubscriptionType, SubscriptionPeriod
from bot.locales.main import get_localization


def build_buy_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SUBSCRIPTION,
                callback_data=f'buy:{PaymentType.SUBSCRIPTION}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PACKAGES,
                callback_data=f'buy:{PaymentType.PACKAGE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PROMO_CODE_ACTIVATE,
                callback_data=f'buy:promo_code'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
                text=f"{SubscriptionType.PREMIUM} 💎",
                callback_data=f'subscription:{SubscriptionType.PREMIUM}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='subscription:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_period_of_subscription_keyboard(
    language_code: str,
    subscription_type: SubscriptionType,
    discount: int,
) -> InlineKeyboardMarkup:
    discount_month_1 = f"{get_localization(language_code).DISCOUNT} {discount}%" \
        if discount > 0 else get_localization(language_code).NO_DISCOUNT
    discount_months_3 = f"{get_localization(language_code).DISCOUNT} {discount}%" \
        if discount > 5 else f"{get_localization(language_code).DISCOUNT} 5%"
    discount_months_6 = f"{get_localization(language_code).DISCOUNT} {discount}%" \
        if discount > 10 else f"{get_localization(language_code).DISCOUNT} 10%"
    discount_months_12 = f"{get_localization(language_code).DISCOUNT} {discount}%" \
        if discount > 20 else f"{get_localization(language_code).DISCOUNT} 20%"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1} ({discount_month_1})",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTH1}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3} ({discount_months_3})",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6} ({discount_months_6})",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS6}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_12} ({discount_months_12})",
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS12}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOPPING_CART,
                callback_data='package:cart'
            )
        ],
    ]

    for package_type in PackageType.get_class_attributes_in_order():
        buttons.append(
            [
                InlineKeyboardButton(
                    text=Package.get_translate_name_and_description(
                        get_localization(language_code),
                        package_type,
                    ).get('name'),
                    callback_data=f'package:{package_type}'
                ),
            ],
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='package:back'
            )
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_package_selection_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='package_selection:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_package_quantity_sent_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ADD_TO_CART,
                callback_data='package_quantity_sent:add_to_cart'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BUY_NOW,
                callback_data='package_quantity_sent:buy_now'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_package_add_to_cart_selection_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GO_TO_CART,
                callback_data='package_add_to_cart_selection:go_to_cart'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTINUE_SHOPPING,
                callback_data='package_add_to_cart_selection:continue_shopping'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_package_cart_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PROCEED_TO_CHECKOUT,
                callback_data='package_cart:proceed_to_checkout'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CLEAR_CART,
                callback_data='package_cart:clear'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='package_cart:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_package_proceed_to_checkout_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='package_proceed_to_checkout:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
