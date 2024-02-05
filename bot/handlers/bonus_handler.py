from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, URLInputFile

from bot.database.main import firebase
from bot.database.models.common import Quota
from bot.database.models.package import PackageType, PackageMinimum, Package, PackageStatus
from bot.database.models.transaction import ServiceType, TransactionType
from bot.database.operations.package import write_package
from bot.database.operations.transaction import write_transaction
from bot.database.operations.user import get_user, get_users_by_referral, update_user
from bot.keyboards.bonus import build_bonus_keyboard
from bot.keyboards.common import build_cancel_keyboard
from bot.locales.main import get_localization
from bot.states.bonus import Bonus

bonus_router = Router()


@bonus_router.message(Command("bonus"))
async def bonus(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user(str(message.from_user.id))
    referred_users = await get_users_by_referral(user.id)

    photo_path = f'packages/{user.language_code}_{user.currency}.png'
    photo = await firebase.bucket.get_blob(photo_path)
    photo_link = firebase.get_public_url(photo.name)

    text = get_localization(user.language_code).bonus(user.id, len(referred_users), user.balance, user.currency)
    reply_markup = build_bonus_keyboard(user.language_code)

    await message.answer_photo(photo=URLInputFile(photo_link, filename=photo_path),
                               caption=text,
                               reply_markup=reply_markup)


@bonus_router.callback_query(lambda c: c.data.startswith('bonus:'))
async def handle_bonus_package_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user = await get_user(str(callback_query.from_user.id))

    package_type = callback_query.data.split(':')[1]

    message = get_localization(user.language_code).choose_min(package_type)

    reply_markup = build_cancel_keyboard(user.language_code)

    await callback_query.message.edit_caption(caption=message, reply_markup=reply_markup)

    await state.update_data(package_type=package_type)
    await state.set_state(Bonus.waiting_for_package_quantity)


@bonus_router.message(Bonus.waiting_for_package_quantity, ~F.text.startswith('/'))
async def quantity_of_bonus_package_sent(message: Message, state: FSMContext):
    user = await get_user(str(message.from_user.id))

    try:
        user_data = await state.get_data()
        package_type = user_data['package_type']
        quantity = int(message.text)
        if (
            (package_type == PackageType.GPT3 and quantity < PackageMinimum.GPT3) or
            (package_type == PackageType.GPT4 and quantity < PackageMinimum.GPT4) or
            (package_type == PackageType.CHAT and quantity < PackageMinimum.CHAT) or
            (package_type == PackageType.DALLE3 and quantity < PackageMinimum.DALLE3) or
            (package_type == PackageType.FACE_SWAP and quantity < PackageMinimum.FACE_SWAP) or
            (package_type == PackageType.MUSIC_GEN and quantity < PackageMinimum.MUSIC_GEN) or
            (package_type == PackageType.ACCESS_TO_CATALOG and quantity < PackageMinimum.ACCESS_TO_CATALOG) or
            (package_type == PackageType.VOICE_MESSAGES and quantity < PackageMinimum.VOICE_MESSAGES) or
            (package_type == PackageType.FAST_MESSAGES and quantity < PackageMinimum.FAST_MESSAGES)
        ):
            reply_markup = build_cancel_keyboard(user.language_code)
            await message.reply(text=get_localization(user.language_code).MIN_ERROR,
                                reply_markup=reply_markup)
        else:
            price = Package.get_price(user.currency, package_type, quantity)
            if price > user.balance:
                reply_markup = build_cancel_keyboard(user.language_code)
                await message.reply(text=get_localization(user.language_code).MAX_ERROR,
                                    reply_markup=reply_markup)
            else:
                user.balance -= price
                until_at = None
                if (
                    package_type == PackageType.VOICE_MESSAGES or
                    package_type == PackageType.FAST_MESSAGES or
                    package_type == PackageType.ACCESS_TO_CATALOG
                ):
                    current_date = datetime.now(timezone.utc)
                    until_at = current_date + timedelta(days=30 * int(quantity))
                package = await write_package(user.id,
                                              package_type,
                                              PackageStatus.SUCCESS,
                                              user.currency,
                                              0,
                                              int(quantity),
                                              until_at)

                service_type = package_type
                if package_type == PackageType.GPT3:
                    user.additional_usage_quota[Quota.GPT3] += quantity
                    service_type = ServiceType.GPT3
                elif package_type == PackageType.GPT4:
                    user.additional_usage_quota[Quota.GPT4] += quantity
                    service_type = ServiceType.GPT4
                elif package_type == PackageType.DALLE3:
                    user.additional_usage_quota[Quota.DALLE3] += quantity
                    service_type = ServiceType.DALLE3
                elif package_type == PackageType.FACE_SWAP:
                    user.additional_usage_quota[Quota.FACE_SWAP] += quantity
                    service_type = ServiceType.FACE_SWAP
                elif package_type == PackageType.MUSIC_GEN:
                    user.additional_usage_quota[Quota.MUSIC_GEN] += quantity
                    service_type = ServiceType.MUSIC_GEN
                elif package_type == PackageType.CHAT:
                    user.additional_usage_quota[Quota.ADDITIONAL_CHATS] += quantity
                    service_type = ServiceType.ADDITIONAL_CHATS
                elif package_type == PackageType.FAST_MESSAGES:
                    user.additional_usage_quota[Quota.FAST_MESSAGES] = True
                    service_type = ServiceType.FAST_MESSAGES
                elif package_type == PackageType.ACCESS_TO_CATALOG:
                    user.additional_usage_quota[Quota.ACCESS_TO_CATALOG] = True
                    service_type = ServiceType.ACCESS_TO_CATALOG
                elif package_type == PackageType.VOICE_MESSAGES:
                    user.additional_usage_quota[Quota.VOICE_MESSAGES] = True
                    service_type = ServiceType.VOICE_MESSAGES
                await write_transaction(user_id=user.id,
                                        type=TransactionType.INCOME,
                                        service=service_type,
                                        amount=0,
                                        currency=user.currency,
                                        quantity=quantity,
                                        details={
                                            'package_id': package.id,
                                            'provider_payment_charge_id': "",
                                        })
                await update_user(user.id, {
                    "balance": user.balance,
                    "additional_usage_quota": user.additional_usage_quota,
                })

                await message.reply(text=get_localization(user.language_code).BONUS_ACTIVATED_SUCCESSFUL)

                await state.clear()
    except ValueError:
        reply_markup = build_cancel_keyboard(user.language_code)
        await message.reply(text=get_localization(user.language_code).VALUE_ERROR,
                            reply_markup=reply_markup)
