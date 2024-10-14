import logging
from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile, LabeledPrice, PreCheckoutQuery

from bot.database.main import firebase
from bot.database.models.cart import CartItem
from bot.database.models.common import PaymentType, PaymentMethod, Currency
from bot.database.models.package import PackageStatus, PackageType, Package
from bot.database.models.subscription import (
    Subscription,
    SubscriptionStatus,
    SubscriptionType,
    SubscriptionPeriod,
)
from bot.database.models.transaction import TransactionType
from bot.database.models.user import UserSettings
from bot.database.operations.cart.getters import get_cart_by_user_id
from bot.database.operations.cart.updaters import update_cart
from bot.database.operations.package.getters import (
    get_packages_by_user_id_and_status,
    get_last_package_with_waiting_payment,
)
from bot.database.operations.package.updaters import update_package
from bot.database.operations.package.writers import write_package
from bot.database.operations.subscription.getters import (
    get_last_subscription_by_user_id,
    get_last_subscription_with_waiting_payment,
)
from bot.database.operations.subscription.updaters import update_subscription
from bot.database.operations.subscription.writers import write_subscription
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.payment.promo_code_handler import handle_promo_code
from bot.helpers.billing.create_payment import create_payment
from bot.helpers.creaters.create_package import create_package
from bot.helpers.creaters.create_subscription import create_subscription
from bot.helpers.getters.get_user_discount import get_user_discount
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.keyboards.ai.mode import build_switched_to_ai_keyboard
from bot.keyboards.payment.payment import (
    build_buy_keyboard,
    build_subscriptions_keyboard,
    build_payment_method_for_subscription_keyboard,
    build_packages_keyboard,
    build_package_selection_keyboard,
    build_package_quantity_sent_keyboard,
    build_package_cart_keyboard,
    build_package_add_to_cart_selection_keyboard,
    build_cancel_subscription_keyboard,
    build_payment_keyboard,
    build_payment_method_for_package_keyboard,
    build_payment_method_for_cart_keyboard, build_period_of_subscription_keyboard,
)
from bot.locales.main import get_localization, get_user_language
from bot.states.payment import Payment

payment_router = Router()


async def handle_buy(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(user_id, state.storage)

    reply_keyboard = build_buy_keyboard(user_language_code)
    text = get_localization(user_language_code).BUY
    await message.answer(
        text=text,
        reply_markup=reply_keyboard,
    )


@payment_router.message(Command('buy'))
async def buy(message: Message, state: FSMContext):
    await state.clear()

    await handle_buy(message, str(message.from_user.id), state)


@payment_router.callback_query(lambda c: c.data.startswith('buy:'))
async def handle_buy_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    payment_type = callback_query.data.split(':')[1]
    if payment_type == PaymentType.PACKAGE:
        await handle_package(callback_query.message, user_id, state)
    elif payment_type == PaymentType.SUBSCRIPTION:
        await handle_subscribe(callback_query.message, user_id, state)
    elif payment_type == 'promo_code':
        await handle_promo_code(callback_query.message, str(callback_query.from_user.id), state)

    await callback_query.message.delete()


async def handle_subscribe(message: Message, user_id: str, state: FSMContext):
    user = await get_user(str(user_id))
    user_language_code = await get_user_language(str(user_id), state.storage)

    photo_path = f'payments/subscriptions_{user_language_code}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    min_prices = {
        SubscriptionType.MINI: Subscription.get_price(
            user.currency,
            SubscriptionType.MINI,
            SubscriptionPeriod.MONTH1,
            user.discount,
        ),
        SubscriptionType.STANDARD: Subscription.get_price(
            user.currency,
            SubscriptionType.STANDARD,
            SubscriptionPeriod.MONTH1,
            user.discount,
        ),
        SubscriptionType.VIP: Subscription.get_price(
            user.currency,
            SubscriptionType.VIP,
            SubscriptionPeriod.MONTH1,
            user.discount,
        ),
        SubscriptionType.PREMIUM: Subscription.get_price(
            user.currency,
            SubscriptionType.PREMIUM,
            SubscriptionPeriod.MONTH1,
            user.discount,
        ),
        SubscriptionType.UNLIMITED: Subscription.get_price(
            user.currency,
            SubscriptionType.UNLIMITED,
            SubscriptionPeriod.MONTH1,
            user.discount,
        ),
    }

    text = get_localization(user_language_code).subscribe(user.currency, min_prices)
    reply_markup = build_subscriptions_keyboard(user_language_code)
    await message.answer_photo(
        photo=URLInputFile(photo_link, filename=photo_path),
        caption=text,
        reply_markup=reply_markup,
    )


