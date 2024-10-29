import logging
import uuid

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import URLInputFile

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


async def send_document(
    bot: Bot,
    chat_id: str,
    document: str,
    reply_markup=None,
    caption=None,
    reply_to_message_id=None,
):
    try:
        extension = document.rsplit('.', 1)[-1]
        await bot.send_document(
            chat_id=chat_id,
            document=URLInputFile(document, filename=f'{uuid.uuid4()}.{extension}', timeout=60),
            reply_markup=reply_markup,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=True,
        )
    except TelegramForbiddenError:
        await update_user(chat_id, {
            'is_blocked': True,
        })
    except Exception as e:
        logging.error(f'Error in send_document: {e}')

        await bot.send_message(
            chat_id=chat_id,
            reply_markup=reply_markup,
            text=document,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=True,
        )

        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=['document'],
        )
