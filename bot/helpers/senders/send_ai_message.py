from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from chatgpt_md_converter import telegram_format

from bot.helpers.split_message import split_message


async def send_ai_message(message: Message, text: str, reply_markup=None):
    formatted_text = telegram_format(text)
    try:
        if len(text) > 4096:
            messages = split_message(text)
            for i in range(len(messages)):
                formatted_message = telegram_format(messages[i])
                try:
                    await message.reply(
                        text=formatted_message,
                        reply_markup=reply_markup if i == len(messages) - 1 else None,
                        allow_sending_without_reply=True,
                    )
                except TelegramBadRequest as e:
                    if e.message.startswith('Bad Request: can\'t parse entities'):
                        await message.reply(
                            text=messages[i],
                            reply_markup=reply_markup,
                            allow_sending_without_reply=True,
                        )
                    else:
                        raise e
        else:
            await message.reply(
                text=formatted_text,
                reply_markup=reply_markup,
                allow_sending_without_reply=True,
            )
    except TelegramBadRequest as e:
        if e.message.startswith('Bad Request: can\'t parse entities'):
            await message.reply(
                text=text,
                reply_markup=reply_markup,
                allow_sending_without_reply=True,
            )
        else:
            raise e