@payment_router.callback_query(lambda c: c.data.startswith('subscription:'))
async def handle_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    subscription_type = callback_query.data.split(':')[1]
    if subscription_type == 'back':
        await handle_buy(callback_query.message, user_id, state)
        await callback_query.message.delete()
    elif subscription_type == 'change_currency':
        user = await get_user(user_id)
        user_language_code = await get_user_language(user_id, state.storage)

        if user.currency == Currency.RUB:
            user.currency = Currency.USD
        elif user.currency == Currency.USD:
            user.currency = Currency.XTR
        else:
            user.currency = Currency.RUB
        await update_user(
            user_id,
            {
                'currency': user.currency,
            }
        )

        min_prices = {
            SubscriptionType.MINI: Subscription.get_price(
                user.currency,
                SubscriptionType.MINI,
                SubscriptionPeriod.MONTH1,
                user.discount,
            ),
            SubscriptionType.STANDARD: Subscription.get_price(
                user.currency,
                SubscriptionType.STANDARD,
                SubscriptionPeriod.MONTH1,
                user.discount,
            ),
            SubscriptionType.VIP: Subscription.get_price(
                user.currency,
                SubscriptionType.VIP,
                SubscriptionPeriod.MONTH1,
                user.discount,
            ),
            SubscriptionType.PREMIUM: Subscription.get_price(
                user.currency,
                SubscriptionType.PREMIUM,
                SubscriptionPeriod.MONTH1,
                user.discount,
            ),
            SubscriptionType.UNLIMITED: Subscription.get_price(
                user.currency,
                SubscriptionType.UNLIMITED,
                SubscriptionPeriod.MONTH1,
                user.discount,
            ),
        }

        text = get_localization(user_language_code).subscribe(user.currency, min_prices)
        reply_markup = build_subscriptions_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=text,
            reply_markup=reply_markup,
        )
    else:
        user_language_code = await get_user_language(user_id, state.storage)

        caption = get_localization(user_language_code).CHOOSE_PAYMENT_METHOD
        reply_markup = build_payment_method_for_subscription_keyboard(user_language_code, subscription_type)
        photo_path = f'payments/subscription_{subscription_type.lower()}_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=caption,
            reply_markup=reply_markup,
        )
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('pms:'))
async def handle_payment_method_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    payment_method = callback_query.data.split(':')[1]
    if payment_method == 'back':
        await handle_subscribe(callback_query.message, user_id, state)
        await callback_query.message.delete()
    else:
        user = await get_user(user_id)
        user_language_code = await get_user_language(user_id, state.storage)
        subscription_type = callback_query.data.split(':')[2]

        if payment_method == PaymentMethod.YOOKASSA:
            amount = float(
                Subscription.get_price(
                    Currency.RUB,
                    subscription_type,
                    SubscriptionPeriod.MONTH1,
                    user.discount,
                )
            )
            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_subscription(user_id, subscription_type),
                amount,
                user_language_code,
                True,
            )

            caption = get_localization(user_language_code).confirmation_subscribe(
                subscription_type,
                Currency.RUB,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('confirmation').get('confirmation_url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            await write_subscription(
                None,
                user_id,
                subscription_type,
                SubscriptionPeriod.MONTH1,
                SubscriptionStatus.WAITING,
                Currency.RUB,
                amount,
                0,
                payment_method,
                payment.get('id'),
            )
        elif payment_method == PaymentMethod.PAY_SELECTION:
            amount = float(
                Subscription.get_price(
                    Currency.USD,
                    subscription_type,
                    SubscriptionPeriod.MONTH1,
                    user.discount,
                )
            )
            subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document()
            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_subscription(user_id, subscription_type),
                amount,
                user_language_code,
                True,
                subscription_ref.id,
            )

            caption = get_localization(user_language_code).confirmation_subscribe(
                subscription_type,
                Currency.USD,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('Url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            await write_subscription(
                subscription_ref.id,
                user_id,
                subscription_type,
                SubscriptionPeriod.MONTH1,
                SubscriptionStatus.WAITING,
                Currency.USD,
                amount,
                0,
                payment_method,
                payment.get('Id'),
            )
        elif payment_method == PaymentMethod.TELEGRAM_STARS:
            caption = get_localization(user_language_code).choose_how_many_months_to_subscribe(subscription_type)
            reply_markup = build_period_of_subscription_keyboard(
                user_language_code,
                subscription_type,
                user.discount,
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )
        else:
            raise NotImplementedError(f'Payment method is not recognized: {payment_method}')


@payment_router.callback_query(lambda c: c.data.startswith('period_of_subscription:'))
async def handle_period_of_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    subscription_type, subscription_period = callback_query.data.split(':')[1], callback_query.data.split(':')[2]
    emojis = Subscription.get_emojis()
    price_with_discount = Subscription.get_price(
        Currency.XTR,
        subscription_type,
        subscription_period,
        user.discount,
    )
    name = (f'{subscription_type} {emojis[subscription_type]} '
            f'({get_localization(user_language_code).cycles_subscribe()[subscription_period]})')
    description = get_localization(user_language_code).confirmation_subscribe(
        subscription_type,
        Currency.XTR,
        price_with_discount,
    )
    photo_path = f'payments/subscription_{subscription_type.lower()}_{user_language_code}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    await callback_query.message.reply_invoice(
        title=name,
        description=description,
        payload=f'{PaymentType.SUBSCRIPTION}:{callback_query.from_user.id}:{subscription_type}:{subscription_period}',
        provider_token='',
        currency=Currency.XTR,
        prices=[LabeledPrice(label=name, amount=int(float(price_with_discount)))],
        photo_url=photo_link,
        photo_width=1024,
        photo_height=768,
    )

    await callback_query.message.delete()


