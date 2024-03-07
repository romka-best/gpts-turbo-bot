from typing import Optional, Literal

from aiogram.types import Message, InlineKeyboardMarkup, BufferedInputFile

from bot.database.models.common import Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.transaction.writers import write_transaction
from bot.integrations.openAI import get_response_text_to_speech


async def reply_with_voice(
    message: Message,
    text: str,
    user_id: str,
    reply_markup: Optional[InlineKeyboardMarkup],
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
):
    audio_content = await get_response_text_to_speech(text, voice)

    total_price = 0.000015 * len(text)
    await write_transaction(
        user_id=user_id,
        type=TransactionType.EXPENSE,
        service=ServiceType.VOICE_MESSAGES,
        amount=total_price,
        currency=Currency.USD,
        quantity=1,
        details={
            'subtype': 'TTS',
            'text': text,
        },
    )

    await message.answer_voice(
        voice=BufferedInputFile(audio_content.read(), filename='answer.ogg'),
        reply_markup=reply_markup,
    )
