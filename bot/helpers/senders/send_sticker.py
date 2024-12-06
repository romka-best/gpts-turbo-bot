import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


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
    except Exception as e:
        logging.error(f'Error in send_sticker: {e}')

        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=['sticker']
        )
