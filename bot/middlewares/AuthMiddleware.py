from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.database.operations.user.getters import get_user


class AuthMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ):
        user = await get_user(str(message.from_user.id))
        if user and user.is_banned:
            await message.answer_sticker(
                'CAACAgIAAxkBAAEMMIJmT_yFTm_LmNvCrZXeEK7t-fdSfAACSQIAAladvQoqlwydCFMhDjUE'
            )
            return

        await handler(message, data)


class AuthCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        callback_query: CallbackQuery,
        data: Dict[str, Any],
    ):
        user = await get_user(str(callback_query.from_user.id))
        if user and user.is_banned:
            await callback_query.message.answer_sticker(
                'CAACAgIAAxkBAAEMMIJmT_yFTm_LmNvCrZXeEK7t-fdSfAACSQIAAladvQoqlwydCFMhDjUE'
            )
            return

        await handler(callback_query, data)
