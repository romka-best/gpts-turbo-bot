import openai
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from telegram import constants

from bot.database.models.common import Quota, Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings, User
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import update_user
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.integrations.openAI import get_response_image
from bot.locales.main import get_localization

dalle_router = Router()

PRICE_DALLE3 = 0.040


async def handle_dalle(message: Message, state: FSMContext, user: User, user_quota: Quota):
    user_data = await state.get_data()

    text = user_data.get('recognized_text', None)
    if text is None:
        text = message.text

    processing_message = await message.reply(text=get_localization(user.language_code).processing_request_image())

    await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.UPLOAD_PHOTO)

    try:
        response_url = await get_response_image(text)

        if user.monthly_limits[user_quota] > 0:
            user.monthly_limits[user_quota] -= 1
        else:
            user.additional_usage_quota[user_quota] -= 1

        await update_user(user.id, {
            "monthly_limits": user.monthly_limits,
            "additional_usage_quota": user.additional_usage_quota,
        })
        await write_transaction(user_id=user.id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.DALLE3,
                                amount=PRICE_DALLE3,
                                currency=Currency.USD,
                                quantity=1)

        footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
            if user.settings[UserSettings.SHOW_USAGE_QUOTA] else ''
        await message.reply_photo(
            caption=f"{get_localization(user.language_code).IMAGE_SUCCESS}{footer_text}",
            photo=response_url,
        )
    except openai.BadRequestError as e:
        if e.code == 'content_policy_violation':
            await message.reply(
                text=get_localization(user.language_code).REQUEST_FORBIDDEN_ERROR,
            )
    except Exception as e:
        await message.answer(
            text=f"{get_localization(user.language_code).ERROR}\n\nPlease contact @roman_danilov",
            parse_mode=None
        )
        await send_message_to_admins(bot=message.bot,
                                     message=f"#error\n\nALARM! Ошибка у пользователя при запросе в DALLE: {user.id}\nИнформация:\n{e}",
                                     parse_mode=None)
    finally:
        await processing_message.delete()
