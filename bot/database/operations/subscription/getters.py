from datetime import datetime
from typing import Optional, List

from google.cloud.firestore_v1 import FieldFilter, Query

from bot.database.main import firebase
from bot.database.models.subscription import Subscription, SubscriptionStatus, SubscriptionType, SubscriptionPeriod


async def get_subscription(subscription_id: str) -> Optional[Subscription]:
    subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document(str(subscription_id))
    subscription = await subscription_ref.get()

    if subscription.exists:
        return Subscription(**subscription.to_dict())


async def get_last_subscription_by_user_id(user_id: str) -> Optional[Subscription]:
    subscription_stream = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .where(filter=FieldFilter("status", "not-in",
                                  [
                                      SubscriptionStatus.WAITING,
                                      SubscriptionStatus.ERROR,
                                      SubscriptionStatus.DECLINED,
                                  ])) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(1) \
        .stream()

    async for doc in subscription_stream:
        return Subscription(**doc.to_dict())


async def get_last_subscription_with_waiting_payment(
    user_id: str,
    subscription_type: SubscriptionType,
    subscription_period: SubscriptionPeriod,
) -> Optional[Subscription]:
    subscription_stream = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .where(filter=FieldFilter("status", "==", SubscriptionStatus.WAITING)) \
        .where(filter=FieldFilter("type", "==", subscription_type)) \
        .where(filter=FieldFilter("period", "==", subscription_period)) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(1) \
        .stream()

    async for doc in subscription_stream:
        return Subscription(**doc.to_dict())


async def get_subscriptions_by_user_id(user_id: str) -> List[Subscription]:
    subscriptions = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .stream()

    return [
        Subscription(**subscription.to_dict()) async for subscription in subscriptions
    ]


async def get_subscription_by_provider_payment_charge_id(provider_payment_charge_id: str) -> Optional[Subscription]:
    subscription_stream = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("provider_payment_charge_id", "==", provider_payment_charge_id)) \
        .limit(1) \
        .stream()

    async for doc in subscription_stream:
        return Subscription(**doc.to_dict())


async def get_subscription_by_provider_auto_payment_charge_id(
    provider_auto_payment_charge_id: str,
) -> Optional[Subscription]:
    subscription_stream = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("provider_auto_payment_charge_id", "==", provider_auto_payment_charge_id)) \
        .limit(1) \
        .stream()

    async for doc in subscription_stream:
        return Subscription(**doc.to_dict())


async def get_subscriptions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Subscription]:
    subscriptions_query = firebase.db.collection(Subscription.COLLECTION_NAME)

    if start_date:
        subscriptions_query = subscriptions_query.where(filter=FieldFilter("created_at", ">=", start_date))
    if end_date:
        subscriptions_query = subscriptions_query.where(filter=FieldFilter("created_at", "<=", end_date))

    subscriptions = subscriptions_query.stream()

    return [
        Subscription(**subscription.to_dict()) async for subscription in subscriptions
    ]


async def get_subscriptions_by_status(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: SubscriptionStatus = None,
) -> List[Subscription]:
    subscriptions_query = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("status", "==", status))

    if start_date:
        subscriptions_query = subscriptions_query.where(filter=FieldFilter("created_at", ">=", start_date))
    if end_date:
        subscriptions_query = subscriptions_query.where(filter=FieldFilter("created_at", "<=", end_date))

    subscriptions = subscriptions_query.stream()

    return [
        Subscription(**subscription.to_dict()) async for subscription in subscriptions
    ]
