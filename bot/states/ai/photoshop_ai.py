from aiogram.fsm.state import StatesGroup, State


class PhotoshopAI(StatesGroup):
    waiting_for_photo = State()
