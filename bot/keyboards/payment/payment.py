from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.common import PaymentType, PaymentMethod
from bot.database.models.package import Package, PackageType
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod
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
    emojis = Subscription.get_emojis()
    buttons = [
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.MINI} {emojis[SubscriptionType.MINI]}',
                callback_data=f'subscription:{SubscriptionType.MINI}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}',
                callback_data=f'subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}',
                callback_data=f'subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.PREMIUM} {emojis[SubscriptionType.PREMIUM]}',
                callback_data=f'subscription:{SubscriptionType.PREMIUM}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{SubscriptionType.UNLIMITED} {emojis[SubscriptionType.UNLIMITED]}',
                callback_data=f'subscription:{SubscriptionType.UNLIMITED}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_CURRENCY,
                callback_data=f'subscription:change_currency'
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
    discount_month_1 = f'{get_localization(language_code).DISCOUNT} {discount}%' \
        if discount > 0 else get_localization(language_code).NO_DISCOUNT
    discount_months_3 = f'{get_localization(language_code).DISCOUNT} {discount}%' \
        if discount > 5 else f'{get_localization(language_code).DISCOUNT} 5%'
    discount_months_6 = f'{get_localization(language_code).DISCOUNT} {discount}%' \
        if discount > 10 else f'{get_localization(language_code).DISCOUNT} 10%'
    discount_months_12 = f'{get_localization(language_code).DISCOUNT} {discount}%' \
        if discount > 20 else f'{get_localization(language_code).DISCOUNT} 20%'

    buttons = [
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTH_1} ({discount_month_1})',
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTH1}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_3} ({discount_months_3})',
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_6} ({discount_months_6})',
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS6}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).MONTHS_12} ({discount_months_12})',
                callback_data=f'period_of_subscription:{subscription_type}:{SubscriptionPeriod.MONTHS12}'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_payment_method_for_subscription_keyboard(
    language_code: str,
    subscription_type: SubscriptionType,
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).YOOKASSA_PAYMENT_METHOD}',
                callback_data=f'pms:{PaymentMethod.YOOKASSA}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).PAY_SELECTION_PAYMENT_METHOD}',
                callback_data=f'pms:{PaymentMethod.PAY_SELECTION}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).TELEGRAM_STARS_PAYMENT_METHOD}',
                callback_data=f'pms:{PaymentMethod.TELEGRAM_STARS}:{subscription_type}'
            ),
        ],
        # [
        #     InlineKeyboardButton(
        #         text=f'{get_localization(language_code).CRYPTO_PAYMENT_METHOD}',
        #         callback_data=f'pms:{PaymentMethod.CRYPTO}:{subscription_type}'
        #     ),
        # ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='pms:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_payment_keyboard(language_code: str, payment_link: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PROCEED_TO_PAY,
                url=payment_link,
                callback_data=f'payment:pay'
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_cancel_subscription_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).APPROVE,
                callback_data=f'cancel_subscription:approve'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CANCEL,
                callback_data=f'cancel_subscription:cancel'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_packages_keyboard(language_code: str, page=0) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOPPING_CART,
                callback_data='package:cart'
            )
        ],
    ]

    if page == 0:
        buttons.append([
            InlineKeyboardButton(
                text=get_localization(language_code).TEXT_MODELS,
                callback_data='package:text',
            ),
        ])
        for package_type in PackageType.get_class_attributes_in_order():
            if package_type in {
                PackageType.CHAT_GPT4_OMNI_MINI,
                PackageType.CHAT_GPT4_OMNI,
                PackageType.CLAUDE_3_SONNET,
                PackageType.CLAUDE_3_OPUS,
                PackageType.GEMINI_1_FLASH,
                PackageType.GEMINI_1_PRO,
                PackageType.CHAT,
                PackageType.ACCESS_TO_CATALOG,
            }:
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
                    text='⬅️',
                    callback_data='package:prev:3'
                ),
                InlineKeyboardButton(
                    text='1/4',
                    callback_data='package:page:0'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='package:next:1'
                ),
            ]
        )
    elif page == 1:
        buttons.append([
            InlineKeyboardButton(
                text=get_localization(language_code).IMAGE_MODELS,
                callback_data='package:text',
            ),
        ])
        for package_type in PackageType.get_class_attributes_in_order():
            if package_type in {
                PackageType.DALL_E,
                PackageType.MIDJOURNEY,
                PackageType.STABLE_DIFFUSION,
                PackageType.FACE_SWAP,
            }:
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
                    text='⬅️',
                    callback_data='package:prev:0'
                ),
                InlineKeyboardButton(
                    text='2/4',
                    callback_data='package:page:1'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='package:next:2'
                ),
            ]
        )
    elif page == 2:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).MUSIC_MODELS,
                    callback_data='package:text',
                ),
            ],
        )
        for package_type in PackageType.get_class_attributes_in_order():
            if package_type in {
                PackageType.MUSIC_GEN,
                PackageType.SUNO,
            }:
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
                    text='⬅️',
                    callback_data='package:prev:1'
                ),
                InlineKeyboardButton(
                    text='3/4',
                    callback_data='package:page:2'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='package:next:3'
                ),
            ]
        )
    elif page == 3:
        for package_type in PackageType.get_class_attributes_in_order():
            if package_type in {
                PackageType.VOICE_MESSAGES,
                PackageType.FAST_MESSAGES,
            }:
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
                    text='⬅️',
                    callback_data='package:prev:2'
                ),
                InlineKeyboardButton(
                    text='4/4',
                    callback_data='package:page:3'
                ),
                InlineKeyboardButton(
                    text='➡️',
                    callback_data='package:next:0'
                ),
            ]
        )

    buttons.extend(
        [
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).CHANGE_CURRENCY,
                    callback_data=f'package:change_currency:{page}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_localization(language_code).BACK,
                    callback_data='package:back'
                )
            ],
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
                text=get_localization(language_code).CHANGE_CURRENCY,
                callback_data=f'package_cart:change_currency'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='package_cart:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_payment_method_for_package_keyboard(
    language_code: str,
    package_type: PackageType,
    package_quantity: int,
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).YOOKASSA_PAYMENT_METHOD}',
                callback_data=f'pmp:{PaymentMethod.YOOKASSA}:{package_type}:{package_quantity}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).PAY_SELECTION_PAYMENT_METHOD}',
                callback_data=f'pmp:{PaymentMethod.PAY_SELECTION}:{package_type}:{package_quantity}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).TELEGRAM_STARS_PAYMENT_METHOD}',
                callback_data=f'pmp:{PaymentMethod.TELEGRAM_STARS}:{package_type}:{package_quantity}'
            ),
        ],
        # [
        #     InlineKeyboardButton(
        #         text=f'{get_localization(language_code).CRYPTO_PAYMENT_METHOD}',
        #         callback_data=f'pmp:{PaymentMethod.CRYPTO}:{package_type}:{package_quantity}'
        #     ),
        # ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='pmp:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_payment_method_for_cart_keyboard(language_code: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).YOOKASSA_PAYMENT_METHOD}',
                callback_data=f'pmc:{PaymentMethod.YOOKASSA}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).PAY_SELECTION_PAYMENT_METHOD}',
                callback_data=f'pmc:{PaymentMethod.PAY_SELECTION}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f'{get_localization(language_code).TELEGRAM_STARS_PAYMENT_METHOD}',
                callback_data=f'pmc:{PaymentMethod.TELEGRAM_STARS}'
            ),
        ],
        # [
        #     InlineKeyboardButton(
        #         text=f'{get_localization(language_code).CRYPTO_PAYMENT_METHOD}',
        #         callback_data=f'pmc:{PaymentMethod.CRYPTO}'
        #     ),
        # ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).BACK,
                callback_data='pmc:back'
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
