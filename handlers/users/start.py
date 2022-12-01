from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import mysql.connector
from loader import dp
from filters import IsPrivate


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


@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    kb_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авторизоваться'),
                KeyboardButton(text='Зарегистрироваться')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f'Добро пожаловать в чат-бот для голосования. \n\n'
                         f'Выберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), text='Вернуться в главное меню')
async def command_start2(message: types.Message):
    kb_menu2 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авторизоваться'),
                KeyboardButton(text='Проверить статус регистрации')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f'Добро пожаловать в чат-бот для голосования. '
                         f'\n\nВыберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu2)


@dp.message_handler(IsPrivate(), text='Вернуться в меню')
async def command_start3(message: types.Message):
    kb_menu3 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Авторизоваться'),
                KeyboardButton(text='Зарегистрироваться')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f'Выберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu3)


@dp.message_handler(IsPrivate(), text='Проверить статус регистрации')
async def command_start4(message: types.Message):
    kb_menu2 = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Вернуться в главное меню')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    userid2 = search_id(message.from_user.id)
    userid2 = int(''.join(map(str, userid2)))
    status_user2 = search_status(userid2)
    status_user2 = int(''.join(map(str, status_user2)))
    if status_user2 == 0:
        await message.answer(f'Статус регистрации: ожидается одобрение.', reply_markup=kb_menu2)
    elif status_user2 == 1:
        await message.answer(f'Статус регистрации: одобрено.', reply_markup=kb_menu2)
    else:
        await message.answer(f'Вы заблокированы.', reply_markup=kb_menu2)


def search_id(id_tg_user):
    userid = id_tg_user
    mysql2 = "SELECT user_id from wp_usermeta where meta_key = 'telegramid' and meta_value = %s"
    cursor3.execute(mysql2, (userid,))
    userid = cursor3.fetchone()
    return userid


def search_status(userid):
    userid2 = userid
    # userid2 = int(''.join(map(str, userid2)))
    mysql3 = "SELECT user_status from wp_users where ID = %s"
    cursor3.execute(mysql3, (userid2,))
    status_user = cursor3.fetchone()
    return status_user
