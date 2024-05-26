from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.models.promo_code import PromoCodeType
from bot.database.operations.promo_code.getters import get_promo_code_by_name
from bot.database.operations.promo_code.writers import write_promo_code
from bot.keyboards.admin.admin import build_admin_keyboard
from bot.keyboards.admin.promo_code import (
    build_create_promo_code_keyboard,
    build_create_promo_code_subscription_keyboard,
    build_create_promo_code_period_of_subscription_keyboard,
    build_create_promo_code_package_keyboard,
    build_create_promo_code_discount_keyboard,
)
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.promo_code import PromoCode

admin_promo_code_router = Router()


async def handle_create_promo_code(message: Message, user_id: str, state: FSMContext):
    user_language_code = await get_user_language(user_id, state.storage)

    reply_markup = build_create_promo_code_keyboard(user_language_code)
    await message.edit_text(
        text=get_localization(user_language_code).PROMO_CODE_INFO_ADMIN,
        reply_markup=reply_markup,
    )


@admin_promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code:'))
async def handle_create_promo_code_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    promo_code_type = callback_query.data.split(':')[1]
    if promo_code_type == 'back':
        reply_markup = build_admin_keyboard(user_language_code)
        await callback_query.message.edit_text(
            text=get_localization(user_language_code).ADMIN_INFO,
            reply_markup=reply_markup,
        )

        return
    elif promo_code_type == PromoCodeType.SUBSCRIPTION:
        photo_path = f'payments/subscriptions_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        caption = get_localization(user_language_code).PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN
        reply_markup = build_create_promo_code_subscription_keyboard(user_language_code)
        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=caption,
            reply_markup=reply_markup,
        )
    elif promo_code_type == PromoCodeType.PACKAGE:
        photo_path = f'payments/packages_{user_language_code}.png'
        photo = await firebase.bucket.get_blob(photo_path)
        photo_link = firebase.get_public_url(photo.name)

        caption = get_localization(user_language_code).PROMO_CODE_CHOOSE_PACKAGE_ADMIN
        reply_markup = build_create_promo_code_package_keyboard(user_language_code)
        await callback_query.message.answer_photo(
            photo=URLInputFile(photo_link, filename=photo_path),
            caption=caption,
            reply_markup=reply_markup,
        )
    elif promo_code_type == PromoCodeType.DISCOUNT:
        text = get_localization(user_language_code).PROMO_CODE_CHOOSE_DISCOUNT_ADMIN
        reply_markup = build_create_promo_code_discount_keyboard(user_language_code)
        await callback_query.message.answer(
            text=text,
            reply_markup=reply_markup,
        )

        await state.set_state(PromoCode.waiting_for_promo_code_discount)

    await callback_query.message.delete()


@admin_promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_subscription:'))
async def handle_create_promo_code_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    subscription_type = callback_query.data.split(':')[1]

    message = get_localization(user_language_code).choose_how_many_months_to_subscribe(subscription_type)
    reply_markup = build_create_promo_code_period_of_subscription_keyboard(user_language_code, subscription_type)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)


