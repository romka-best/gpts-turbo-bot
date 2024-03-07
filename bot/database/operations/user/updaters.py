from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.user import User


async def update_user(user_id: str, data: Dict):
    user_ref = firebase.db.collection(User.COLLECTION_NAME).document(user_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await user_ref.update(data)


async def update_user_in_transaction(transaction, user_id: str, data: Dict):
    data['edited_at'] = datetime.now(timezone.utc)

    transaction.update(firebase.db.collection(User.COLLECTION_NAME).document(user_id), data)
