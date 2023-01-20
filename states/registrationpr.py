from aiogram.dispatcher.filters.state import StatesGroup, State


class registrationpr(StatesGroup):
    user_lg = State()
    user_pswd = State()
    user_nick = State()
    user_email = State()
    user_url = State()
    user_regdate = State()
    user_activationkey = State()
    user_status = State()
    user_display_name = State()
    user_address = State()
    user_area_number = State()
    user_number = State()
    user_tg_id = State()
