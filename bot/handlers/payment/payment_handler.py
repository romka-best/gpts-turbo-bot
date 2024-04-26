from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, URLInputFile

from bot.config import config
from bot.database.main import firebase
from bot.database.models.cart import CartItem
from bot.database.models.common import PaymentType, Model
from bot.database.models.package import PackageStatus, PackageType, Package
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.models.transaction import TransactionType
from bot.database.models.user import UserSettings
from bot.database.operations.cart.getters import get_cart_by_user_id
from bot.database.operations.cart.updaters import update_cart
from bot.database.operations.package.getters import get_last_package_by_user_id, get_packages_by_user_id_and_status
from bot.database.operations.package.updaters import update_package
from bot.database.operations.package.writers import write_package
from bot.database.operations.subscription.getters import get_last_subscription_by_user_id
from bot.database.operations.subscription.writers import write_subscription
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user
from bot.handlers.payment.promo_code_handler import handle_promo_code
from bot.helpers.creaters.create_package import create_package
from bot.helpers.creaters.create_subscription import create_subscription
from bot.helpers.senders.send_message_to_admins import send_message_to_admins
from bot.keyboards.common.common import build_recommendations_keyboard
from bot.keyboards.payment.payment import (
    build_buy_keyboard,
    build_subscriptions_keyboard,
    build_period_of_subscription_keyboard,
    build_packages_keyboard,
    build_package_selection_keyboard,
    build_package_quantity_sent_keyboard,
    build_package_cart_keyboard,
    build_package_add_to_cart_selection_keyboard,
    build_package_proceed_to_checkout_keyboard,
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

    photo_path = f'payments/subscriptions_{user_language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user_language_code).subscribe(user.currency)
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
    user = await get_user(str(user_id))

    subscription_type = callback_query.data.split(':')[1]
    if subscription_type == 'back':
        await handle_buy(callback_query.message, user_id, state)
        await callback_query.message.delete()
    else:
        user_language_code = await get_user_language(user_id, state.storage)

        caption = get_localization(user_language_code).choose_how_many_months_to_subscribe(subscription_type)
        reply_markup = build_period_of_subscription_keyboard(user_language_code, subscription_type, user.discount)
        photo_path = f'payments/subscription_{subscription_type.lower()}_{user_language_code}_{user.currency}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=caption,
            reply_markup=reply_markup,
        )
        await callback_query.message.delete()


@payment_router.callback_query(lambda c: c.data.startswith('period_of_subscription:'))
async def handle_period_of_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    subscription_type, subscription_period = callback_query.data.split(':')[1], callback_query.data.split(':')[2]

    emojis = Subscription.get_emojis()
    price = Subscription.get_price(user.currency, subscription_type, subscription_period, user.discount)
    name = (f"{subscription_type} {emojis[subscription_type]} "
            f"({get_localization(user_language_code).cycles_subscribe()[subscription_period]})")
    description = get_localization(user_language_code).confirmation_subscribe(subscription_type, subscription_period)
    photo_path = f'payments/subscription_{subscription_type.lower()}_{user_language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    await callback_query.message.reply_invoice(
        title=name,
        description=description,
        payload=f"{PaymentType.SUBSCRIPTION}:{callback_query.from_user.id}:{subscription_type}:{subscription_period}",
        provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
        currency=f"{user.currency}",
        prices=[LabeledPrice(label=name, amount=price * 100)],
        photo_url=photo_link,
        photo_width=1024,
        photo_height=768,
    )

    await callback_query.message.delete()


