from aiogram.fsm.state import StatesGroup, State


class Ads(StatesGroup):
    waiting_for_campaign_name = State()
