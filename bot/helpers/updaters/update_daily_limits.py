import logging
from datetime import datetime, timezone

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from google.cloud.firestore_v1 import AsyncWriteBatch

from bot.config import config
from bot.database.main import firebase
from bot.database.models.common import Quota, DEFAULT_ROLE, PaymentMethod
from bot.database.models.subscription import (
    SubscriptionStatus,
    SUBSCRIPTION_FREE_LIMITS,
)
from bot.database.models.user import User, UserSettings
from bot.database.operations.chat.getters import get_chats_by_user_id
from bot.database.operations.chat.updaters import update_chat
from bot.database.operations.package.getters import get_packages_by_user_id
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.getters import get_last_subscription_by_user_id
from bot.database.operations.subscription.updaters import update_subscription
from bot.database.operations.user.getters import get_users
from bot.database.operations.user.updaters import update_user
from bot.helpers.billing.create_auto_payment import create_auto_payment
from bot.helpers.billing.create_payment import OrderItem
from bot.helpers.senders.send_error_info import send_error_info
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers
from bot.locales.main import get_localization


async def update_daily_limits(bot: Bot):
    all_users = await get_users(is_blocked=False)

    for i in range(0, len(all_users), config.BATCH_SIZE):
        batch = firebase.db.batch()
        user_batch = all_users[i:i + config.BATCH_SIZE]

        for user in user_batch:
            await update_user_daily_limits(bot, user, batch)

        await batch.commit()

    await send_message_to_admins_and_developers(bot, f'<b>Updated daily limits successfully</b> 🎉')


async def update_user_daily_limits(bot: Bot, user: User, batch: AsyncWriteBatch):
    try:
        had_subscription = bool(user.subscription_id)
        user = await update_user_subscription(bot, user, batch)
        await update_user_additional_usage_quota(bot, user, had_subscription, batch)
    except TelegramForbiddenError:
        await update_user(user.id, {
            'is_blocked': True,
        })
    except Exception as e:
        logging.error(f'Error updating user {user.id}: {e}')
        await send_error_info(
            bot=bot,
            user_id=user.id,
            info=str(e),
            hashtags=['user', 'update'],
        )


