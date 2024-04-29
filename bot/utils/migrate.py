import asyncio
import logging

from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.database.main import firebase
from bot.database.models.message import Message
from bot.database.operations.message.updaters import update_message
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def migrate(bot: Bot):
    logging.info("START_MIGRATION")

    try:
        tasks = []

        messages = firebase.db.collection(Message.COLLECTION_NAME).stream()
        async for message in messages:
            message_id, content, photo_filename = (
                message.to_dict().get('id'),
                message.to_dict().get('content'),
                message.to_dict().get('photo_filename')
            )
            tasks.append(
                update_message(
                    message_id,
                    {
                        "content": content if content else "",
                        "photo_filenames": [photo_filename] if photo_filename else [],
                        "photo_filename": DELETE_FIELD,
                    }
                )
            )

        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration", e)
        await send_message_to_admins(bot, "<b>The database migration was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION")