@admin_promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_period_of_subscription:'))
async def handle_create_promo_code_period_of_subscription_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    subscription_type, subscription_period = callback_query.data.split(':')[1], callback_query.data.split(':')[2]

    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.edit_caption(
        caption=get_localization(user_language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
        reply_markup=reply_markup
    )

    await state.set_state(PromoCode.waiting_for_promo_code_name)
    await state.update_data(
        promo_code_type=PromoCodeType.SUBSCRIPTION,
        promo_code_subscription_type=subscription_type,
        promo_code_subscription_period=subscription_period,
    )


@admin_promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_package:'))
async def handle_create_promo_code_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    package_type = callback_query.data.split(':')[1]

    message = get_localization(user_language_code).choose_min(package_type)
    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

    await state.update_data(promo_code_package_type=package_type)
    await state.set_state(PromoCode.waiting_for_promo_code_package_quantity)


@admin_promo_code_router.message(PromoCode.waiting_for_promo_code_package_quantity, ~F.text.startswith('/'))
async def handle_create_promo_promo_code_package_quantity_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    try:
        quantity = int(message.text)

        reply_markup = build_cancel_keyboard(user_language_code)
        await message.answer(
            text=get_localization(user_language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
            reply_markup=reply_markup
        )

        await state.set_state(PromoCode.waiting_for_promo_code_name)
        await state.update_data(
            promo_code_type=PromoCodeType.PACKAGE,
            promo_code_package_quantity=quantity,
        )
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )


@admin_promo_code_router.callback_query(lambda c: c.data.startswith('create_promo_code_discount:'))
async def handle_create_promo_code_discount_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    discount = int(callback_query.data.split(':')[1])
    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.answer(
        text=get_localization(user_language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
        reply_markup=reply_markup
    )

    await state.set_state(PromoCode.waiting_for_promo_code_name)
    await state.update_data(
        promo_code_type=PromoCodeType.DISCOUNT,
        promo_code_discount=discount,
    )


@admin_promo_code_router.message(PromoCode.waiting_for_promo_code_discount, ~F.text.startswith('/'))
async def handle_create_promo_code_discount_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    try:
        discount = int(message.text)

        if 1 <= discount <= 50:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.answer(
                text=get_localization(user_language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
                reply_markup=reply_markup
            )

            await state.set_state(PromoCode.waiting_for_promo_code_name)
            await state.update_data(
                promo_code_type=PromoCodeType.DISCOUNT,
                promo_code_discount=discount,
            )
        else:
            raise ValueError
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )


@admin_promo_code_router.message(PromoCode.waiting_for_promo_code_name, F.text, ~F.text.startswith('/'))
async def promo_code_name_sent(message: Message, state: FSMContext):
    user_language_code = await get_user_language(str(message.from_user.id), state.storage)

    promo_code_name = message.text.upper()
    typed_promo_code = await get_promo_code_by_name(promo_code_name)
    reply_markup = build_cancel_keyboard(user_language_code)
    if typed_promo_code:
        await message.reply(
            text=get_localization(user_language_code).PROMO_CODE_NAME_EXISTS_ERROR,
            reply_markup=reply_markup,
        )
    else:
        await message.reply(
            text=get_localization(user_language_code).PROMO_CODE_CHOOSE_DATE,
            reply_markup=reply_markup,
        )

        await state.set_state(state=None)
        await state.update_data(promo_code_name=promo_code_name)
        await state.set_state(PromoCode.waiting_for_promo_code_date)


@admin_promo_code_router.message(PromoCode.waiting_for_promo_code_date, ~F.text.startswith('/'))
async def promo_code_date_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        user_data = await state.get_data()
        promo_code_until_date = datetime.strptime(message.text, "%d.%m.%Y")
        promo_code_name = user_data['promo_code_name']
        promo_code_type = user_data['promo_code_type']
        details = {}
        if promo_code_type == PromoCodeType.SUBSCRIPTION:
            details['subscription_type'] = user_data['promo_code_subscription_type']
            details['subscription_period'] = user_data['promo_code_subscription_period']
        elif promo_code_type == PromoCodeType.PACKAGE:
            details['package_type'] = user_data['promo_code_package_type']
            details['package_quantity'] = user_data['promo_code_package_quantity']
        elif promo_code_type == PromoCodeType.DISCOUNT:
            details['discount'] = int(user_data['promo_code_discount'])

        await write_promo_code(
            created_by_user_id=user_id,
            name=promo_code_name,
            type=promo_code_type,
            until=promo_code_until_date,
            details=details,
        )
        await message.answer(text=get_localization(user_language_code).PROMO_CODE_SUCCESS_ADMIN)

        await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).PROMO_CODE_DATE_VALUE_ERROR,
            reply_markup=reply_markup,
        )
