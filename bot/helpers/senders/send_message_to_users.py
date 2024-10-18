import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter, TelegramForbiddenError, TelegramNetworkError

from bot.database.models.user import User
from bot.database.operations.user.getters import get_users_by_language_code
from bot.database.operations.user.updaters import update_user

BATCH_SIZE = 30
DELAY_SECONDS = 1


async def delayed_send_message_to_user(bot: Bot, chat_id: str, text: str, timeout: int):
    await asyncio.sleep(timeout)

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            disable_notification=True,
        )
    except TelegramForbiddenError:
        asyncio.create_task(update_user(chat_id, {'is_blocked': True}))
    except TelegramRetryAfter as e:
        await delayed_send_message_to_user(bot, chat_id, text, e.retry_after + 30)
    except TelegramNetworkError as error:
        logging.error(error)
    except TelegramBadRequest as error:
        logging.error(error)


async def send_message_to_user(bot: Bot, user: User, message: str):
    try:
        if not user.is_blocked:
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=message,
                disable_notification=True,
            )
    except TelegramForbiddenError:
        asyncio.create_task(update_user(user.id, {'is_blocked': True}))
    except TelegramRetryAfter as e:
        await delayed_send_message_to_user(bot, user.telegram_chat_id, message, e.retry_after + 30)
    except TelegramNetworkError:
        await delayed_send_message_to_user(bot, user.telegram_chat_id, message, 60)
    except TelegramBadRequest as error:
        logging.error(error)


async def send_message_to_users(bot: Bot, language_code: str, message: str):
    users = await get_users_by_language_code(language_code)
    for i in range(0, len(users), BATCH_SIZE):
        batch_users = users[i:i + BATCH_SIZE]

        tasks = [
            send_message_to_user(bot, user, message) for user in batch_users
        ]

        await asyncio.gather(*tasks)

        if i + BATCH_SIZE < len(users):
            await asyncio.sleep(DELAY_SECONDS)
