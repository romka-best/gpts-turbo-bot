import logging
import uuid
from typing import List

from aiogram import Bot
from aiogram.types import InputMediaPhoto, URLInputFile


async def send_images(bot: Bot, chat_id: str, images: List[str]):
    for i in range(0, len(images), 10):
        sliced_images = images[i:i + 10]
        try:
            media_group = [InputMediaPhoto(media=img) for img in sliced_images]
            await bot.send_media_group(chat_id=chat_id, media=media_group)
        except Exception as e:
            logging.error(f'Ошибка при отправке изображений: {e}')
            for j in range(len(sliced_images)):
                try:
                    await bot.send_photo(chat_id=chat_id,
                                         photo=URLInputFile(sliced_images[j], filename=f'{uuid.uuid4()}'))
                except Exception as e:
                    logging.error(f'Ошибка при отправке изображения: {e}')
