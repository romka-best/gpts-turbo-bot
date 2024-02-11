from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, URLInputFile

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import PaymentType
from bot.database.models.package import PackageStatus, PackageType, Package, PackageMinimum
from bot.database.models.subscription import Subscription, SubscriptionStatus
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.package import write_package, get_last_package_by_user_id
from bot.database.operations.subscription import write_subscription, get_last_subscription_by_user_id
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user
from bot.helpers.create_package import create_package
from bot.helpers.create_subscription import create_subscription
from bot.keyboards.common import build_cancel_keyboard, build_recommendations_keyboard
from bot.keyboards.payment import (
    build_buy_keyboard,
    build_subscriptions_keyboard,
    build_period_of_subscription_keyboard,
    build_packages_keyboard,
)
from bot.locales.main import get_localization
from bot.states.payment import Payment

payment_router = Router()


async def handle_buy(message: Message, user_id: str):
    user = await get_user(user_id)

    reply_keyboard = build_buy_keyboard(user.language_code)
    text = get_localization(user.language_code).BUY
    await message.answer(
        text=text,
        reply_markup=reply_keyboard,
    )


@payment_router.message(Command("buy"))
async def buy(message: Message, state: FSMContext):
    await state.clear()

    await handle_buy(message, str(message.from_user.id))


@payment_router.callback_query(lambda c: c.data.startswith('buy:'))
async def handle_buy_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    payment_type = callback_query.data.split(':')[1]
    if payment_type == PaymentType.PACKAGE:
        await handle_package(callback_query.message, user_id)
    elif payment_type == PaymentType.SUBSCRIPTION:
        await handle_subscribe(callback_query.message, user_id)

    await callback_query.message.delete()


async def handle_subscribe(message: Message, user_id: str):
    user = await get_user(str(user_id))

    photo_path = f'subscriptions/{user.language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user.language_code).subscribe(user.currency)
    reply_markup = build_subscriptions_keyboard(user.language_code)
    await message.answer_photo(
        photo=URLInputFile(photo_link, filename=photo_path),
        caption=text,
        reply_markup=reply_markup,
    )


@payment_router.callback_query(lambda c: c.data.startswith('subscription:'))
async def handle_subscription_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    subscription_type = callback_query.data.split(':')[1]
    if subscription_type == 'back':
        await handle_buy(callback_query.message, user_id)
        await callback_query.message.delete()
    else:
        user = await get_user(user_id)

        message = get_localization(user.language_code).choose_how_many_months_to_subscribe(subscription_type)
        reply_markup = build_period_of_subscription_keyboard(user.language_code, subscription_type)

        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)


@payment_router.callback_query(lambda c: c.data.startswith('period_of_subscription:'))
async def handle_period_of_subscription_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    subscription_type, subscription_period = callback_query.data.split(':')[1], callback_query.data.split(':')[2]

    emojis = Subscription.get_emojis()
    price = Subscription.get_price(user.currency, subscription_type, subscription_period)
    name = (f"{subscription_type} {emojis[subscription_type]} "
            f"({get_localization(user.language_code).cycles_subscribe()[subscription_period]})")
    description = get_localization(user.language_code).confirmation_subscribe(subscription_type, subscription_period)

    await callback_query.message.reply_invoice(
        title=name,
        description=description,
        payload=f"{PaymentType.SUBSCRIPTION}:{callback_query.from_user.id}:{subscription_type}:{subscription_period}",
        provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
        currency=f"{user.currency}",
        prices=[LabeledPrice(label=name, amount=price * 100)],
    )

    await callback_query.message.delete()


async def handle_package(message: Message, user_id: str):
    user = await get_user(user_id)

    photo_path = f'packages/{user.language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user.language_code).package()
    reply_markup = build_packages_keyboard(user.language_code)

    await message.answer_photo(
        photo=URLInputFile(photo_link, filename=photo_path),
        caption=text,
        reply_markup=reply_markup,
    )


@payment_router.callback_query(lambda c: c.data.startswith('package:'))
async def handle_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_id = str(callback_query.from_user.id)

    package_type = callback_query.data.split(':')[1]
    if package_type == 'back':
        await handle_buy(callback_query.message, user_id)
        await callback_query.message.delete()
    else:
        user = await get_user(user_id)

        message = get_localization(user.language_code).choose_min(package_type)

        reply_markup = build_cancel_keyboard(user.language_code)

        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

        await state.update_data(package_type=package_type)
        await state.set_state(Payment.waiting_for_package_quantity)