async def handle_package(message: Message, user_id: str, state: FSMContext, is_edit=False, page=0):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    photo_path = f'payments/packages_{user.subscription_type.lower()}_{user_language_code}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user_language_code).package(user.currency, page)
    reply_markup = build_packages_keyboard(user_language_code, page)

    if is_edit:
        await message.edit_caption(
            caption=text,
            reply_markup=reply_markup,
        )
    else:
        await message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=text,
            reply_markup=reply_markup,
        )


@payment_router.callback_query(lambda c: c.data.startswith('package:'))
async def handle_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    package_type = callback_query.data.split(':')[1]
    if package_type == 'text' or package_type == 'page':
        return
    elif package_type == 'next' or package_type == 'prev':
        page = int(callback_query.data.split(':')[2])
        await handle_package(callback_query.message, str(callback_query.from_user.id), state, True, page)

        return
    elif package_type == 'change_currency':
        if user.currency == Currency.RUB:
            user.currency = Currency.USD
        elif user.currency == Currency.USD:
            user.currency = Currency.XTR
        else:
            user.currency = Currency.RUB
        await update_user(
            user_id,
            {
                'currency': user.currency,
            }
        )

        page = int(callback_query.data.split(':')[2])
        await handle_package(callback_query.message, str(callback_query.from_user.id), state, True, page)
    elif package_type == 'back':
        await handle_buy(callback_query.message, user_id, state)
        await callback_query.message.delete()
    elif package_type == 'cart':
        cart = await get_cart_by_user_id(user_id)

        discount = 0
        if user.currency != Currency.XTR:
            discount = get_user_discount(user.discount, user.subscription_type)
        message = get_localization(user_language_code).shopping_cart(
            user.currency,
            cart.items,
            discount,
        )
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    else:
        message = get_localization(user_language_code).choose_min(package_type)
        reply_markup = build_package_selection_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

        await state.update_data(package_type=package_type)
        await state.set_state(Payment.waiting_for_package_quantity)


@payment_router.callback_query(lambda c: c.data.startswith('package_selection:'))
async def handle_package_selection_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    await handle_package(callback_query.message, user_id, state)
    await callback_query.message.delete()


@payment_router.message(Payment.waiting_for_package_quantity, ~F.text.startswith('/'))
async def quantity_of_package_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        quantity = int(message.text)

        photo_path = f'payments/packages_{user.subscription_type.lower()}_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        reply_markup = build_package_quantity_sent_keyboard(user_language_code)
        await message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=get_localization(user_language_code).ADD_TO_CART_OR_BUY_NOW,
            reply_markup=reply_markup,
        )

        await state.update_data(package_quantity=quantity)
    except (TypeError, ValueError):
        reply_markup = build_package_selection_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )


@payment_router.callback_query(lambda c: c.data.startswith('package_quantity_sent:'))
async def handle_package_quantity_sent_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)
    user_data = await state.get_data()

    package_type = user_data['package_type']
    package_quantity = user_data['package_quantity']

    action = callback_query.data.split(':')[1]
    if action == 'add_to_cart':
        cart = await get_cart_by_user_id(user_id)
        is_already_in_cart = False
        for index, cart_item in enumerate(cart.items):
            if cart_item.get('package_type') == package_type:
                is_already_in_cart = True
                cart.items[index]['quantity'] = cart_item.get('quantity', 0) + package_quantity
                break
        if not is_already_in_cart:
            cart.items.append(CartItem(package_type, package_quantity).to_dict())

        await update_cart(cart.id, {
            'items': cart.items,
        })

        reply_markup = build_package_add_to_cart_selection_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).GO_TO_CART_OR_CONTINUE_SHOPPING,
            reply_markup=reply_markup,
        )
    elif action == 'buy_now':
        reply_markup = build_payment_method_for_package_keyboard(user_language_code, package_type, package_quantity)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).CHOOSE_PAYMENT_METHOD,
            reply_markup=reply_markup,
        )


