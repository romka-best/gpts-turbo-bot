from bot.database.main import firebase
from bot.database.models.chat import Chat
from bot.database.operations.chat.helpers import create_chat_object


async def write_chat_in_transaction(transaction, user_id: str, telegram_chat_id: str, title: str) -> Chat:
    chat = await create_chat_object(user_id, telegram_chat_id, title)
    transaction.set(firebase.db.collection(Chat.COLLECTION_NAME).document(chat.id), chat.to_dict())

    return chat
