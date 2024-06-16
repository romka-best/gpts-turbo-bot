from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.models.cart import CartItem
from bot.database.models.common import PaymentType, PaymentMethod, Currency
from bot.database.models.package import PackageStatus, PackageType, Package
from bot.database.models.subscription import Subscription, SubscriptionStatus, SubscriptionType, SubscriptionPeriod
from bot.database.operations.cart.getters import get_cart_by_user_id
from bot.database.operations.cart.updaters import update_cart
from bot.database.operations.package.getters import get_packages_by_user_id_and_status
from bot.database.operations.package.updaters import update_package
from bot.database.operations.package.writers import write_package
from bot.database.operations.subscription.getters import get_last_subscription_by_user_id
from bot.database.operations.subscription.updaters import update_subscription
from bot.database.operations.subscription.writers import write_subscription
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.payment.promo_code_handler import handle_promo_code
from bot.helpers.billing.create_payment import create_payment
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
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
    build_payment_method_for_cart_keyboard,
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


@payment_router.message(Command("buy"))
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
        SubscriptionType.STANDARD: Subscription.get_price(
            user.currency,
            SubscriptionType.STANDARD,
            SubscriptionPeriod.MONTH1,
            user.discount,
        )[1],
        SubscriptionType.VIP: Subscription.get_price(
            user.currency,
            SubscriptionType.VIP,
            SubscriptionPeriod.MONTH1,
            user.discount,
        )[1],
        SubscriptionType.PREMIUM: Subscription.get_price(
            user.currency,
            SubscriptionType.PREMIUM,
            SubscriptionPeriod.MONTH1,
            user.discount,
        )[1],
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
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )
        else:
            user.currency = Currency.RUB
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )

        min_prices = {
            SubscriptionType.STANDARD: Subscription.get_price(
                user.currency,
                SubscriptionType.STANDARD,
                SubscriptionPeriod.MONTH1,
                user.discount,
            )[1],
            SubscriptionType.VIP: Subscription.get_price(
                user.currency,
                SubscriptionType.VIP,
                SubscriptionPeriod.MONTH1,
                user.discount,
            )[1],
            SubscriptionType.PREMIUM: Subscription.get_price(
                user.currency,
                SubscriptionType.PREMIUM,
                SubscriptionPeriod.MONTH1,
                user.discount,
            )[1],
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
                )[1]
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
                )[1]
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
        else:
            raise NotImplementedError


async def handle_package(message: Message, user_id: str, state: FSMContext, is_edit=False, page=0):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    photo_path = f'payments/packages_{user_language_code}.png'
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
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )
        else:
            user.currency = Currency.RUB
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )

        page = int(callback_query.data.split(':')[2])
        await handle_package(callback_query.message, str(callback_query.from_user.id), state, True, page)
    elif package_type == 'back':
        await handle_buy(callback_query.message, user_id, state)
        await callback_query.message.delete()
    elif package_type == 'cart':
        cart = await get_cart_by_user_id(user_id)

        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
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
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        quantity = int(message.text)

        photo_path = f'payments/packages_{user_language_code}.png'
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
    if action == "add_to_cart":
        cart = await get_cart_by_user_id(user_id)
        is_already_in_cart = False
        for index, cart_item in enumerate(cart.items):
            if cart_item.get("package_type") == package_type:
                is_already_in_cart = True
                cart.items[index]["quantity"] = cart_item.get("quantity", 0) + package_quantity
                break
        if not is_already_in_cart:
            cart.items.append(CartItem(package_type, package_quantity).to_dict())

        await update_cart(cart.id, {
            "items": cart.items,
        })

        reply_markup = build_package_add_to_cart_selection_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).GO_TO_CART_OR_CONTINUE_SHOPPING,
            reply_markup=reply_markup,
        )
    elif action == "buy_now":
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
    if action == "go_to_cart":
        cart = await get_cart_by_user_id(user_id)

        photo_path = f'payments/packages_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=message,
            reply_markup=reply_markup,
        )
        await callback_query.message.delete()
    elif action == "continue_shopping":
        await handle_package(callback_query.message, user_id, state)
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('package_cart:'))
async def handle_package_cart_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == "proceed_to_checkout":
        reply_markup = build_payment_method_for_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(
            caption=get_localization(user_language_code).CHOOSE_PAYMENT_METHOD,
            reply_markup=reply_markup,
        )
    elif action == "clear":
        cart = await get_cart_by_user_id(user_id)
        if cart.items:
            cart.items = []
            await update_cart(cart.id, {
                "items": cart.items,
            })

            message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
            reply_markup = build_package_cart_keyboard(user_language_code)
            await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    elif action == "change_currency":
        if user.currency == Currency.RUB:
            user.currency = Currency.USD
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )
        else:
            user.currency = Currency.RUB
            await update_user(
                user_id,
                {
                    "currency": user.currency,
                }
            )

        cart = await get_cart_by_user_id(user_id)
        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    elif action == "back":
        await handle_package(callback_query.message, user_id, state)
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('package_proceed_to_checkout:'))
async def handle_package_proceed_to_checkout_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    cart = await get_cart_by_user_id(user_id)

    message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
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
            amount = Package.get_price(Currency.RUB, package_type, package_quantity, user.discount)
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
            amount = Package.get_price(Currency.USD, package_type, package_quantity, user.discount)
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
        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items, user.discount)
        reply_markup = build_package_cart_keyboard(user_language_code)
        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)
    else:
        if payment_method == PaymentMethod.YOOKASSA:
            amount = 0
            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get("package_type"), cart_item.get("quantity", 0)

                amount += Package.get_price(Currency.RUB, package_type, package_quantity, user.discount)

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
                    "status": PackageStatus.CANCELED,
                })

            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get("package_type"), cart_item.get("quantity", 0)

                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * package_quantity)
                package_amount = Package.get_price(Currency.RUB, package_type, package_quantity, user.discount)
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
                package_type, package_quantity = cart_item.get("package_type"), cart_item.get("quantity", 0)

                amount += Package.get_price(Currency.USD, package_type, package_quantity, user.discount)

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
                    "status": PackageStatus.CANCELED,
                })

            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get("package_type"), cart_item.get("quantity", 0)

                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * package_quantity)
                package_amount = Package.get_price(Currency.USD, package_type, package_quantity, user.discount)
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
        else:
            raise NotImplementedError


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
                "status": subscription.status,
            }
        )

        user_language_code = await get_user_language(user_id, state.storage)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).CANCEL_SUBSCRIPTION_SUCCESS,
        )

        await send_message_to_admins(
            bot=callback_query.bot,
            message=f"#payment #subscription #canceled\n\n"
                    f"❌ <b>Отмена подписки у пользователя: {subscription.user_id}</b>\n\n"
                    f"ℹ️ ID: {subscription.id}\n"
                    f"💱 Метод оплаты: {subscription.payment_method}\n"
                    f"💳 Тип подписки: {subscription.type}\n"
                    f"💰 Сумма: {subscription.amount}{Currency.SYMBOLS[subscription.currency]}\n"
                    f"💸 Чистая сумма: {float(subscription.income_amount)}{Currency.SYMBOLS[subscription.currency]}\n"
                    f"🗓 Период подписки: {subscription.start_date.strftime('%d.%m.%Y')}-{subscription.end_date.strftime('%d.%m.%Y')}\n\n"
                    f"Грустно, но что поделать 🤷",
        )
    else:
        await callback_query.message.delete()
