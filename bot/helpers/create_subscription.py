from datetime import datetime, timezone

from google.cloud import firestore

from bot.database.models.common import Quota
from bot.database.models.subscription import SubscriptionStatus, SubscriptionLimit
from bot.database.operations.subscription import get_subscription, update_subscription_in_transaction
from bot.database.operations.user import get_user, update_user_in_transaction


@firestore.async_transactional
async def create_subscription(transaction,
                              subscription_id: str,
                              user_id: str,
                              provider_payment_charge_id: str):
    user = await get_user(user_id)
    subscription = await get_subscription(subscription_id)

    await update_subscription_in_transaction(transaction, subscription_id, {
        "status": SubscriptionStatus.ACTIVE,
        "provider_payment_charge_id": provider_payment_charge_id,
    })

    user.monthly_limits.update(SubscriptionLimit.LIMITS[subscription.type])
    for key, value in SubscriptionLimit.ADDITIONAL_QUOTA_LIMITS[subscription.type].items():
        if key in user.additional_usage_quota and key == Quota.ADDITIONAL_CHATS:
            user.additional_usage_quota[key] += value
        else:
            user.additional_usage_quota[key] = value
    await update_user_in_transaction(transaction, user_id, {
        "subscription_type": subscription.type,
        "monthly_limits": user.monthly_limits,
        "additional_usage_quota": user.additional_usage_quota,
        "last_subscription_limit_update": datetime.now(timezone.utc),
    })
