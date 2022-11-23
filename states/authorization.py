from aiogram.dispatcher.filters.state import StatesGroup, State


class authorization(StatesGroup):
    user_lg2= State()
    user_pswd2 = State()