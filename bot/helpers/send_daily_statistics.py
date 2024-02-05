from aiogram import Bot

from bot.handlers.statistics_handler import handle_get_statistics
from bot.helpers.send_message_to_admins import send_message_to_admins


async def send_daily_statistics(bot: Bot):
    text = await handle_get_statistics('ru', 'day')
    await send_message_to_admins(bot, text)
