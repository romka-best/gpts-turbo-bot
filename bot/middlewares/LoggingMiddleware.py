import logging
from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class LoggingMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ):
        logging.info(f"Received message from {message.from_user.id}: {message.text}")
        await handler(message, data)


class LoggingCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        callback_query: CallbackQuery,
        data: Dict[str, Any],
    ):
        logging.info(f"Received callback_query from {callback_query.from_user.id}: {callback_query.data}")
        await handler(callback_query, data)
