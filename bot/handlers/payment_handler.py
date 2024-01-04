from datetime import datetime, timezone

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment, BufferedInputFile

from bot.config import config
from bot.database.main import bucket, db
from bot.database.models.common import Quota
from bot.database.models.package import PackageStatus, PackageType, Package
from bot.database.models.subscription import Subscription, SubscriptionStatus, SubscriptionLimit, SubscriptionType
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings
from bot.database.operations.package import write_package, get_last_package_by_user_id, get_packages_by_user_id
from bot.database.operations.subscription import write_subscription, get_last_subscription_by_user_id, \
    update_subscription
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, get_users
from bot.helpers.create_package import create_package
from bot.helpers.create_subscription import create_subscription
from bot.keyboards.payment import build_subscriptions_keyboard, build_period_of_subscription_keyboard, \
    build_packages_keyboard, build_quantity_of_packages_keyboard
from bot.locales.main import get_localization
from bot.states.payment import Payment

payment_router = Router()


class PaymentType:
    SUBSCRIPTION = 'SUBSCRIPTION'
    PACKAGE = 'PACKAGE'


@payment_router.message(Command("subscribe"))
async def subscribe(message: Message):
    user = await get_user(str(message.from_user.id))

    photo_path = f'subscriptions/{user.language_code}_{user.currency}.png'
    photo = bucket.blob(photo_path)
    photo_data = photo.download_as_string()

    text = get_localization(user.language_code).subscribe(user.currency)
    reply_markup = build_subscriptions_keyboard(user.language_code)

    await message.answer_photo(photo=BufferedInputFile(photo_data, filename=photo_path),
                               caption=text,
                               reply_markup=reply_markup)


@payment_router.callback_query(lambda c: c.data.startswith('subscribe:'))
async def handle_subscription_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    language_code = (await get_user(str(callback_query.from_user.id))).language_code

    subscription_type = callback_query.data.split(':')[1]

    message = get_localization(language_code).choose_how_many_months_to_subscribe(subscription_type)
    reply_markup = build_period_of_subscription_keyboard(language_code, subscription_type)

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

    await callback_query.delete_message()


@payment_router.message(Command("buy"))
async def buy(message: Message):
    user = await get_user(str(message.from_user.id))

    photo_path = f'packages/{user.language_code}_{user.currency}.png'
    photo = bucket.blob(photo_path)
    photo_data = photo.download_as_string()

    text = get_localization(user.language_code).buy()
    reply_markup = build_packages_keyboard(user.language_code)

    await message.answer_photo(photo=BufferedInputFile(photo_data, filename=photo_path),
                               caption=text,
                               reply_markup=reply_markup)


@payment_router.callback_query(lambda c: c.data.startswith('package:'))
async def handle_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    package_type = callback_query.data.split(':')[1]

    if package_type == PackageType.ACCESS_TO_CATALOG:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).ACCESS_TO_CATALOG
        description = get_localization(user.language_code).ACCESS_TO_CATALOG_DESCRIPTION

        await callback_query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{callback_query.from_user.id}:{package_type}:1",
            provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await callback_query.delete_message()
    elif package_type == PackageType.VOICE_MESSAGES:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
        description = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION

        await callback_query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{callback_query.from_user.id}:{package_type}:1",
            provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await callback_query.delete_message()
    elif package_type == PackageType.FAST_MESSAGES:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).FAST_ANSWERS
        description = get_localization(user.language_code).FAST_ANSWERS_DESCRIPTION

        await callback_query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{callback_query.from_user.id}:{package_type}:1",
            provider_token=config.YOOKASSA_TOKEN.get_secret_value(),
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await callback_query.delete_message()
    else:
        message = get_localization(user.language_code).choose_min(package_type)

        reply_markup = build_quantity_of_packages_keyboard(user.language_code)

        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

        await state.update_data(package_type=package_type)
        await state.set_state(Payment.waiting_for_package_quantity)


@payment_router.callback_query(Payment.waiting_for_package_quantity,
                               lambda c: c.data.startswith('quantity_of_package:'))
async def handle_quantity_of_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    if callback_query.data == 'cancel':
        await state.clear()

        await callback_query.delete_message()


@payment_router.message(Payment.waiting_for_package_quantity)
async def feedback_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        user_data = await state.get_data()
        package_type = user_data['package_type']
        quantity = int(message.text)
        if (
            (package_type == PackageType.GPT3 and quantity < 50) or
            (package_type == PackageType.GPT4 and quantity < 50) or
            (package_type == PackageType.CHAT and quantity < 1) or
            (package_type == PackageType.DALLE3 and quantity < 10) or
            (package_type == PackageType.FACE_SWAP and quantity < 10)
        ):
            await message.reply(text=get_localization(user.language_code).MIN_ERROR)
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
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR)


