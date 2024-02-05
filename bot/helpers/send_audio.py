import logging

from aiogram import Bot
from aiogram.types import URLInputFile


async def send_audio(bot: Bot,
                     chat_id: str,
                     result: str,
                     caption: str,
                     filename: str,
                     duration: int,
                     reply_markup=None):
    try:
        await bot.send_audio(
            chat_id=chat_id,
            audio=URLInputFile(result, filename=filename),
            caption=caption,
            duration=duration,
            reply_markup=reply_markup,
        )
    except Exception as e:
        logging.error(f'Error in send_audio: {e}')
