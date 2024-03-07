from bot.database.main import firebase
from bot.database.models.chat import Chat


async def create_chat_object(user_id: str, telegram_chat_id: str, title: str) -> Chat:
    chat_ref = firebase.db.collection(Chat.COLLECTION_NAME).document()
    return Chat(
        id=chat_ref.id,
        user_id=user_id,
        telegram_chat_id=telegram_chat_id,
        title=title,
    )
