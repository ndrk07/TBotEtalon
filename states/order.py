from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    product = State()
    count = State()
    name = State()
    phone = State()
