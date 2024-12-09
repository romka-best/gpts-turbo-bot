import asyncio

from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError, TelegramRetryAfter
from aiogram.types import Message
from aiohttp import ClientOSError
from chatgpt_md_converter import telegram_format
from redis.exceptions import ConnectionError

from bot.config import config
from bot.helpers.split_message import split_message


async def delayed_send_ai_message(message: Message, text: str, timeout: int, reply_markup=None):
    await asyncio.sleep(timeout)

    try:
        await message.reply(
            text=text,
            reply_markup=reply_markup,
            allow_sending_without_reply=True,
        )
    except TelegramRetryAfter as e:
        asyncio.create_task(delayed_send_ai_message(message, text, e.retry_after + 30, reply_markup))


async def send_ai_message(message: Message, text: str, reply_markup=None):
    formatted_text = telegram_format(text)

    messages = split_message(formatted_text)
    for i in range(len(messages)):
        formatted_message = messages[i]
        try:
            for j in range(config.MAX_RETRIES):
                try:
                    await message.reply(
                        text=formatted_message,
                        reply_markup=reply_markup if i == len(messages) - 1 else None,
                        allow_sending_without_reply=True,
                    )
                    break
                except (ConnectionResetError, OSError, ClientOSError, ConnectionError, TelegramNetworkError) as e:
                    if j == config.MAX_RETRIES - 1:
                        raise e
                    continue
        except TelegramRetryAfter as e:
            asyncio.create_task(
                delayed_send_ai_message(
                    message,
                    formatted_message,
                    e.retry_after + 30,
                    reply_markup if i == len(messages) - 1 else None,
                )
            )
        except TelegramBadRequest as e:
            if e.message.startswith('Bad Request: can\'t parse entities'):
                await message.reply(
                    text=formatted_message,
                    reply_markup=reply_markup if i == len(messages) - 1 else None,
                    allow_sending_without_reply=True,
                    parse_mode=None,
                )
            elif (
                e.message.startswith('Bad Request: message text is empty') or
                e.message.startswith('Bad Request: text must be non-empty')
            ):
                pass
            elif e.message.startswith('Bad Request: message is too long'):
                await message.reply(
                    text=formatted_message[:4096],
                    reply_markup=reply_markup if i == len(messages) - 1 else None,
                    allow_sending_without_reply=True,
                    parse_mode=None,
                )
            else:
                raise e
