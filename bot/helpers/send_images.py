from typing import List

from aiogram.types import Message, InputMediaPhoto


async def send_images(message: Message, images: List[str]):
    for i in range(0, len(images), 10):
        media_group = [InputMediaPhoto(media=img) for img in images[i:i + 10]]
        await message.reply_media_group(media=media_group)
