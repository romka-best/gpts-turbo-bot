import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import URLInputFile

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


async def send_audio(
    bot: Bot,
    chat_id: str,
    result: str,
    caption: str,
    filename: str,
    duration: int,
    reply_markup=None,
    reply_to_message_id=None,
):
    try:
        await bot.send_audio(
            chat_id=chat_id,
            audio=URLInputFile(result, filename=filename, timeout=60),
            caption=caption,
            duration=duration,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )
    except TelegramForbiddenError:
        await update_user(chat_id, {
            "is_blocked": True,
        })
    except Exception as e:
        logging.error(f'Error in send_audio: {e}')
        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=["audio"]
        )
