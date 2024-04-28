import logging
import uuid
from typing import List

from aiogram import Bot
from aiogram.types import InputMediaPhoto, URLInputFile

from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def send_image(bot: Bot, chat_id: str, image: str, reply_markup=None, caption=None, reply_to_message_id=None):
    try:
        await bot.send_photo(
            chat_id=chat_id,
            photo=URLInputFile(image, filename=f'{uuid.uuid4()}', timeout=60),
            reply_markup=reply_markup,
            caption=caption,
            reply_to_message_id=reply_to_message_id,
        )
    except Exception as e:
        logging.error(f'Error in send_image: {e}')
        await send_message_to_admins(
            bot=bot,
            message=f"#error\n\nALARM! Ошибка при отправке изображения у пользователя: {chat_id}\n"
                    f"Информация:\n{e}",
            parse_mode=None,
        )


async def send_images(bot: Bot, chat_id: str, images: List[str]):
    for i in range(0, len(images), 10):
        sliced_images = images[i:i + 10]
        try:
            media_group = [InputMediaPhoto(media=img) for img in sliced_images]
            await bot.send_media_group(chat_id=chat_id, media=media_group)
        except Exception as e:
            logging.error(f'Error in send_images: {e}')
            for j in range(len(sliced_images)):
                try:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=URLInputFile(sliced_images[j], filename=f'{uuid.uuid4()}'),
                    )
                except Exception as e:
                    logging.error(f'Error in send_images with second try: {e}')
                    await send_message_to_admins(
                        bot=bot,
                        message=f"#error\n\nALARM! Ошибка при отправке изображения у пользователя: {chat_id}\n"
                                f"Информация:\n{e}",
                        parse_mode=None,
                    )
