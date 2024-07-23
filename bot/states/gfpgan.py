from aiogram.fsm.state import StatesGroup, State


class GFPGAN(StatesGroup):
    waiting_for_photo_to_restore = State()
