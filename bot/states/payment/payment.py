from aiogram.fsm.state import StatesGroup, State


class Payment(StatesGroup):
    waiting_for_package_quantity = State()
