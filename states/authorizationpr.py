from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthorizationPr(StatesGroup):
    user_lg2 = State()
    user_pswd2 = State()
