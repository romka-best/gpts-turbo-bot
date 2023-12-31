from typing import List, Optional

from google.cloud.firestore import Query

from bot.database.main import db
from bot.database.models.message import Message


async def get_message(message_id: str) -> Optional[Message]:
    message_ref = db.collection("messages").document(message_id)
    message = await message_ref.get()

    if message.exists:
        return Message(**message.to_dict())


async def get_messages_by_chat_id(chat_id: str) -> List[Message]:
    messages_stream = db.collection("messages") \
        .where("chat_id", "==", chat_id) \
        .order_by("created_at", direction=Query.DESCENDING) \
        .limit(10) \
        .stream()
    messages = [Message(**message.to_dict()) async for message in messages_stream]

    return messages


async def create_message_object(chat_id: str, sender: str, sender_id: str, content: str) -> Message:
    message_ref = db.collection('messages').document()

    return Message(
        id=message_ref.id,
        chat_id=chat_id,
        sender=sender,
        sender_id=sender_id,
        content=content
    )


async def write_message(chat_id: str, sender: str, sender_id: str, content: str) -> Message:
    message = await create_message_object(chat_id, sender, sender_id, content)
    await db.collection('messages').document(message.id).set(message.to_dict())

    return message


async def write_message_in_transaction(transaction, chat_id: str, sender: str, sender_id: str, content: str) -> Message:
    message = await create_message_object(chat_id, sender, sender_id, content)
    transaction.set(db.collection('messages').document(message.id), message.to_dict())

    return message
