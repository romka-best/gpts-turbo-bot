from bot.database.main import firebase
from bot.database.models.message import Message


async def create_message_object(
    chat_id: str,
    sender: str,
    sender_id: str,
    content: str,
    is_in_context=True,
    photo_filenames=None,
) -> Message:
    message_ref = firebase.db.collection(Message.COLLECTION_NAME).document()

    return Message(
        id=message_ref.id,
        chat_id=chat_id,
        sender=sender,
        sender_id=sender_id,
        content=content,
        is_in_context=is_in_context,
        photo_filenames=photo_filenames,
    )
