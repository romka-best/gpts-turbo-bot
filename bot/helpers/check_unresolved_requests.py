import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Bot

from bot.database.models.request import RequestStatus
from bot.database.operations.request.getters import get_started_requests
from bot.database.operations.request.updaters import update_request
from bot.helpers.senders.send_message_to_admins import send_message_to_admins


async def check_unresolved_requests(bot: Bot):
    today_utc_day = datetime.now(timezone.utc)
    yesterday_utc_day = today_utc_day - timedelta(days=1)
    not_finished_requests = await get_started_requests(yesterday_utc_day, today_utc_day - timedelta(minutes=30))

    tasks = []
    for not_finished_request in not_finished_requests:
        had_error = True
        not_finished_request.details['has_error'] = had_error
        tasks.append(
            update_request(
                not_finished_request.id,
                {
                    "status": RequestStatus.FINISHED,
                    "details": not_finished_request.details,
                }
            )
        )

    await asyncio.gather(*tasks)

    if len(tasks):
        await send_message_to_admins(
            bot,
            f"⚠️ <b>Внимание!</b>\n\nЯ нашёл генерации, которым больше 30 минут ❗️\n\nКоличество: {len(tasks)}",
        )
