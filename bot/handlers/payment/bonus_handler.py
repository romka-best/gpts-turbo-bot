from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.models.package import PackageType, Package, PackageStatus
from bot.database.models.transaction import TransactionType
from bot.database.operations.package.writers import write_package
from bot.database.operations.transaction.writers import write_transaction
from bot.database.operations.user.getters import get_user, get_users_by_referral
from bot.database.operations.user.updaters import update_user
from bot.keyboards.payment.bonus import build_bonus_keyboard
from bot.keyboards.common.common import build_cancel_keyboard
from bot.locales.main import get_localization, get_user_language
from bot.states.bonus import Bonus

bonus_router = Router()


@bonus_router.message(Command("bonus"))
async def bonus(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)
    referred_users = await get_users_by_referral(user_id)

    photo_path = f'payments/packages_{user_language_code}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user_language_code).bonus(user_id, len(referred_users), user.balance)
    reply_markup = build_bonus_keyboard(user_language_code)
    await message.answer_photo(
        photo=URLInputFile(photo_link, filename=photo_path),
        caption=text,
        reply_markup=reply_markup,
    )


@bonus_router.callback_query(lambda c: c.data.startswith('bonus:'))
async def handle_bonus_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_language_code = await get_user_language(str(callback_query.from_user.id), state.storage)

    package_type = callback_query.data.split(':')[1]

    message = get_localization(user_language_code).choose_min(package_type)

    reply_markup = build_cancel_keyboard(user_language_code)
    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

    await state.update_data(package_type=package_type)
    await state.set_state(Bonus.waiting_for_package_quantity)


@bonus_router.message(Bonus.waiting_for_package_quantity, ~F.text.startswith('/'))
async def quantity_of_bonus_package_sent(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user_language_code = await get_user_language(user_id, state.storage)

    try:
        user_data = await state.get_data()
        package_type = user_data['package_type']
        package_quantity = int(message.text)
        price = Package.get_price(user.currency, package_type, package_quantity)
        if price > user.balance:
            reply_markup = build_cancel_keyboard(user_language_code)
            await message.reply(
                text=get_localization(user_language_code).MAX_ERROR,
                reply_markup=reply_markup,
            )
        else:
            user.balance -= price
            until_at = None
            if (
                package_type == PackageType.VOICE_MESSAGES or
                package_type == PackageType.FAST_MESSAGES or
                package_type == PackageType.ACCESS_TO_CATALOG
            ):
                current_date = datetime.now(timezone.utc)
                until_at = current_date + timedelta(days=30 * package_quantity)
            package = await write_package(
                user_id,
                package_type,
                PackageStatus.SUCCESS,
                user.currency,
                0,
                package_quantity,
                until_at,
            )

            (
                service_type,
                user.additional_usage_quota,
            ) = Package.get_service_type_and_update_quota(
                package_type,
                user.additional_usage_quota,
                package_quantity,
            )
            await write_transaction(
                user_id=user_id,
                type=TransactionType.INCOME,
                service=service_type,
                amount=0,
                currency=user.currency,
                quantity=package_quantity,
                details={
                    'package_id': package.id,
                    'provider_payment_charge_id': "",
                    'is_bonus': True,
                },
            )
            await update_user(user_id, {
                "balance": user.balance,
                "additional_usage_quota": user.additional_usage_quota,
            })

            await message.reply(text=get_localization(user_language_code).BONUS_ACTIVATED_SUCCESSFUL)

            await state.clear()
    except (TypeError, ValueError):
        reply_markup = build_cancel_keyboard(user_language_code)
        await message.reply(
            text=get_localization(user_language_code).VALUE_ERROR,
            reply_markup=reply_markup,
        )
