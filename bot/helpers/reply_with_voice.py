from typing import Optional

from aiogram.types import Message, InlineKeyboardMarkup

from bot.database.models.common import Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.operations.transaction import write_transaction
from bot.integrations.openAI import get_response_text_to_speech


async def reply_with_voice(message: Message, text: str, user_id: str, reply_markup: Optional[InlineKeyboardMarkup]):
    audio_content = await get_response_text_to_speech(text)

    total_price = 0.000015 * len(text)
    await write_transaction(user_id=user_id,
                            type=TransactionType.EXPENSE,
                            service=ServiceType.VOICE_MESSAGES,
                            amount=total_price,
                            currency=Currency.USD,
                            quantity=1)

    await message.answer_voice(voice=audio_content,
                               reply_markup=reply_markup)
