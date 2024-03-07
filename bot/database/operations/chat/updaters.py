from datetime import datetime, timezone
from typing import Dict

from bot.database.main import firebase
from bot.database.models.chat import Chat


async def update_chat(chat_id: str, data: Dict) -> None:
    chat_ref = firebase.db.collection(Chat.COLLECTION_NAME).document(chat_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await chat_ref.update(data)
