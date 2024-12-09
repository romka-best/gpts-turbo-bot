import asyncio
import logging
import traceback

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter
from aiogram import Bot

from bot.config import config


async def delayed_send_message_to_developers(
    bot: Bot,
    chat_id: str,
    text: str,
    parse_mode: str,
    timeout: int,
):
    await asyncio.sleep(timeout)

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
        )
    except (TelegramBadRequest, TelegramForbiddenError) as error:
        logging.error(error)
    except TelegramRetryAfter as e:
        asyncio.create_task(
            delayed_send_message_to_developers(bot, chat_id, text, parse_mode, e.retry_after + 30)
        )
    except Exception:
        error_trace = traceback.format_exc()
        logging.exception(f'Error in delayed_send_message_to_developers: {error_trace}')


async def send_message_to_developers(bot: Bot, message: str, parse_mode='HTML'):
    for chat_id in config.DEVELOPER_IDS:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )
        except (TelegramBadRequest, TelegramForbiddenError) as error:
            logging.error(error)
        except TelegramRetryAfter as e:
            asyncio.create_task(
                delayed_send_message_to_developers(bot, chat_id, message, parse_mode, e.retry_after + 30)
            )
        except Exception:
            error_trace = traceback.format_exc()
            logging.exception(f'Error in send_message_to_developers: {error_trace}')
