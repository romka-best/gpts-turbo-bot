from datetime import datetime, timezone
from typing import List, Optional, Dict

from google.cloud.firestore import Query

from bot.database.main import firebase
from bot.database.models.message import Message


async def get_message(message_id: str) -> Optional[Message]:
    message_ref = firebase.db.collection("messages").document(message_id)
    message = await message_ref.get()

    if message.exists:
        message_dict = message.to_dict()
        return Message(
            id=message_dict.get('id'),
            chat_id=message_dict.get('chat_id'),
            sender=message_dict.get('sender'),
            sender_id=message_dict.get('sender_id'),
            content=message_dict.get('content'),
            is_in_context=message_dict.get('is_in_context'),
            photo_filename=message_dict.get('photo_filename'),
            created_at=message_dict.get('created_at'),
            edited_at=message_dict.get('edited_at'),
        )


async def get_messages() -> List[Message]:
    messages = firebase.db.collection("messages").stream()

    return [
        Message(
            id=message.to_dict().get('id'),
            chat_id=message.to_dict().get('chat_id'),
            sender=message.to_dict().get('sender'),
            sender_id=message.to_dict().get('sender_id'),
            content=message.to_dict().get('content'),
            is_in_context=message.to_dict().get('is_in_context'),
            photo_filename=message.to_dict().get('photo_filename'),
            created_at=message.to_dict().get('created_at'),
            edited_at=message.to_dict().get('edited_at'),
        ) async for message in messages
    ]


async def get_messages_by_chat_id(chat_id: str, limit=10, is_in_context=True) -> List[Message]:
    messages_query = firebase.db.collection("messages").where("chat_id", "==", chat_id)
    if is_in_context is not None:
        messages_query = messages_query.where("is_in_context", "==", is_in_context)
    if limit > 0:
        messages_query = messages_query.limit(limit)
    messages_stream = messages_query.order_by("created_at", direction=Query.DESCENDING).stream()

    messages = [
        Message(
            id=message.to_dict().get('id'),
            chat_id=message.to_dict().get('chat_id'),
            sender=message.to_dict().get('sender'),
            sender_id=message.to_dict().get('sender_id'),
            content=message.to_dict().get('content'),
            is_in_context=message.to_dict().get('is_in_context'),
            photo_filename=message.to_dict().get('photo_filename'),
            created_at=message.to_dict().get('created_at'),
            edited_at=message.to_dict().get('edited_at'),
        )
        async for message in messages_stream
    ]

    return messages


async def create_message_object(
    chat_id: str,
    sender: str,
    sender_id: str,
    content: str,
    is_in_context=True,
    photo_filename=None,
) -> Message:
    message_ref = firebase.db.collection('messages').document()

    return Message(
        id=message_ref.id,
        chat_id=chat_id,
        sender=sender,
        sender_id=sender_id,
        content=content,
        is_in_context=is_in_context,
        photo_filename=photo_filename,
    )


async def write_message(
    chat_id: str,
    sender: str,
    sender_id: str,
    content: str,
    is_in_context=True,
    photo_filename=None,
) -> Message:
    message = await create_message_object(chat_id, sender, sender_id, content, is_in_context, photo_filename)
    await firebase.db.collection('messages').document(message.id).set(message.to_dict())

    return message


async def write_message_in_transaction(
    transaction,
    chat_id: str,
    sender: str,
    sender_id: str,
    content: str,
    is_in_context=True,
    photo_filename=None,
) -> Message:
    message = await create_message_object(chat_id, sender, sender_id, content, is_in_context, photo_filename)
    transaction.set(firebase.db.collection('messages').document(message.id), message.to_dict())

    return message


async def update_message(message_id: str, data: Dict) -> None:
    message_ref = firebase.db.collection('messages').document(message_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await message_ref.update(data)
