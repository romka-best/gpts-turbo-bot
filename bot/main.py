import asyncio
import logging

import aiocron
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from bot.handlers.catalog_handler import catalog_router
from bot.handlers.chat_gpt_handler import chat_gpt_router
from bot.handlers.chats_handler import chats_router
from bot.handlers.common_handler import common_router
from bot.handlers.dalle_handler import dalle_router
from bot.handlers.face_swap_handler import face_swap_router
from bot.handlers.feedback_handler import feedback_router
from bot.handlers.language_handler import language_router
from bot.handlers.mode_handler import mode_router
from bot.handlers.payment_handler import payment_router, update_monthly_limits
from bot.handlers.profile_handler import profile_router
from bot.handlers.promo_code_handler import promo_code_router
from bot.handlers.settings_handler import settings_router
from bot.handlers.statistics_handler import statistics_router
from bot.handlers.voice_handler import voice_router
from config import config

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(), sm_strategy=FSMStrategy.GLOBAL_USER)


@aiocron.crontab('0 0 * * *')
async def daily_tasks():
    await update_monthly_limits(bot)


async def main() -> None:
    dp.include_routers(
        common_router,
        catalog_router,
        chats_router,
        feedback_router,
        language_router,
        mode_router,
        payment_router,
        profile_router,
        promo_code_router,
        settings_router,
        statistics_router,
        voice_router,
        chat_gpt_router,
        dalle_router,
        face_swap_router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