@payment_router.callback_query(lambda c: c.data.startswith('package_add_to_cart_selection:'))
async def handle_package_add_to_cart_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'go_to_cart':
        cart = await get_cart_by_user_id(user_id)

        photo_path = f'payments/packages_{user.subscription_type.lower()}_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        discount = 0
        if user.currency != Currency.XTR:
            discount = get_user_discount(user.discount, user.subscription_type)
        message = get_localization(user_language_code).shopping_cart(
            user.currency,
            cart.items,
            discount,
        )
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=message,
            reply_markup=reply_markup,
        )
        await callback_query.message.delete()
    elif action == 'continue_shopping':
        await handle_package(callback_query.message, user_id, state)
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('package_cart:'))
async def handle_package_cart_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == 'proceed_to_checkout':
        reply_markup = build_payment_method_for_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).CHOOSE_PAYMENT_METHOD,
            reply_markup=reply_markup,
        )
    elif action == 'clear':
        cart = await get_cart_by_user_id(user_id)
        if cart.items:
            cart.items = []
            await update_cart(cart.id, {
                'items': cart.items,
            })

            discount = 0
            if user.currency != Currency.XTR:
                discount = get_user_discount(user.discount, user.subscription_type)
            message = get_localization(user_language_code).shopping_cart(
                user.currency,
                cart.items,
                discount,
            )
            reply_markup = build_package_cart_keyboard(user_language_code)
            await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    elif action == 'change_currency':
        if user.currency == Currency.RUB:
            user.currency = Currency.USD
        elif user.currency == Currency.USD:
            user.currency = Currency.XTR
        else:
            user.currency = Currency.RUB
        await update_user(
            user_id,
            {
                'currency': user.currency,
            }
        )

        cart = await get_cart_by_user_id(user_id)

        discount = 0
        if user.currency != Currency.XTR:
            discount = get_user_discount(user.discount, user.subscription_type)
        message = get_localization(user_language_code).shopping_cart(
            user.currency,
            cart.items,
            discount,
        )
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    elif action == 'back':
        await handle_package(callback_query.message, user_id, state)
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('package_proceed_to_checkout:'))
async def handle_package_proceed_to_checkout_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    cart = await get_cart_by_user_id(user_id)

    discount = 0
    if user.currency != Currency.XTR:
        discount = get_user_discount(user.discount, user.subscription_type)
    message = get_localization(user_language_code).shopping_cart(
        user.currency,
        cart.items,
        discount,
    )
    reply_markup = build_package_cart_keyboard(user_language_code)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)