async def update_user_subscription(bot: Bot, user: User, batch: AsyncWriteBatch):
    user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)
    current_date = datetime.now(timezone.utc)
    current_subscription = await get_last_subscription_by_user_id(user.id)

    if (
        current_subscription and
        current_subscription.end_date <= current_date and
        current_subscription.status != SubscriptionStatus.FINISHED
    ):
        if current_subscription.provider_auto_payment_charge_id and current_subscription.status != SubscriptionStatus.CANCELED:
            product = await get_product(current_subscription.product_id)
            if current_subscription.payment_method == PaymentMethod.YOOKASSA:
                payment = await create_auto_payment(
                    payment_method=current_subscription.payment_method,
                    provider_auto_payment_charge_id=current_subscription.provider_auto_payment_charge_id,
                    user_id=current_subscription.user_id,
                    description=get_localization(user.interface_language_code).payment_description_renew_subscription(
                        current_subscription.user_id,
                        product.names.get(user.interface_language_code),
                    ),
                    amount=current_subscription.amount,
                    language_code=user.interface_language_code,
                    order_items=[
                        OrderItem(
                            product=product,
                            price=current_subscription.amount,
                        ),
                    ],
                )
                if not payment:
                    current_subscription.status = SubscriptionStatus.FINISHED
                    user.daily_limits = SUBSCRIPTION_FREE_LIMITS

                    await update_subscription(current_subscription.id, {'status': current_subscription.status})
                    batch.update(user_ref, {
                        'subscription_id': '',
                        'daily_limits': user.daily_limits,
                        'last_subscription_limit_update': current_date,
                        'edited_at': current_date,
                    })

                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user.interface_language_code).SUBSCRIPTION_END,
                        disable_notification=True,
                    )
                return user
            elif current_subscription.payment_method == PaymentMethod.PAY_SELECTION:
                payment = await create_auto_payment(
                    payment_method=current_subscription.payment_method,
                    provider_auto_payment_charge_id=current_subscription.provider_auto_payment_charge_id,
                    user_id=current_subscription.user_id,
                    description=get_localization(user.interface_language_code).payment_description_renew_subscription(
                        current_subscription.user_id,
                        product.names.get(user.interface_language_code),
                    ),
                    amount=current_subscription.amount,
                    language_code=user.interface_language_code,
                    order_items=[
                        OrderItem(
                            product=product,
                            price=current_subscription.amount,
                        ),
                    ],
                    order_id=current_subscription.provider_auto_payment_charge_id,
                )
                if not payment:
                    current_subscription.status = SubscriptionStatus.FINISHED
                    user.daily_limits = SUBSCRIPTION_FREE_LIMITS

                    await update_subscription(current_subscription.id, {'status': current_subscription.status})
                    batch.update(user_ref, {
                        'subscription_id': '',
                        'daily_limits': user.daily_limits,
                        'last_subscription_limit_update': current_date,
                        'edited_at': current_date,
                    })

                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user.interface_language_code).SUBSCRIPTION_END,
                        disable_notification=True,
                    )
            elif current_subscription.payment_method == PaymentMethod.STRIPE or current_subscription.payment_method == PaymentMethod.TELEGRAM_STARS:
                days_difference = (current_date - current_subscription.end_date).days
                if days_difference > 3:
                    current_subscription.status = SubscriptionStatus.FINISHED if current_subscription.status != SubscriptionStatus.CANCELED else current_subscription.status
                    user.daily_limits = SUBSCRIPTION_FREE_LIMITS

                    await update_subscription(current_subscription.id, {'status': current_subscription.status})
                    batch.update(user_ref, {
                        'subscription_id': '',
                        'daily_limits': user.daily_limits,
                        'last_subscription_limit_update': current_date,
                        'edited_at': current_date,
                    })

                    await bot.send_message(
                        chat_id=user.telegram_chat_id,
                        text=get_localization(user.interface_language_code).SUBSCRIPTION_END,
                        disable_notification=True,
                    )
        else:
            current_subscription.status = SubscriptionStatus.FINISHED if current_subscription.status != SubscriptionStatus.CANCELED else current_subscription.status
            user.daily_limits = SUBSCRIPTION_FREE_LIMITS

            await update_subscription(current_subscription.id, {'status': current_subscription.status})
            batch.update(user_ref, {
                'subscription_id': '',
                'daily_limits': user.daily_limits,
                'last_subscription_limit_update': current_date,
                'edited_at': current_date,
            })

            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user.interface_language_code).SUBSCRIPTION_END,
                disable_notification=True,
            )

        return user

    if current_subscription and current_subscription.product_id:
        product = await get_product(current_subscription.product_id)
        daily_limits = product.details.get('limits')
    else:
        daily_limits = SUBSCRIPTION_FREE_LIMITS
    batch.update(user_ref, {
        'daily_limits': daily_limits,
        'edited_at': current_date,
    })

    return user


async def update_user_additional_usage_quota(bot: Bot, user: User, had_subscription: bool, batch: AsyncWriteBatch):
    need_update = False

    count_active_packages_before = 0
    for quota in [Quota.VOICE_MESSAGES, Quota.FAST_MESSAGES, Quota.ACCESS_TO_CATALOG]:
        if user.additional_usage_quota.get(quota) and not user.subscription_id:
            user.additional_usage_quota[quota] = False
            count_active_packages_before += 1
            need_update = True

    if need_update:
        user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user.id)
        current_date = datetime.now(timezone.utc)

        packages = await get_packages_by_user_id(user.id)
        count_active_packages_after = 0
        for package in packages:
            product = await get_product(package.product_id)
            if product.details.get('is_recurring', False) and package.until_at > current_date:
                user.additional_usage_quota[Quota.VOICE_MESSAGES] = True
                count_active_packages_after += 1

        if not user.additional_usage_quota[Quota.VOICE_MESSAGES]:
            user.settings[user.current_model][UserSettings.TURN_ON_VOICE_MESSAGES] = False

        if not user.additional_usage_quota[Quota.ACCESS_TO_CATALOG]:
            await reset_user_chats(user, bot)

        batch.update(user_ref, {
            'additional_usage_quota': user.additional_usage_quota,
            'settings': user.settings,
            'edited_at': current_date,
        })

        if not had_subscription and count_active_packages_before > count_active_packages_after:
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=get_localization(user.interface_language_code).PACKAGES_END,
                disable_notification=True,
            )


async def reset_user_chats(user: User, bot: Bot):
    chats = await get_chats_by_user_id(user.id)

    need_to_send_message = False
    for chat in chats:
        if chat.role != DEFAULT_ROLE:
            await update_chat(chat.id, {
                'role': DEFAULT_ROLE,
            })
            need_to_send_message = True

    if need_to_send_message:
        await bot.send_message(
            chat_id=user.telegram_chat_id,
            text=get_localization(user.interface_language_code).CHATS_RESET,
            disable_notification=True,
        )
