from aiogram.fsm.state import StatesGroup, State


class FaceSwap(StatesGroup):
    waiting_for_face_swap_quantity = State()