@payment_router.message(Payment.waiting_for_package_quantity, ~F.text.startswith('/'))
async def quantity_of_package_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        user_data = await state.get_data()
        package_type = user_data['package_type']
        quantity = int(message.text)
        if (
            (package_type == PackageType.GPT3 and quantity < PackageMinimum.GPT3) or
            (package_type == PackageType.GPT4 and quantity < PackageMinimum.GPT4) or
            (package_type == PackageType.CHAT and quantity < PackageMinimum.CHAT) or
            (package_type == PackageType.DALLE3 and quantity < PackageMinimum.DALLE3) or
            (package_type == PackageType.FACE_SWAP and quantity < PackageMinimum.FACE_SWAP) or
            (package_type == PackageType.MUSIC_GEN and quantity < PackageMinimum.MUSIC_GEN) or
            (package_type == PackageType.ACCESS_TO_CATALOG and quantity < PackageMinimum.ACCESS_TO_CATALOG) or
            (package_type == PackageType.VOICE_MESSAGES and quantity < PackageMinimum.VOICE_MESSAGES) or
            (package_type == PackageType.FAST_MESSAGES and quantity < PackageMinimum.FAST_MESSAGES)
        ):
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.reply(text=get_localization(user.language_code).MIN_ERROR,
                                reply_markup=reply_markup)
        else:
            price = Package.get_price(user.currency, package_type, quantity)
            name = ""
            description = ""
            if package_type == PackageType.GPT3:
                name = get_localization(user.language_code).GPT3_REQUESTS
                description = get_localization(user.language_code).GPT3_REQUESTS_DESCRIPTION
            elif package_type == PackageType.GPT4:
                name = get_localization(user.language_code).GPT4_REQUESTS
                description = get_localization(user.language_code).GPT4_REQUESTS_DESCRIPTION
            elif package_type == PackageType.CHAT:
                name = get_localization(user.language_code).THEMATIC_CHATS
                description = get_localization(user.language_code).THEMATIC_CHATS_DESCRIPTION
            elif package_type == PackageType.DALLE3:
                name = get_localization(user.language_code).DALLE3_REQUESTS
                description = get_localization(user.language_code).DALLE3_REQUESTS_DESCRIPTION
            elif package_type == PackageType.FACE_SWAP:
                name = get_localization(user.language_code).FACE_SWAP_REQUESTS
                description = get_localization(user.language_code).FACE_SWAP_REQUESTS_DESCRIPTION
            elif package_type == PackageType.MUSIC_GEN:
                name = get_localization(user.language_code).MUSIC_GEN_REQUESTS
                description = get_localization(user.language_code).MUSIC_GEN_REQUESTS_DESCRIPTION
            elif package_type == PackageType.ACCESS_TO_CATALOG:
                name = get_localization(user.language_code).ACCESS_TO_CATALOG
                description = get_localization(user.language_code).ACCESS_TO_CATALOG_DESCRIPTION
            elif package_type == PackageType.VOICE_MESSAGES:
                name = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
                description = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION
            elif package_type == PackageType.FAST_MESSAGES:
                name = get_localization(user.language_code).FAST_ANSWERS
                description = get_localization(user.language_code).FAST_ANSWERS_DESCRIPTION

            await message.reply_invoice(
                title=f"{name} ({quantity})",
                description=description,
                payload=f"{PaymentType.PACKAGE}:{user.id}:{package_type}:{quantity}",
                provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
                currency=f"{user.currency}",
                prices=[LabeledPrice(label=name, amount=price * 100)],
            )

            await state.clear()
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR,
                            reply_markup=reply_markup)


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
    else:
        await pre_checkout_query.answer(ok=False)


@payment_router.message(F.successful_payment)
async def successful_payment(message: Message):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)

    payment = message.successful_payment
    payment_type = payment.invoice_payload.split(':')[0]
    if payment_type == PaymentType.SUBSCRIPTION:
        subscription = await get_last_subscription_by_user_id(user_id)

        transaction = firebase.db.transaction()
        await create_subscription(transaction,
                                  subscription.id,
                                  subscription.user_id,
                                  payment.provider_payment_charge_id)
        await write_transaction(
            user_id=user.id,
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

        await message.answer(text=get_localization(user.language_code).SUBSCRIPTION_SUCCESS)
    elif payment_type == PaymentType.PACKAGE:
        package = await get_last_package_by_user_id(user_id)

        transaction = firebase.db.transaction()
        await create_package(
            transaction,
            package.id,
            package.user_id,
            payment.provider_payment_charge_id,
        )

        service_type = package.type
        if package.type == PackageType.GPT3:
            service_type = ServiceType.GPT3
        elif package.type == PackageType.GPT4:
            service_type = ServiceType.GPT4
        elif package.type == PackageType.DALLE3:
            service_type = ServiceType.DALLE3
        elif package.type == PackageType.FACE_SWAP:
            service_type = ServiceType.FACE_SWAP
        elif package.type == PackageType.MUSIC_GEN:
            service_type = ServiceType.MUSIC_GEN
        elif package.type == PackageType.CHAT:
            service_type = ServiceType.ADDITIONAL_CHATS
        elif package.type == PackageType.ACCESS_TO_CATALOG:
            service_type = ServiceType.ACCESS_TO_CATALOG
        elif package.type == PackageType.VOICE_MESSAGES:
            service_type = ServiceType.VOICE_MESSAGES
        elif package.type == PackageType.FAST_MESSAGES:
            service_type = ServiceType.FAST_MESSAGES
        await write_transaction(
            user_id=user.id,
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

        await message.answer(text=get_localization(user.language_code).PACKAGE_SUCCESS)

    reply_markup = await build_recommendations_keyboard(user)
    await message.answer(
        text=get_localization(user.language_code).switched(user.current_model),
        reply_markup=reply_markup,
    )
