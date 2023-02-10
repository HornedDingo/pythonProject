from aiogram import types
from database.db import db
from database.get import mysql,  mysql3
from loader import dp
from filters import IsPrivate
from keyboards.reply import kb_menu, kb_menu4

cursor2 = db.cursor()


def search_id(id_tg_user):
    userid = id_tg_user
    cursor2.execute(mysql, (userid,))
    userid = cursor2.fetchone()
    userid = int(''.join(map(str, userid)))
    return userid


def search_status(userid):
    userid2 = userid
    cursor2.execute(mysql3, (userid2,))
    status_user = cursor2.fetchone()
    status_user = int(''.join(map(str, status_user)))
    return status_user


@dp.message_handler(IsPrivate(), text='Вернуться в главное меню')
async def command_start2(message: types.Message):
    await message.answer(f'Добро пожаловать в чат-бот для голосования. '
                         f'\n\nВыберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), text='Вернуться в меню')
async def command_start3(message: types.Message):
    await message.answer(f'Выберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)

