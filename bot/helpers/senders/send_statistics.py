from aiogram import Bot

from bot.handlers.admin.statistics_handler import handle_get_statistics
from bot.helpers.senders.send_message_to_admins_and_developers import send_message_to_admins_and_developers


async def send_statistics(bot: Bot, period='day'):
    texts = await handle_get_statistics('ru', period)
    for text in texts:
        await send_message_to_admins_and_developers(bot, text)
