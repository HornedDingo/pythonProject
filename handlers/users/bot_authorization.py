from aiogram import types
from aiogram.dispatcher import FSMContext
from passlib.handlers.phpass import phpass
from filters import IsPrivate
from handlers.users.start import search_id, search_status
from loader import dp
from states import AuthorizationPr
from database.db import db
from database.get import mysql4, mysql5
from keyboards.reply import kb_menu3
from handlers.users.bot_menu import show_list
from database.get import mysql9

cursor2 = db.cursor()

cursor2.execute("USE pollbase")


def q_done(id_q, user_id):
    q_id = id_q
    userid = user_id
    cursor2.execute(mysql9, (q_id, userid,))
    id_log = cursor2.fetchone()
    if id_log is not None:
        if int(''.join(map(str, id_log))) > 0:
            done_q = True
    else:
        done_q = False
    return done_q


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
            cursor2.execute(mysql4, (userid2,))
            exit_value = cursor2.fetchone()
            exit_value = int(''.join(map(str, exit_value)))
            if exit_value == 0:
                questions_list = show_list(message.from_user.id)
                print(questions_list)
                await message.answer(f'Добро пожаловать!\n' + questions_list[1])
            else:
                await message.answer(f'Здравствуйте, \n'
                                     f'для авторизации введите свой логин:')
                await AuthorizationPr.user_lg2.set()
    except Exception:
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
        cursor2.execute(mysql5, (user_lg2,))
        user_pswd4 = cursor2.fetchone()
        user_pswd4 = ''.join(user_pswd4)
        phpass.verify(user_pswd2, user_pswd4)
        await message.answer(f'Добро пожаловать!')
    except Exception:
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.')
    await state.finish()
