from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from passlib.handlers.phpass import phpass

from filters import IsPrivate
from handlers.users.start import search_id, search_status
from loader import dp
from states import AuthorizationPr
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rgaatrfla",
    port="3306",
    database="pollbase"
)

cursor2 = db.cursor()
cursor3 = db.cursor()
cursor2.execute("USE pollbase")


@dp.message_handler(IsPrivate(), text='Авторизоваться')
async def bot_auth2(message: types.Message):
    try:
        userid2 = search_id(message.from_user.id)
        userid2 = int(''.join(map(str, userid2)))
        status_user = search_status(userid2)
        status_user = int(''.join(map(str, status_user)))
        if status_user == 0:
            await message.answer(f'Попробуйте позже. Ожидается одобрение регистрации.')
        elif status_user == 1:
            mysql2 = "SELECT meta_value from wp_usermeta where meta_key = 'auth_2' and user_id = %s"
            cursor3.execute(mysql2, (userid2,))
            exit_value = cursor3.fetchone()
            exit_value = int(''.join(map(str, exit_value)))
            if exit_value == 0:
                await message.answer(f'Добро пожаловать!')
            else:
                await message.answer(f'Здравствуйте, \n'
                                     f'для авторизации введите свой логин:')
                await AuthorizationPr.user_lg2.set()
    except Exception:
        kb_menu3 = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Вернуться в меню')
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer(f'Вы не зарегистрированы.', reply_markup=kb_menu3)


@dp.message_handler(IsPrivate(), state=AuthorizationPr.user_lg2)
async def get_lg(message: types.Message, state: FSMContext):
    await state.update_data(user_lg2=message.text)
    await message.answer(f'Введите ваш пароль: ')
    await AuthorizationPr.user_pswd2.set()


@dp.message_handler(IsPrivate(), state=AuthorizationPr.user_pswd2)
async def get_pswd2(message: types.Message, state: FSMContext):
    try:
        await state.update_data(user_pswd2=message.text)
        data = await state.get_data()
        user_lg2 = data.get('user_lg2')
        user_pswd2 = data.get('user_pswd2')
        mysql1 = "SELECT user_pass from wp_users where user_login = %s;"
        cursor2.execute(mysql1, (user_lg2,))
        user_pswd4 = cursor2.fetchone()
        user_pswd4 = ''.join(user_pswd4)
        phpass.verify(user_pswd2, user_pswd4)
        await message.answer(f'Добро пожаловать!')
        # await state.finish()
    except Exception:
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.')
    await state.finish()