async def handle_package(message: Message, user_id: str, state: FSMContext):
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    photo_path = f'payments/packages_{user_language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user_language_code).package()
    reply_markup = build_packages_keyboard(user_language_code)

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
    if package_type == 'back':
        await handle_buy(callback_query.message, user_id, state)
        await callback_query.message.delete()
    elif package_type == 'cart':
        cart = await get_cart_by_user_id(user_id)

        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items)
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

        photo_path = f'payments/packages_{user_language_code}_{user.currency}.png'
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
    user = await get_user(user_id)
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
        cart_items = [{"package_type": package_type, "quantity": package_quantity}]
        if not Package.is_above_minimal_price(user.currency, cart_items):
            reply_markup = build_package_selection_keyboard(user_language_code)
            await callback_query.message.reply(
                text=get_localization(user_language_code).MIN_ERROR,
                reply_markup=reply_markup,
            )
        else:
            price = Package.get_price(user.currency, package_type, package_quantity)
            name_and_description = Package.get_translate_name_and_description(
                get_localization(user_language_code),
                package_type,
            )
            name = name_and_description.get('name')
            description = name_and_description.get('description')

            photo_path = f'payments/packages_{user_language_code}_{user.currency}.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_link = firebase.get_public_url(photo.name)

            await callback_query.message.reply_invoice(
                title=f"{name} ({package_quantity})",
                description=description,
                payload=f"{PaymentType.PACKAGE}:{user.id}:{package_type}:{package_quantity}",
                provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
                currency=f"{user.currency}",
                prices=[LabeledPrice(label=name, amount=price * 100)],
                photo_url=photo_link,
                photo_width=1024,
                photo_height=768,
            )

            await callback_query.message.delete()
            await state.clear()


@payment_router.callback_query(lambda c: c.data.startswith('package_add_to_cart_selection:'))
async def handle_package_add_to_cart_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    action = callback_query.data.split(':')[1]
    if action == "go_to_cart":
        cart = await get_cart_by_user_id(user_id)

        photo_path = f'payments/packages_{user_language_code}_{user.currency}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        message = get_localization(user_language_code).shopping_cart(user.currency, cart.items)
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
        cart = await get_cart_by_user_id(user_id)

        if not Package.is_above_minimal_price(user.currency, cart.items):
            reply_markup = build_package_proceed_to_checkout_keyboard(user_language_code)
            await callback_query.message.edit_caption(
                caption=get_localization(user_language_code).MIN_ERROR,
                reply_markup=reply_markup,
            )
        else:
            prices = []
            payload = f"{PaymentType.CART}:{user.id}"
            for cart_item in cart.items:
                package_type, package_quantity = cart_item.get("package_type"), cart_item.get("quantity", 0)

                name_and_description = Package.get_translate_name_and_description(
                    get_localization(user_language_code),
                    package_type,
                )
                name = name_and_description.get('name')
                price = Package.get_price(user.currency, package_type, package_quantity)

                prices.append(LabeledPrice(label=f"{name} ({package_quantity})", amount=price * 100))
                payload += f":{package_type}:{package_quantity}"

            photo_path = f'payments/packages_{user_language_code}_{user.currency}.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_link = firebase.get_public_url(photo.name)

            await callback_query.message.reply_invoice(
                title=f"{get_localization(user_language_code).PACKAGES}",
                description=f"{get_localization(user_language_code).SHOPPING_CART}",
                payload=payload,
                provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
                currency=f"{user.currency}",
                prices=prices,
                photo_url=photo_link,
                photo_width=1024,
                photo_height=768,
            )

            await callback_query.message.delete()
            await state.clear()
    elif action == "clear":
        cart = await get_cart_by_user_id(user_id)
        if cart.items:
            cart.items = []
            await update_cart(cart.id, {
                "items": cart.items,
            })

            message = get_localization(user_language_code).shopping_cart(user.currency, cart.items)
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

    message = get_localization(user_language_code).shopping_cart(user.currency, cart.items)
    reply_markup = build_package_cart_keyboard(user_language_code)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)


