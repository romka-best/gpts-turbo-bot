from datetime import datetime, timezone
from typing import Optional, Dict, List

from bot.database.main import firebase
from bot.database.models.chat import Chat
from bot.database.operations.user import get_user


async def get_chat(chat_id: str) -> Optional[Chat]:
    chat_ref = firebase.db.collection("chats").document(str(chat_id))
    chat = await chat_ref.get()

    if chat.exists:
        return Chat(**chat.to_dict())


async def get_chat_by_user_id(user_id: str) -> Optional[Chat]:
    user = await get_user(user_id)

    if user:
        chat = await get_chat(user.current_chat_id)
        return chat


async def get_chats(start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Chat]:
    chats_query = firebase.db.collection("chats")

    if start_date:
        chats_query = chats_query.where("created_at", ">=", start_date)
    if end_date:
        chats_query = chats_query.where("created_at", "<=", end_date)

    chats = chats_query.stream()
    return [Chat(**chat.to_dict()) async for chat in chats]


async def get_chats_by_user_id(user_id: str) -> List[Chat]:
    chats_query = firebase.db.collection('chats').where("user_id", "==", user_id)
    chats = [Chat(**chat.to_dict()) async for chat in chats_query.stream()]

    return chats


async def create_chat_object(user_id: str, telegram_chat_id: str, title) -> Chat:
    chat_ref = firebase.db.collection('chats').document()
    return Chat(id=chat_ref.id, user_id=user_id, telegram_chat_id=telegram_chat_id, title=title)


async def write_chat_in_transaction(transaction, user_id: str, telegram_chat_id: str, title) -> Chat:
    chat = await create_chat_object(user_id, telegram_chat_id, title)
    transaction.set(firebase.db.collection('chats').document(chat.id), chat.to_dict())

    return chat


async def update_chat(chat_id: str, data: Dict):
    chat_ref = firebase.db.collection('chats').document(chat_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await chat_ref.update(data)


async def delete_chat(chat_id: str):
    chat_ref = firebase.db.collection('chats').document(chat_id)
    await chat_ref.delete()
