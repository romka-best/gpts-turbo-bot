import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from aiogram.exceptions import TelegramForbiddenError
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from bot.config import config
from bot.database.main import firebase
from bot.database.operations.user import update_user
from bot.handlers.catalog_handler import catalog_router
from bot.handlers.chat_gpt_handler import chat_gpt_router
from bot.handlers.chats_handler import chats_router
from bot.handlers.common_handler import common_router
from bot.handlers.dalle_handler import dalle_router
from bot.handlers.face_swap_handler import face_swap_router
from bot.handlers.feedback_handler import feedback_router
from bot.handlers.language_handler import language_router
from bot.handlers.mode_handler import mode_router
from bot.handlers.payment_handler import payment_router
from bot.handlers.photo_handler import photo_router
from bot.handlers.profile_handler import profile_router
from bot.handlers.promo_code_handler import promo_code_router
from bot.handlers.settings_handler import settings_router
from bot.handlers.statistics_handler import statistics_router
from bot.handlers.text_handler import text_router
from bot.handlers.voice_handler import voice_router
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.helpers.update_daily_limits import update_monthly_limits

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
    yield
    await bot.session.close()
    await firebase.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    try:
        await dp.feed_update(bot=bot, update=telegram_update)
    except TelegramForbiddenError:
        user_id = None
        if telegram_update.callback_query and telegram_update.callback_query.message.from_user.id:
            user_id = str(telegram_update.callback_query.message.from_user.id)
        elif telegram_update.message and telegram_update.message.from_user.id:
            user_id = str(telegram_update.message.from_user.id)

        if user_id:
            await update_user(user_id, {
                "is_blocked": True
            })
    except Exception as e:
        logging.exception(f"Error in bot_webhook: {e}")


@app.get("/run-daily-tasks")
async def daily_tasks():
    await update_monthly_limits(bot)

    message = "Daily tasks executed successfully"
    await send_message_to_admins(bot, f'<b>{message}</b> 🎉')

    return {
        "code": 200,
        "message": message,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 8080))
