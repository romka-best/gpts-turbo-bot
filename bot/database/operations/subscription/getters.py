from typing import Optional

from google.cloud.firestore_v1 import FieldFilter, Query

from bot.database.main import firebase
from bot.database.models.subscription import Subscription


async def get_subscription(subscription_id: str) -> Optional[Subscription]:
    subscription_ref = firebase.db.collection(Subscription.COLLECTION_NAME).document(str(subscription_id))
    subscription = await subscription_ref.get()

    if subscription.exists:
        return Subscription(**subscription.to_dict())


async def get_last_subscription_by_user_id(user_id: str) -> Optional[Subscription]:
    subscription_stream = firebase.db.collection(Subscription.COLLECTION_NAME) \
        .where(filter=FieldFilter("user_id", "==", user_id)) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(1) \
        .stream()

    async for doc in subscription_stream:
        return Subscription(**doc.to_dict())
