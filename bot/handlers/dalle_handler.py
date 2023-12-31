import time

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from telegram import constants

from bot.database.models.common import Model, Quota, Currency
from bot.database.models.transaction import TransactionType, ServiceType
from bot.database.models.user import UserSettings
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, update_user
from bot.helpers.send_message_to_admins import send_message_to_admins
from bot.integrations.openAI import get_response_image
from bot.locales.main import get_localization
from bot.utils.is_messages_limit_exceeded import is_messages_limit_exceeded
from bot.utils.is_time_limit_exceeded import is_time_limit_exceeded

dalle_router = Router()

PRICE_DALLE3 = 0.040


@dalle_router.message()
async def handle_dalle(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))
    user_data = await state.get_data()

    current_time = time.time()

    if user.current_model == Model.DALLE3:
        user_quota = Quota.DALLE3
    else:
        return
    need_exit = (await is_time_limit_exceeded(message, state, user, current_time) or
                 await is_messages_limit_exceeded(message, user, user_quota))
    if need_exit:
        return
    await state.update_data(last_request_time=current_time)

    text = user_data.get('recognized_text', None)
    if text is None:
        text = message.text

    processing_message = await message.reply(text=get_localization(user.language_code).processing_request())

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
    except Exception as e:
        await message.answer(f"{get_localization(user.language_code).ERROR}: {e}\n\nPlease contact @roman_danilov")
        await send_message_to_admins(bot=message.bot,
                                     message=f"#error\n\nALARM! Ошибка у пользователя: {user.id}\nИнформация:\n{e}")
    finally:
        await processing_message.delete()
