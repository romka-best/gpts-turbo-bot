import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter, TelegramNetworkError, TelegramBadRequest

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


async def delayed_send_sticker(bot: Bot, chat_id: str, sticker_id: str, timeout: int):
    await asyncio.sleep(timeout)

    try:
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker_id,
            disable_notification=True,
        )
    except TelegramForbiddenError:
        asyncio.create_task(update_user(chat_id, {'is_blocked': True}))
    except TelegramRetryAfter as e:
        asyncio.create_task(delayed_send_sticker(bot, chat_id, sticker_id, e.retry_after + 30))
    except TelegramNetworkError as error:
        logging.error(error)
    except TelegramBadRequest as error:
        logging.error(error)


async def send_sticker(
    bot: Bot,
    chat_id: str,
    sticker_id: str,
):
    try:
        await bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker_id,
            disable_notification=True,
        )
    except TelegramForbiddenError:
        await update_user(chat_id, {
            'is_blocked': True,
        })
    except TelegramRetryAfter as e:
        asyncio.create_task(delayed_send_sticker(bot, chat_id, sticker_id, e.retry_after + 30))
    except TelegramNetworkError:
        asyncio.create_task(delayed_send_sticker(bot, chat_id, sticker_id, 60))
    except TelegramBadRequest as error:
        logging.error(error)
    except Exception as e:
        logging.error(f'Error in send_sticker: {e}')

        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=['sticker']
        )
