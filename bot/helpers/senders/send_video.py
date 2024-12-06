import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import URLInputFile

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


async def send_video(
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
        await bot.send_video(
            chat_id=chat_id,
            video=URLInputFile(result, filename=filename, timeout=300),
            caption=caption,
            duration=duration,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=True,
        )
    except TelegramForbiddenError:
        await update_user(chat_id, {
            'is_blocked': True,
        })
    except Exception as e:
        logging.error(f'Error in send_video: {e}')

        await bot.send_message(
            chat_id=chat_id,
            reply_markup=reply_markup,
            text=result,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=True,
        )

        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=['video']
        )