@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    payment_type = pre_checkout_query.invoice_payload.split(':')[0]
    if payment_type == PaymentType.SUBSCRIPTION:
        _, user_id, subscription_type, subscription_period = pre_checkout_query.invoice_payload.split(':')
        try:
            await write_subscription(
                user_id,
                subscription_type,
                subscription_period,
                SubscriptionStatus.WAITING,
                pre_checkout_query.currency,
                pre_checkout_query.total_amount // 100,
            )
            await pre_checkout_query.answer(ok=True)
        except Exception:
            await pre_checkout_query.answer(ok=False)
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
                user_id,
                package_type,
                PackageStatus.WAITING,
                pre_checkout_query.currency,
                pre_checkout_query.total_amount // 100,
                int(quantity),
                until_at,
            )
            await pre_checkout_query.answer(ok=True)
        except Exception:
            await pre_checkout_query.answer(ok=False)
    elif payment_type == PaymentType.CART:
        _, user_id, packages = pre_checkout_query.invoice_payload.split(':', 2)
        packages = packages.split(':')

        try:
            packages_with_waiting_status = await get_packages_by_user_id_and_status(user_id, PackageStatus.WAITING)
            for package_with_waiting_status in packages_with_waiting_status:
                await update_package(package_with_waiting_status.id, {
                    "status": PackageStatus.CANCELED,
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
                package_amount = Package.get_price(pre_checkout_query.currency, package_type, package_quantity)
                await write_package(
                    user_id,
                    package_type,
                    PackageStatus.WAITING,
                    pre_checkout_query.currency,
                    package_amount,
                    package_quantity,
                    until_at,
                )
            await pre_checkout_query.answer(ok=True)
        except Exception:
            await pre_checkout_query.answer(ok=False)
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
        subscription = await get_last_subscription_by_user_id(user_id)

        transaction = firebase.db.transaction()
        await create_subscription(
            transaction,
            subscription.id,
            subscription.user_id,
            payment.provider_payment_charge_id,
        )
        await write_transaction(
            user_id=user_id,
            type=TransactionType.INCOME,
            service=subscription.type,
            amount=subscription.amount,
            currency=subscription.currency,
            quantity=1,
            details={
                'subscription_id': subscription.id,
                'provider_payment_charge_id': payment.provider_payment_charge_id
            },
        )
        await update_user(user_id, {
            "discount": 0,
        })

        await message.answer(text=get_localization(user_language_code).SUBSCRIPTION_SUCCESS)
        await send_message_to_admins(
            bot=message.bot,
            message=f"#payment #subscription\n\n🤑<b>Успешно прошла оплата подписки у пользователя: {user_id}</b>\n\n"
                    f"💳 Тип подписки: {subscription.type}\n"
                    f"💰 Сумма: {subscription.amount}₽\n\n"
                    f"Продолжаем в том же духе 💪",
        )
    elif payment_type == PaymentType.PACKAGE:
        package = await get_last_package_by_user_id(user_id)

        transaction = firebase.db.transaction()
        await create_package(
            transaction,
            package.id,
            package.user_id,
            payment.provider_payment_charge_id,
        )

        service_type, _ = Package.get_service_type_and_update_quota(package.type, user.additional_usage_quota, 0)
        await write_transaction(
            user_id=user_id,
            type=TransactionType.INCOME,
            service=service_type,
            amount=package.amount,
            currency=package.currency,
            quantity=package.quantity,
            details={
                'package_id': package.id,
                'provider_payment_charge_id': payment.provider_payment_charge_id
            },
        )

        await message.answer(text=get_localization(user_language_code).PACKAGE_SUCCESS)
        await send_message_to_admins(
            bot=message.bot,
            message=f"#payment #package\n\n🤑<b>Успешно прошла оплата пакета у пользователя: {user_id}</b>\n\n"
                    f"💳 Тип пакета: {package.type}\n"
                    f"🔢 Количество: {package.quantity}\n"
                    f"💰 Сумма: {package.amount}₽\n\n"
                    f"Продолжаем в том же духе 💪",
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
                payment.provider_payment_charge_id,
            )

            service_type, _ = Package.get_service_type_and_update_quota(package.type, user.additional_usage_quota, 0)
            await write_transaction(
                user_id=user_id,
                type=TransactionType.INCOME,
                service=service_type,
                amount=package.amount,
                currency=package.currency,
                quantity=package.quantity,
                details={
                    'package_id': package.id,
                    'provider_payment_charge_id': payment.provider_payment_charge_id
                },
            )

        cart = await get_cart_by_user_id(user_id)
        cart.items = []
        await update_cart(cart.id, {
            "items": cart.items,
        })

        await message.answer(text=get_localization(user_language_code).PACKAGES_SUCCESS)
        await send_message_to_admins(
            bot=message.bot,
            message=f"#payment #packages\n\n🤑<b>Успешно прошла оплата пакетов у пользователя: {user_id}</b>\n\n"
                    f"💰 Сумма: {payment.total_amount // 100}₽\n\n"
                    f"Продолжаем в том же духе 💪",
        )

    reply_markup = await build_recommendations_keyboard(user.current_model, user_language_code, user.gender)
    await message.answer(
        text=get_localization(user_language_code).switched(
            user.current_model,
            user.settings[Model.CHAT_GPT][UserSettings.VERSION],
        ),
        reply_markup=reply_markup,
    )
