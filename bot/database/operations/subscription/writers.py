from bot.database.main import firebase
from bot.database.models.common import Currency
from bot.database.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod, SubscriptionStatus
from bot.database.operations.subscription.helpers import create_subscription_object


async def write_subscription(
    user_id: str,
    type: SubscriptionType,
    period: SubscriptionPeriod,
    status: SubscriptionStatus,
    currency: Currency,
    amount: float,
) -> Subscription:
    subscription = await create_subscription_object(user_id, type, period, status, currency, amount)
    await firebase.db.collection(Subscription.COLLECTION_NAME).document(subscription.id).set(subscription.to_dict())

    return subscription
