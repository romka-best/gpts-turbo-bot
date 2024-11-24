import logging
import uuid

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InputMediaPhoto, URLInputFile

from bot.database.operations.user.updaters import update_user
from bot.helpers.senders.send_error_info import send_error_info


async def send_image(bot: Bot, chat_id: str, image: str, reply_markup=None, caption=None, reply_to_message_id=None):
    try:
        extension = image.rsplit('.', 1)[-1]
        await bot.send_photo(
            chat_id=chat_id,
            photo=URLInputFile(image, filename=f'{uuid.uuid4()}.{extension}', timeout=60),
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
        logging.error(f'Error in send_image: {e}')

        await bot.send_message(
            chat_id=chat_id,
            reply_markup=reply_markup,
            text=image,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=True,
        )

        await send_error_info(
            bot=bot,
            user_id=chat_id,
            info=str(e),
            hashtags=['image'],
        )


async def send_images(bot: Bot, chat_id: str, images: list[str]):
    for i in range(0, len(images), 10):
        sliced_images = images[i:i + 10]
        try:
            media_group = [InputMediaPhoto(media=img) for img in sliced_images]
            await bot.send_media_group(chat_id=chat_id, media=media_group)
        except TelegramForbiddenError:
            await update_user(chat_id, {
                'is_blocked': True,
            })
        except Exception as e:
            logging.error(f'Error in send_images: {e}')
            for j in range(len(sliced_images)):
                try:
                    image = sliced_images[j]
                    extension = image.rsplit('.', 1)[-1]
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=URLInputFile(image, filename=f'{uuid.uuid4()}.{extension}'),
                    )
                except Exception as e:
                    logging.error(f'Error in send_images with second try: {e}')
                    await send_error_info(
                        bot=bot,
                        user_id=chat_id,
                        info=str(e),
                        hashtags=['image'],
                    )
