from aiogram import Bot

from bot.handlers.admin.statistics_handler import handle_get_statistics
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def send_admin_statistics(bot: Bot, period='day'):
    text = await handle_get_statistics('ru', period)
    await send_message_to_admins(bot, text)
