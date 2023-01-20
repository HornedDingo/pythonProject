from aiogram import types
from database.db import db
from handlers.users.bot_authorization import search_id, search_status
from loader import dp
from filters import IsPrivate
from keyboards.reply import kb_menu, kb_menu2, kb_menu4

cursor2 = db.cursor()
cursor2.execute("USE pollbase")


@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Добро пожаловать в чат-бот для голосования. \n\n'
                         f'Выберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), text='Вернуться в главное меню')
async def command_start2(message: types.Message):
    await message.answer(f'Добро пожаловать в чат-бот для голосования. '
                         f'\n\nВыберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu2)


@dp.message_handler(IsPrivate(), text='Вернуться в меню')
async def command_start3(message: types.Message):
    await message.answer(f'Выберите один из предложенных ниже вариантов действий.', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), text='Проверить статус регистрации')
async def command_start4(message: types.Message):
    userid2 = search_id(message.from_user.id)
    userid2 = int(''.join(map(str, userid2)))
    status_user2 = search_status(userid2)
    status_user2 = int(''.join(map(str, status_user2)))
    if status_user2 == 0:
        await message.answer(f'Статус регистрации: ожидается одобрение.', reply_markup=kb_menu4)
    elif status_user2 == 1:
        await message.answer(f'Статус регистрации: одобрено.', reply_markup=kb_menu4)
    else:
        await message.answer(f'Вы заблокированы.', reply_markup=kb_menu4)
