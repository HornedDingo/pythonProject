from aiogram import types
from aiogram.dispatcher import FSMContext
from passlib.handlers.phpass import phpass
from filters import IsPrivate
from handlers.users.bot_menu import search_for_users_id, q_is_active, q_name
from loader import dp
from states import AuthorizationPr
from database.db import db
from database.get import mysql4, mysql5, mysql9, mysql2, mysql3, mysql12
from keyboards.reply import kb_menu3

cursor2 = db.cursor()
cursor2.execute("USE pollbase")


def search_id(id_tg_user):
    userid = id_tg_user
    cursor2.execute(mysql2, (userid,))
    userid = cursor2.fetchone()
    return userid


def search_status(userid):
    userid2 = userid
    cursor2.execute(mysql3, (userid2,))
    status_user = cursor2.fetchone()
    return status_user


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
                b = []
                a = []
                cursor2.execute(mysql12)
                qs = cursor2.fetchall()
                n = len(qs)
                for i in range(0, n):
                    b.append(int(''.join(map(str, qs[i]))))
                    q_user_id = search_for_users_id(b[i])
                    q_active = q_is_active(b[i])
                    q_answered = q_done(b[i], userid2)
                    print(q_answered)
                    if ((q_user_id == 4) or (q_user_id == 1)) & (q_active is True) & (q_answered is False):
                        a.append(''.join(q_name(b[i])))
                print(a)
                await message.answer(f'Добро пожаловать!\n' + a[1])
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
        userid2 = search_id(message.from_user.id)
        userid2 = int(''.join(map(str, userid2)))
        user_lg2 = data.get('user_lg2')
        user_pswd2 = data.get('user_pswd2')
        cursor2.execute(mysql5, (user_lg2,))
        user_pswd4 = cursor2.fetchone()
        user_pswd4 = ''.join(user_pswd4)
        phpass.verify(user_pswd2, user_pswd4)
        b = []
        a = []
        cursor2.execute(mysql12)
        qs = cursor2.fetchall()
        n = len(qs)
        for i in range(0, n):
            b.append(int(''.join(map(str, qs[i]))))
            q_user_id = search_for_users_id(b[i])
            q_active = q_is_active(b[i])
            q_answered = q_done(b[i], userid2)
            print(q_answered)
            if ((q_user_id == 4) or (q_user_id == userid2)) & (q_active is True) & (q_answered is False):
                a.append(''.join(q_name(b[i])))
        print(a)
        await message.answer(f'Добро пожаловать!\n' + a[1])
    except Exception:
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.')
    await state.finish()
