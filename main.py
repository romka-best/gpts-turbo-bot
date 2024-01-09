import logging
import os
from contextlib import asynccontextmanager

import uvicorn
import aiocron
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from bot.config import config
from bot.database.main import firebase
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
from bot.handlers.photo_handler import photo_router
from bot.handlers.profile_handler import profile_router
from bot.handlers.promo_code_handler import promo_code_router
from bot.handlers.settings_handler import settings_router
from bot.handlers.statistics_handler import statistics_router
from bot.handlers.text_handler import text_router
from bot.handlers.voice_handler import voice_router

WEBHOOK_PATH = f"/bot/{config.BOT_TOKEN.get_secret_value()}"
WEBHOOK_URL = config.WEBHOOK_URL + WEBHOOK_PATH

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
storage = RedisStorage.from_url(config.REDIS_URL)
dp = Dispatcher(storage=storage, sm_strategy=FSMStrategy.GLOBAL_USER)


@asynccontextmanager
async def lifespan(_: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

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
        chat_gpt_router,
        dalle_router,
        face_swap_router,
        photo_router,
        voice_router,
        text_router,
    )

    await firebase.init()
    await daily_tasks()
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    try:
        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
    except Exception as e:
        logging.exception(f"Error in bot_webhook: {e}")


async def daily_tasks():
    await update_monthly_limits(bot)


aiocron.crontab('0 0 * * *', func=daily_tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