@payment_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    payment_type = pre_checkout_query.invoice_payload.split(':')[0]
    if payment_type == PaymentType.SUBSCRIPTION:
        _, user_id, subscription_type, subscription_period = pre_checkout_query.invoice_payload.split(':')
        try:
            await write_subscription(user_id,
                                     subscription_type,
                                     subscription_period,
                                     SubscriptionStatus.WAITING,
                                     pre_checkout_query.currency,
                                     pre_checkout_query.total_amount // 100)
            await pre_checkout_query.answer(ok=True)
        except Exception:
            await pre_checkout_query.answer(ok=False)
    elif payment_type == PaymentType.PACKAGE:
        _, user_id, package_type, quantity = pre_checkout_query.invoice_payload.split(':')
        try:
            await write_package(user_id,
                                package_type,
                                PackageStatus.WAITING,
                                pre_checkout_query.currency,
                                pre_checkout_query.total_amount // 100,
                                int(quantity))
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

        transaction = db.transaction()
        await create_subscription(transaction,
                                  subscription.id,
                                  subscription.user_id,
                                  payment.provider_payment_charge_id)
        await write_transaction(user_id=user.id,
                                type=TransactionType.INCOME,
                                service=subscription.type,
                                amount=subscription.amount,
                                currency=subscription.currency,
                                quantity=1)

        await message.answer(text=get_localization(user.language_code).SUBSCRIPTION_SUCCESS)
    elif payment_type == PaymentType.PACKAGE:
        package = await get_last_package_by_user_id(user_id)

        transaction = db.transaction()
        await create_package(transaction,
                             package.id,
                             package.user_id,
                             payment.provider_payment_charge_id)

        service_type = package.type
        if package.type == PackageType.GPT3:
            service_type = ServiceType.GPT3
        elif package.type == PackageType.GPT4:
            service_type = ServiceType.GPT4
        elif package.type == PackageType.DALLE3:
            service_type = ServiceType.DALLE3
        elif package.type == PackageType.FACE_SWAP:
            service_type = ServiceType.FACE_SWAP
        elif package.type == PackageType.CHAT:
            service_type = ServiceType.ADDITIONAL_CHATS
        elif package.type == PackageType.ACCESS_TO_CATALOG:
            service_type = ServiceType.ACCESS_TO_CATALOG
        elif package.type == PackageType.VOICE_MESSAGES:
            service_type = ServiceType.VOICE_MESSAGES
        elif package.type == PackageType.FAST_MESSAGES:
            service_type = ServiceType.FAST_MESSAGES
        await write_transaction(user_id=user.id,
                                type=TransactionType.INCOME,
                                service=service_type,
                                amount=package.amount,
                                currency=package.currency,
                                quantity=package.quantity)

        await message.answer(text=get_localization(user.language_code).PACKAGE_SUCCESS)


async def update_monthly_limits(bot: Bot):
    all_users = await get_users()
    for i in range(0, len(all_users), config.USER_BATCH_SIZE):
        batch = db.batch()
        user_batch = all_users[i:i + config.USER_BATCH_SIZE]

        for user in user_batch:
            user_ref = db.collection("users").document(user.id)

            current_date = datetime.now(timezone.utc)
            is_time_to_update_limits = (current_date - user.last_subscription_limit_update).days >= 30
            if user.last_subscription_limit_update and is_time_to_update_limits:
                current_subscription = await get_last_subscription_by_user_id(user.id)
                if current_subscription and current_subscription.end_date <= current_date:
                    packages = await get_packages_by_user_id(user.id)
                    user.additional_usage_quota[Quota.VOICE_MESSAGES] = False
                    user.additional_usage_quota[Quota.FAST_MESSAGES] = False
                    user.additional_usage_quota[Quota.ACCESS_TO_CATALOG] = False
                    for package in packages:
                        if package.type == PackageType.VOICE_MESSAGES:
                            user.additional_usage_quota[Quota.VOICE_MESSAGES] = True
                        elif package.type == PackageType.FAST_MESSAGES:
                            user.additional_usage_quota[Quota.FAST_MESSAGES] = True
                        elif package.type == PackageType.ACCESS_TO_CATALOG:
                            user.additional_usage_quota[Quota.ACCESS_TO_CATALOG] = True

                    if not user.additional_usage_quota[Quota.VOICE_MESSAGES]:
                        user.settings[UserSettings.TURN_ON_VOICE_MESSAGES] = False

                    await update_subscription(current_subscription.id, {
                        "status": SubscriptionStatus.FINISHED,
                    })
                    batch.update(user_ref, {
                        "monthly_limits": SubscriptionLimit.LIMITS[SubscriptionType.FREE],
                        "additional_usage_quota": user.additional_usage_quota,
                        "settings": user.settings,
                        "last_subscription_limit_update": datetime.now(timezone.utc)
                    })

                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user.language_code).SUBSCRIPTION_END
                    )
                else:
                    batch.update(user_ref, {
                        "monthly_limits": SubscriptionLimit.LIMITS[SubscriptionType.FREE],
                        "last_subscription_limit_update": datetime.now(timezone.utc)
                    })

                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user.language_code).SUBSCRIPTION_RESET
                    )

        await batch.commit()
