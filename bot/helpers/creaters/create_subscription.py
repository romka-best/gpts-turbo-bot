from datetime import datetime, timezone

from aiogram import Bot
from google.cloud import firestore

from bot.database.models.subscription import SubscriptionStatus
from bot.database.operations.product.getters import get_product
from bot.database.operations.subscription.getters import get_subscription, get_subscriptions_by_user_id
from bot.database.operations.subscription.updaters import update_subscription_in_transaction
from bot.database.operations.user.getters import get_user
from bot.database.operations.user.updaters import update_user_in_transaction
from bot.helpers.billing.unsubscribe import unsubscribe


@firestore.async_transactional
async def create_subscription(
    transaction,
    bot: Bot,
    subscription_id: str,
    user_id: str,
    income_amount: float,
    provider_payment_charge_id: str,
    provider_auto_payment_charge_id: str,
):
    user = await get_user(user_id)
    subscription = await get_subscription(subscription_id)
    product = await get_product(subscription.product_id)
    all_subscriptions = await get_subscriptions_by_user_id(user_id)

    for old_subscription in all_subscriptions:
        if old_subscription.id != subscription.id and old_subscription.status == SubscriptionStatus.ACTIVE:
            await unsubscribe(transaction, old_subscription, bot)

    subscription.status = SubscriptionStatus.ACTIVE
    await update_subscription_in_transaction(transaction, subscription_id, {
        'status': subscription.status,
        'provider_payment_charge_id': provider_payment_charge_id,
        'provider_auto_payment_charge_id': provider_auto_payment_charge_id,
        'income_amount': income_amount,
    })

    user.daily_limits.update(product.details.get('limits'))
    await update_user_in_transaction(transaction, user_id, {
        'subscription_id': subscription.id,
        'daily_limits': user.daily_limits,
        'additional_usage_quota': user.additional_usage_quota,
        'last_subscription_limit_update': datetime.now(timezone.utc),
    })