@payment_router.callback_query(lambda c: c.data.startswith('pmp:'))
async def handle_payment_method_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    payment_method = callback_query.data.split(':')[1]
    if payment_method == 'back':
        await handle_package(callback_query.message, user_id, state, True)
    else:
        user = await get_user(user_id)
        user_language_code = await get_user_language(user_id, state.storage)

        package_type, package_quantity = callback_query.data.split(':')[2], int(callback_query.data.split(':')[3])

        if payment_method == PaymentMethod.YOOKASSA:
            amount = Package.get_price(
                Currency.RUB,
                package_type,
                package_quantity,
                get_user_discount(user.discount, user.subscription_type),
            )

            package_name_and_description = Package.get_translate_name_and_description(
                get_localization(user_language_code),
                package_type,
            )
            package_name = package_name_and_description.get('name')
            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_package(
                    user_id,
                    package_name,
                    package_quantity,
                ),
                amount,
                user_language_code,
                False,
            )

            caption = get_localization(user_language_code).confirmation_package(
                package_name,
                package_quantity,
                Currency.RUB,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('confirmation').get('confirmation_url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            until_at = None
            if (
                package_type == PackageType.VOICE_MESSAGES or
                package_type == PackageType.FAST_MESSAGES or
                package_type == PackageType.ACCESS_TO_CATALOG
            ):
                current_date = datetime.now(timezone.utc)
                until_at = current_date + timedelta(days=30 * int(package_quantity))
            await write_package(
                None,
                user_id,
                package_type,
                PackageStatus.WAITING,
                Currency.RUB,
                amount,
                0,
                int(package_quantity),
                payment_method,
                payment.get('id'),
                until_at,
            )
        elif payment_method == PaymentMethod.PAY_SELECTION:
            amount = Package.get_price(
                Currency.USD,
                package_type,
                package_quantity,
                get_user_discount(user.discount, user.subscription_type),
            )

            package_name_and_description = Package.get_translate_name_and_description(
                get_localization(user_language_code),
                package_type,
            )
            package_name = package_name_and_description.get('name')

            package_ref = firebase.db.collection(Package.COLLECTION_NAME).document()
            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_package(
                    user_id,
                    package_name,
                    package_quantity,
                ),
                amount,
                user_language_code,
                False,
                package_ref.id,
            )

            caption = get_localization(user_language_code).confirmation_package(
                package_name,
                package_quantity,
                Currency.USD,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('Url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            until_at = None
            if (
                package_type == PackageType.VOICE_MESSAGES or
                package_type == PackageType.FAST_MESSAGES or
                package_type == PackageType.ACCESS_TO_CATALOG
            ):
                current_date = datetime.now(timezone.utc)
                until_at = current_date + timedelta(days=30 * int(package_quantity))
            await write_package(
                package_ref.id,
                user_id,
                package_type,
                PackageStatus.WAITING,
                Currency.USD,
                amount,
                0,
                int(package_quantity),
                payment_method,
                package_ref.id,
                until_at,
            )
        elif payment_method == PaymentMethod.TELEGRAM_STARS:
            amount = Package.get_price(Currency.XTR, package_type, package_quantity, 0)

            package_name_and_description = Package.get_translate_name_and_description(
                get_localization(user_language_code),
                package_type,
            )
            package_name = package_name_and_description.get('name')
            package_description = package_name_and_description.get('description')

            photo_path = f'payments/packages_{user.subscription_type.lower()}_{user_language_code}.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_link = firebase.get_public_url(photo.name)

            await callback_query.message.reply_invoice(
                title=f'{package_name} ({package_quantity})',
                description=package_description,
                payload=f'{PaymentType.PACKAGE}:{user.id}:{package_type}:{package_quantity}',
                provider_token='',
                currency=Currency.XTR,
                prices=[LabeledPrice(label=package_name, amount=int(amount))],
                photo_url=photo_link,
                photo_width=1024,
                photo_height=768,
            )

            await callback_query.message.delete()
            await state.clear()
        else:
            raise NotImplementedError


@payment_router.callback_query(lambda c: c.data.startswith('pmc:'))
async def handle_payment_method_cart_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    cart = await get_cart_by_user_id(user_id)

    payment_method = callback_query.data.split(':')[1]
    if payment_method == 'back':
        discount = 0
        if user.currency != Currency.XTR:
            get_user_discount(user.discount, user.subscription_type)
        message = get_localization(user_language_code).shopping_cart(
            user.currency,
            cart.items,
            discount,
        )
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    else:
        if payment_method == PaymentMethod.YOOKASSA:
            amount = 0
            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get('package_type'), cart_item.get('quantity', 0)

                amount += Package.get_price(
                    Currency.RUB,
                    package_type,
                    package_quantity,
                    get_user_discount(user.discount, user.subscription_type),
                )

            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_cart(user_id),
                amount,
                user_language_code,
                False,
            )

            caption = get_localization(user_language_code).confirmation_cart(
                cart.items,
                Currency.RUB,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('confirmation').get('confirmation_url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            packages_with_waiting_status = await get_packages_by_user_id_and_status(user_id, PackageStatus.WAITING)
            for package_with_waiting_status in packages_with_waiting_status:
                await update_package(package_with_waiting_status.id, {
                    'status': PackageStatus.CANCELED,
                })

            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get('package_type'), cart_item.get('quantity', 0)

                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * package_quantity)
                package_amount = Package.get_price(
                    Currency.RUB,
                    package_type,
                    package_quantity,
                    get_user_discount(user.discount, user.subscription_type),
                )
                await write_package(
                    None,
                    user_id,
                    package_type,
                    PackageStatus.WAITING,
                    Currency.RUB,
                    package_amount,
                    0,
                    int(package_quantity),
                    payment_method,
                    payment.get('id'),
                    until_at,
                )
        elif payment_method == PaymentMethod.PAY_SELECTION:
            amount = 0
            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get('package_type'), cart_item.get('quantity', 0)

                amount += Package.get_price(
                    Currency.USD,
                    package_type,
                    package_quantity,
                    get_user_discount(user.discount, user.subscription_type),
                )

            package_ref = firebase.db.collection(Package.COLLECTION_NAME).document()
            payment = await create_payment(
                payment_method,
                user_id,
                get_localization(user_language_code).payment_description_cart(user_id),
                amount,
                user_language_code,
                False,
                package_ref.id,
            )

            caption = get_localization(user_language_code).confirmation_cart(
                cart.items,
                Currency.USD,
                amount,
            )
            reply_markup = build_payment_keyboard(
                user_language_code,
                payment.get('Url'),
            )
            await callback_query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
            )

            packages_with_waiting_status = await get_packages_by_user_id_and_status(user_id, PackageStatus.WAITING)
            for package_with_waiting_status in packages_with_waiting_status:
                await update_package(package_with_waiting_status.id, {
                    'status': PackageStatus.CANCELED,
                })

            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get('package_type'), cart_item.get('quantity', 0)

                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * package_quantity)
                package_amount = Package.get_price(
                    Currency.USD,
                    package_type,
                    package_quantity,
                    get_user_discount(user.discount, user.subscription_type),
                )
                await write_package(
                    None,
                    user_id,
                    package_type,
                    PackageStatus.WAITING,
                    Currency.USD,
                    package_amount,
                    0,
                    int(package_quantity),
                    payment_method,
                    package_ref.id,
                    until_at,
                )
        elif payment_method == PaymentMethod.TELEGRAM_STARS:
            amount = 0
            payload = f'{PaymentType.CART}:{user.id}'
            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get('package_type'), cart_item.get('quantity', 0)

                amount += Package.get_price(Currency.XTR, package_type, package_quantity, 0)
                payload += f':{package_type}:{package_quantity}'

            photo_path = f'payments/packages_{user.subscription_type.lower()}_{user_language_code}.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_link = firebase.get_public_url(photo.name)

            await callback_query.message.reply_invoice(
                title=get_localization(user_language_code).PACKAGES,
                description=get_localization(user_language_code).SHOPPING_CART,
                payload=payload,
                provider_token='',
                currency=Currency.XTR,
                prices=[LabeledPrice(label=get_localization(user_language_code).SHOPPING_CART, amount=int(amount))],
                photo_url=photo_link,
                photo_width=1024,
                photo_height=768,
            )

            await callback_query.message.delete()
            await state.clear()
        else:
            raise NotImplementedError


@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    payment_type = pre_checkout_query.invoice_payload.split(':')[0]
    if payment_type == PaymentType.SUBSCRIPTION:
        _, user_id, subscription_type, subscription_period = pre_checkout_query.invoice_payload.split(':')
        try:
            await write_subscription(
                None,
                user_id,
                subscription_type,
                subscription_period,
                SubscriptionStatus.WAITING,
                pre_checkout_query.currency,
                pre_checkout_query.total_amount,
                0,
                PaymentMethod.TELEGRAM_STARS,
                None,
            )

            await pre_checkout_query.answer(ok=True)
        except Exception as e:
            logging.error(f'Error in payment_handler: {e}')

            await pre_checkout_query.answer(ok=False)

            await send_message_to_admins(
                bot=pre_checkout_query.bot,
                message=f'#payment #subscription #error\n\n'
                        f'🚫 Неизвестная ошибка в блоке оплаты у подписки:\n\n'
                        f'💱 Метод оплаты: {PaymentMethod.TELEGRAM_STARS}\n'
                        f'ℹ️ Информация:\n {e}\n\n'
                        f'@roman_danilov, посмотришь? 🤨',
                parse_mode=None,
            )
    elif payment_type == PaymentType.PACKAGE:
        _, user_id, package_type, quantity = pre_checkout_query.invoice_payload.split(':')
        try:
            until_at = None
            if (
                package_type == PackageType.VOICE_MESSAGES or
                package_type == PackageType.FAST_MESSAGES or
                package_type == PackageType.ACCESS_TO_CATALOG
            ):
                current_date = datetime.now(timezone.utc)
                until_at = current_date + timedelta(days=30 * int(quantity))
            await write_package(
                None,
                user_id,
                package_type,
                PackageStatus.WAITING,
                pre_checkout_query.currency,
                pre_checkout_query.total_amount,
                0,
                int(quantity),
                PaymentMethod.TELEGRAM_STARS,
                None,
                until_at,
            )
            await pre_checkout_query.answer(ok=True)
        except Exception as e:
            logging.error(f'Error in payment_handler: {e}')

            await pre_checkout_query.answer(ok=False)

            await send_message_to_admins(
                bot=pre_checkout_query.bot,
                message=f'#payment #package #error\n\n'
                        f'🚫 Неизвестная ошибка в блоке оплаты у пакета:\n\n'
                        f'💱 Метод оплаты: {PaymentMethod.TELEGRAM_STARS}\n'
                        f'ℹ️ Информация:\n {e}\n\n'
                        f'@roman_danilov, посмотришь? 🤨',
                parse_mode=None,
            )
    elif payment_type == PaymentType.CART:
        _, user_id, packages = pre_checkout_query.invoice_payload.split(':', 2)
        packages = packages.split(':')
        try:
            packages_with_waiting_status = await get_packages_by_user_id_and_status(user_id, PackageStatus.WAITING)
            for package_with_waiting_status in packages_with_waiting_status:
                await update_package(package_with_waiting_status.id, {
                    'status': PackageStatus.CANCELED,
                })

            for i in range(0, len(packages), 2):
                package_type, package_quantity = packages[i], int(packages[i + 1])
                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * package_quantity)
                package_amount = Package.get_price(pre_checkout_query.currency, package_type, package_quantity, 0)
                await write_package(
                    None,
                    user_id,
                    package_type,
                    PackageStatus.WAITING,
                    pre_checkout_query.currency,
                    package_amount,
                    0,
                    package_quantity,
                    PaymentMethod.TELEGRAM_STARS,
                    None,
                    until_at,
                )
            await pre_checkout_query.answer(ok=True)
        except Exception as e:
            logging.error(f'Error in payment_handler: {e}')

            await pre_checkout_query.answer(ok=False)

            await send_message_to_admins(
                bot=pre_checkout_query.bot,
                message=f'#payment #packages #error\n\n'
                        f'🚫 Неизвестная ошибка в блоке оплаты у пакетов:\n\n'
                        f'💱 Метод оплаты: {PaymentMethod.YOOKASSA}\n'
                        f'ℹ️ Информация:\n {e}\n\n'
                        f'@roman_danilov, посмотришь? 🤨',
                parse_mode=None,
            )
    else:
        await pre_checkout_query.answer(ok=False)


