from aiogram import Bot
from google.cloud.firestore_v1 import DELETE_FIELD

from bot.database.operations.request.getters import get_requests
from bot.database.operations.request.updaters import update_request
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def migrate(bot: Bot):
    requests = await get_requests()
    for request in requests:
        await update_request(request.id, {
            'processing_message_ids': [request.message_id],
        })

    requests = await get_requests()
    for request in requests:
        await update_request(request.id, {
            'message_id': DELETE_FIELD,
        })

    await send_message_to_admins_and_developers(
        bot, '<b>Database Migration Was Successful!</b> 🎉',
    )
