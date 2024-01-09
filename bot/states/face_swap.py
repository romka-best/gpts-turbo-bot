from aiogram.fsm.state import StatesGroup, State


class FaceSwap(StatesGroup):
    waiting_for_face_swap_quantity = State()

    # Admin
    waiting_for_face_swap_system_package_name = State()
    waiting_for_face_swap_package_name = State()
    waiting_for_face_swap_picture = State()
