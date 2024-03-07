from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.message import Message


async def update_message(message_id: str, data: Dict) -> None:
    message_ref = firebase.db.collection(Message.COLLECTION_NAME).document(message_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await message_ref.update(data)
