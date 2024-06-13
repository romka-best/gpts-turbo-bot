from typing import Optional

from bot.database.main import firebase
from bot.database.models.common import Currency, PaymentMethod
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionStatus


async def create_subscription_object(
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
    subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document(subscription_id)
    return Subscription(
        id=subscription_ref.id,
        user_id=user_id,
        type=type,
        period=period,
        status=status,
        currency=currency,
        amount=amount,
        income_amount=income_amount,
        payment_method=payment_method,
        provider_payment_charge_id=provider_payment_charge_id,
    )
