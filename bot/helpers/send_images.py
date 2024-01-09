import logging
import uuid
from typing import List

from aiogram.types import Message, InputMediaPhoto, URLInputFile


async def send_images(message: Message, images: List[str]):
    for i in range(0, len(images), 10):
        sliced_images = images[i:i + 10]
        try:
            media_group = [InputMediaPhoto(media=img) for img in sliced_images]
            await message.reply_media_group(media=media_group)
        except Exception as e:
            logging.error(f'Ошибка при отправке изображений: {e}')
            for j in range(len(sliced_images)):
                try:
                    await message.reply_photo(photo=URLInputFile(sliced_images[j], filename=f'{uuid.uuid4()}'))
                except Exception as e:
                    logging.error(f'Ошибка при отправке изображения: {e}')
