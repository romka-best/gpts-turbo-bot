from datetime import datetime, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from bot.database.main import firebase
from bot.database.models.promo_code import PromoCodeType
from bot.database.models.subscription import SubscriptionType, SubscriptionStatus
from bot.database.operations.promo_code import get_promo_code_by_name, get_used_promo_code_by_user_id_and_promo_code_id, \
    write_used_promo_code, write_promo_code
from bot.database.operations.subscription import write_subscription
from bot.database.operations.user import get_user
from bot.helpers.create_subscription import create_subscription
from bot.keyboards.common import build_cancel_keyboard
from bot.utils.is_admin import is_admin
from bot.keyboards.promo_code import build_promo_code_keyboard, build_create_promo_code_keyboard, \
    build_create_promo_code_subscription_keyboard, build_create_promo_code_period_of_subscription_keyboard, \
    build_create_promo_code_name_keyboard, build_create_promo_code_date_keyboard
from bot.locales.main import get_localization
from bot.states.promo_code import PromoCode

promo_code_router = Router()


@promo_code_router.message(Command("promo_code"))
async def promo_code(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    reply_markup = build_promo_code_keyboard(user.language_code)
    await message.answer(text=get_localization(user.language_code).PROMO_CODE_INFO,
                         reply_markup=reply_markup)

    await state.set_state(PromoCode.waiting_for_promo_code)


@promo_code_router.message(PromoCode.waiting_for_promo_code)
async def promo_code_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    typed_promo_code = await get_promo_code_by_name(message.text.upper())
    if typed_promo_code:
        current_date = datetime.now(timezone.utc)
        if current_date <= typed_promo_code.until:
            used_promo_code = await get_used_promo_code_by_user_id_and_promo_code_id(user.id, typed_promo_code.id)
            if used_promo_code:
                reply_markup = build_cancel_keyboard(user.language_code)
                await message.reply(
                    text=get_localization(user.language_code).PROMO_CODE_ALREADY_USED_ERROR,
                    reply_markup=reply_markup
                )
            else:
                if typed_promo_code.type == PromoCodeType.SUBSCRIPTION:
                    if user.subscription_type == SubscriptionType.FREE:
                        subscription = await write_subscription(user.id,
                                                                typed_promo_code.details['subscription_type'],
                                                                typed_promo_code.details['subscription_period'],
                                                                SubscriptionStatus.WAITING,
                                                                user.currency,
                                                                0)

                        transaction = firebase.db.transaction()
                        await create_subscription(transaction,
                                                  subscription.id,
                                                  subscription.user_id,
                                                  "")

                        await write_used_promo_code(user.id, typed_promo_code.id)
                        await message.reply(
                            text=get_localization(user.language_code).PROMO_CODE_SUCCESS
                        )

                        await state.clear()
                    else:
                        reply_markup = build_cancel_keyboard(user.language_code)
                        await message.reply(
                            text=get_localization(user.language_code).PROMO_CODE_ALREADY_HAVE_SUBSCRIPTION,
                            reply_markup=reply_markup
                        )
                else:
                    await write_used_promo_code(user.id, typed_promo_code.id)
                    await message.reply(
                        text=get_localization(user.language_code).PROMO_CODE_SUCCESS
                    )
        else:
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.reply(
                text=get_localization(user.language_code).PROMO_CODE_EXPIRED_ERROR,
                reply_markup=reply_markup
            )
    else:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(
            text=get_localization(user.language_code).PROMO_CODE_NOT_FOUND_ERROR,
            reply_markup=reply_markup
        )


@promo_code_router.message(Command("create_promo_code"))
async def create_promo_code(message: Message):
    if is_admin(str(message.chat.id)):
        user = await get_user(str(message.from_user.id))

        reply_markup = build_create_promo_code_keyboard(user.language_code)
        await message.answer(text=get_localization(user.language_code).PROMO_CODE_INFO_ADMIN,
                             reply_markup=reply_markup)


@promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code:'))
async def handle_create_promo_code_selection(callback_query: CallbackQuery):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    promo_code_type = callback_query.data.split(':')[1]

    if promo_code_type == 'cancel':
        await callback_query.message.delete()
    else:
        if promo_code_type == PromoCodeType.SUBSCRIPTION:
            photo_path = f'subscriptions/{user.language_code}_{user.currency}.png'
            photo = await firebase.bucket.get_blob(photo_path)
            photo_data = await photo.download()

            caption = get_localization(user.language_code).PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN
            reply_markup = build_create_promo_code_subscription_keyboard(user.language_code)

            await callback_query.message.answer_photo(photo=BufferedInputFile(photo_data, filename=photo_path),
                                                      caption=caption,
                                                      reply_markup=reply_markup)

        await callback_query.message.delete()


@promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_subscription:'))
async def handle_create_promo_code_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    language_code = (await get_user(str(callback_query.from_user.id))).language_code

    subscription_type = callback_query.data.split(':')[1]

    if subscription_type == 'cancel':
        await callback_query.message.delete()

        await state.clear()
    else:
        message = get_localization(language_code).choose_how_many_months_to_subscribe(subscription_type)
        reply_markup = build_create_promo_code_period_of_subscription_keyboard(language_code, subscription_type)

        await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)


@promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_period_of_subscription:'))
async def handle_create_promo_code_period_of_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    subscription_type, subscription_period = callback_query.data.split(':')[1], callback_query.data.split(':')[2]

    reply_markup = build_create_promo_code_name_keyboard(user.language_code)

    await callback_query.message.edit_caption(
        caption=get_localization(user.language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
        reply_markup=reply_markup
    )

    await state.set_state(PromoCode.waiting_for_promo_code_name)
    await state.update_data(promo_code_type=PromoCodeType.SUBSCRIPTION,
                            promo_code_subscription_type=subscription_type,
                            promo_code_subscription_period=subscription_period)


@promo_code_router.message(PromoCode.waiting_for_promo_code_name)
async def promo_code_name_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    promo_code_name = message.text.upper()
    typed_promo_code = await get_promo_code_by_name(promo_code_name)
    if typed_promo_code:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(
            text=get_localization(user.language_code).PROMO_CODE_NAME_EXISTS_ERROR,
            reply_markup=reply_markup,
        )
    else:
        reply_markup = build_create_promo_code_date_keyboard(user.language_code)
        await message.reply(
            text=get_localization(user.language_code).PROMO_CODE_CHOOSE_DATE,
            reply_markup=reply_markup,
        )

        await state.set_state(state=None)
        await state.update_data(promo_code_name=promo_code_name)
        await state.set_state(PromoCode.waiting_for_promo_code_date)


@promo_code_router.message(PromoCode.waiting_for_promo_code_date)
async def promo_code_date_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        user_data = await state.get_data()
        promo_code_until_date = datetime.strptime(message.text, "%d.%m.%Y")
        promo_code_name = user_data['promo_code_name']
        promo_code_type = user_data['promo_code_type']
        details = {}
        if promo_code_type == PromoCodeType.SUBSCRIPTION:
            details['subscription_type'] = user_data['promo_code_subscription_type']
            details['subscription_period'] = user_data['promo_code_subscription_period']

        await write_promo_code(
            created_by_user_id=user.id,
            name=promo_code_name,
            type=promo_code_type,
            until=promo_code_until_date,
            details=details,
        )
        await message.answer(text=get_localization(user.language_code).PROMO_CODE_SUCCESS_ADMIN)

        await state.clear()
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(
            text=get_localization(user.language_code).PROMO_CODE_DATE_VALUE_ERROR,
            reply_markup=reply_markup,
        )
