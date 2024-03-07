from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionStatus


async def create_subscription_object(
    user_id: str,
    type: SubscriptionType,
    period: SubscriptionPeriod,
    status: SubscriptionStatus,
    currency: Currency,
    amount: float,
) -> Subscription:
    subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document()
    return Subscription(
        id=subscription_ref.id,
        user_id=user_id,
        type=type,
        period=period,
        status=status,
        currency=currency,
        amount=amount
    )