@payment_router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    payment = message.successful_payment
    payment_type = payment.invoice_payload.split(':')[0]
    if payment_type == PaymentType.SUBSCRIPTION:
        _, user_id, subscription_type, subscription_period = payment.invoice_payload.split(':')
        subscription = await get_last_subscription_with_waiting_payment(user_id, subscription_type, subscription_period)
        transaction = firebase.db.transaction()
        await create_subscription(
            transaction,
            message.bot,
            subscription.id,
            subscription.user_id,
            subscription.amount,
            payment.provider_payment_charge_id,
            '',
        )
        await write_transaction(
            user_id=user_id,
            type=TransactionType.INCOME,
            service=subscription.type,
            amount=subscription.amount,
            clear_amount=subscription.amount,
            currency=subscription.currency,
            quantity=1,
            details={
                'payment_method': PaymentMethod.TELEGRAM_STARS,
                'subscription_id': subscription.id,
                'provider_payment_charge_id': payment.provider_payment_charge_id,
                'provider_auto_payment_charge_id': '',
            },
        )
        await update_user(user_id, {
            'discount': 0,
        })

        await message.answer(
            text=get_localization(user_language_code).SUBSCRIPTION_SUCCESS,
        )
        await send_message_to_admins(
            bot=message.bot,
            message=f'#payment #subscription #success\n\n'
                    f'🤑 <b>Успешно оформлена подписка у пользователя: {subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {subscription.id}\n'
                    f'💱 Метод оплаты: {subscription.payment_method}\n'
                    f'💳 Тип подписки: {subscription.type}\n'
                    f'💰 Сумма: {subscription.amount}{Currency.SYMBOLS[subscription.currency]}\n\n'
                    f'Продолжаем в том же духе 💪',
        )
    elif payment_type == PaymentType.PACKAGE:
        _, user_id, package_type, package_quantity = payment.invoice_payload.split(':')
        package = await get_last_package_with_waiting_payment(user_id, package_type, int(package_quantity))

        transaction = firebase.db.transaction()
        await create_package(
            transaction,
            package.id,
            package.user_id,
            package.amount,
            payment.provider_payment_charge_id,
        )

        service_type, _ = Package.get_service_type_and_update_quota(package.type, user.additional_usage_quota, 0)
        await write_transaction(
            user_id=user_id,
            type=TransactionType.INCOME,
            service=service_type,
            amount=package.amount,
            clear_amount=package.amount,
            currency=package.currency,
            quantity=package.quantity,
            details={
                'payment_method': PaymentMethod.TELEGRAM_STARS,
                'package_id': package.id,
                'provider_payment_charge_id': payment.provider_payment_charge_id
            },
        )

        await message.answer(
            text=get_localization(user_language_code).PACKAGE_SUCCESS,
        )
        await send_message_to_admins(
            bot=message.bot,
            message=f'#payment #package #success\n\n'
                    f'🤑 <b>Успешно прошла оплата пакета у пользователя: {package.user_id}</b>\n\n'
                    f'ℹ️ ID: {package.id}\n'
                    f'💱 Метод оплаты: {package.payment_method}\n'
                    f'💳 Тип пакета: {package.type}\n'
                    f'🔢 Количество: {package.quantity}\n'
                    f'💰 Сумма: {package.amount}{Currency.SYMBOLS[package.currency]}\n\n'
                    f'Продолжаем в том же духе 💪',
        )
    elif payment_type == PaymentType.CART:
        user_id = payment.invoice_payload.split(':')[1]
        packages = await get_packages_by_user_id_and_status(user_id, PackageStatus.WAITING)

        transaction = firebase.db.transaction()
        for package in packages:
            await create_package(
                transaction,
                package.id,
                package.user_id,
                package.amount,
                payment.provider_payment_charge_id,
            )

            service_type, _ = Package.get_service_type_and_update_quota(package.type, user.additional_usage_quota, 0)
            await write_transaction(
                user_id=user_id,
                type=TransactionType.INCOME,
                service=service_type,
                amount=package.amount,
                clear_amount=package.amount,
                currency=package.currency,
                quantity=package.quantity,
                details={
                    'payment_method': PaymentMethod.TELEGRAM_STARS,
                    'package_id': package.id,
                    'provider_payment_charge_id': payment.provider_payment_charge_id
                },
            )

        cart = await get_cart_by_user_id(user_id)
        cart.items = []
        await update_cart(cart.id, {
            'items': cart.items,
        })

        await message.answer(
            text=get_localization(user_language_code).PACKAGES_SUCCESS,
        )
        await send_message_to_admins(
            bot=message.bot,
            message=f'#payment #packages #success\n\n'
                    f'🤑 <b>Успешно прошла оплата пакетов у пользователя: {user.id}</b>\n\n'
                    f'💱 Метод оплаты: {PaymentMethod.TELEGRAM_STARS}\n'
                    f'💰 Сумма: {payment.total_amount}{Currency.SYMBOLS[packages[0].currency]}\n\n'
                    f'Продолжаем в том же духе 💪',
        )

    reply_markup = build_switched_to_ai_keyboard(user_language_code, user.current_model)
    await message.answer(
        text=get_localization(user_language_code).switched(
            user.current_model,
            user.settings[user.current_model][UserSettings.VERSION],
        ),
        reply_markup=reply_markup,
    )


