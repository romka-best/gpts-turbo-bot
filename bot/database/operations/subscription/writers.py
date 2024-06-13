from typing import Optional

from bot.database.main import firebase
from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionStatus
from bot.database.operations.subscription.helpers import create_subscription_object


async def write_subscription(
    subscription_id: Optional[str],
    user_id: str,
    type: SubscriptionType,
    period: SubscriptionPeriod,
    status: SubscriptionStatus,
    currency: Currency,
    amount: float,
    income_amount: float,
    payment_method: PaymentMethod,
    provider_payment_charge_id: Optional[str],
) -> Subscription:
    subscription = await create_subscription_object(
        subscription_id,
        user_id,
        type,
        period,
        status,
        currency,
        amount,
        income_amount,
        payment_method,
        provider_payment_charge_id,
    )

    await firebase.db.collection(Subscription.COLLECTION_NAME).document(subscription.id).set(subscription.to_dict())

    return subscription
