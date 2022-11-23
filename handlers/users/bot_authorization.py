from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from filters import IsPrivate
from loader import dp
from states import authorization
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rgaatrfla",
    port="3306",
    database="pollbase"
)


cursor2 = db.cursor()
cursor2.execute("USE pollbase")

@dp.message_handler(IsPrivate(), text='Авторизоваться')
async def bot_auth1(message: types.Message):
    await message.answer(f'Здравствуйте, \n'
                         f'для авторизации введите свой логин:')
    await authorization.user_lg2.set()

@dp.message_handler(IsPrivate(), Command('auth'))
async def bot_auth1(message: types.Message):
    await message.answer(f'Здравствуйте, \n'
                         f'для авторизации введите свой логин:')
    await authorization.user_lg2.set()

@dp.message_handler(IsPrivate(), state=authorization.user_lg2)
async def get_lg(message: types.Message, state: FSMContext):
    await state.update_data(user_lg2=message.text)
    await message.answer(f'Введите ваш пароль: ')
    await authorization.user_pswd2.set()


@dp.message_handler(IsPrivate(), state=authorization.user_pswd2)
async def get_pswd2(message: types.Message, state: FSMContext):
    await state.update_data(user_pswd2=message.text)
    data = await state.get_data()
    user_lg2 = data.get('user_lg2')
    user_pswd2 = data.get('user_pswd2')
    mysql="SELECT user_nicename from wp_users where user_login = %s AND user_pass = %s;"
    cursor2.execute(mysql, (user_lg2, user_pswd2))
    if not cursor2.fetchone():
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.')
        await state.finish()
    else:
        await message.answer(f'Добро пожаловать!')
        await state.finish()