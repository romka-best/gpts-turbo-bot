import asyncio
import logging

from aiogram import Bot

from bot.database.operations.message import get_messages, update_message
from bot.helpers.send_message_to_admins import send_message_to_admins


async def migration_messages(bot: Bot):
    try:
        logging.info("START_MIGRATION_MESSAGES")

        messages = await get_messages()
        tasks = []
        for message in messages:
            tasks.append(
                update_message(
                    message.id,
                    {
                        "is_in_context": True,
                    }
                )
            )
        await asyncio.gather(*tasks)

        await send_message_to_admins(bot, "<b>The database migration with messages was successful!</b> 🎉")
    except Exception as e:
        logging.exception("Error in migration_messages", e)
        await send_message_to_admins(bot, "<b>The database migration with messages was not successful!</b> 🚨")
    finally:
        logging.info("END_MIGRATION_MESSAGES")