async def handle_cancel_subscription(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(user_id, state.storage)

    subscription = await get_last_subscription_by_user_id(user_id)
    if subscription and subscription.status == SubscriptionStatus.ACTIVE:
        text = get_localization(user_language_code).CANCEL_SUBSCRIPTION_CONFIRMATION
        reply_markup = build_cancel_subscription_keyboard(user_language_code)
    else:
        text = get_localization(user_language_code).NO_ACTIVE_SUBSCRIPTION
        reply_markup = None

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )


@payment_router.callback_query(lambda c: c.data.startswith('cancel_subscription:'))
async def handle_cancel_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    action = callback_query.data.split(':')[1]
    if action == 'approve':
        subscription = await get_last_subscription_by_user_id(user_id)
        subscription.status = SubscriptionStatus.CANCELED
        await update_subscription(
            subscription.id,
            {
                'status': subscription.status,
            }
        )

        user_language_code = await get_user_language(user_id, state.storage)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).CANCEL_SUBSCRIPTION_SUCCESS,
        )

        await send_message_to_admins(
            bot=callback_query.bot,
            message=f'#payment #subscription #canceled\n\n'
                    f'❌ <b>Отмена подписки у пользователя: {subscription.user_id}</b>\n\n'
                    f'ℹ️ ID: {subscription.id}\n'
                    f'💱 Метод оплаты: {subscription.payment_method}\n'
                    f'💳 Тип подписки: {subscription.type}\n'
                    f'💰 Сумма: {subscription.amount}{Currency.SYMBOLS[subscription.currency]}\n'
                    f'💸 Чистая сумма: {float(subscription.income_amount)}{Currency.SYMBOLS[subscription.currency]}\n'
                    f'🗓 Период подписки: {subscription.start_date.strftime("%d.%m.%Y")}-{subscription.end_date.strftime("%d.%m.%Y")}\n\n'
                    f'Грустно, но что поделать 🤷',
        )
    else:
        await callback_query.message.delete()
