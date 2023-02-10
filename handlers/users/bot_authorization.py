from asyncio import sleep
from datetime import datetime
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher import FSMContext
from passlib.handlers.phpass import phpass
from filters import IsPrivate
from handlers.users.bot_menu import search_for_users_id, q_is_active, q_name
from loader import dp, bot
from states import AuthorizationPr
from database.db import db
from database.get import mysql4, mysql5, mysql9, mysql, mysql3, mysql12, mysql13, mysql14, mysql15, mysql20
from database.create import mysql16, mysql2
from keyboards.reply import kb_menu3, kb_menu4

cursor2 = db.cursor()
cursor2.execute("USE pollbase")


class Question:
    def __init__(self):
        self.q_id = ""
        self.answers = []
        self.id_user = ""
        self.q_date = datetime.now()
        self.id_chat = ""
        self.user_role = ""


def search_id(id_tg_user):
    userid = id_tg_user
    cursor2.execute(mysql, (userid,))
    userid = cursor2.fetchone()
    return userid


def search_id_by_login(ex_login):
    user_log = ex_login
    cursor2.execute(mysql20, (user_log,))
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


def get_questions(data):
    questions = InlineKeyboardMarkup()
    b0 = InlineKeyboardButton(text='Обновить', callback_data='kkk')
    questions.add(*[InlineKeyboardButton(button, callback_data=button) for button in data]).add(b0)
    return questions


async def show_users_questions():
    b = []
    a = []
    cursor2.execute(mysql12)
    qs = cursor2.fetchall()
    n = len(qs)
    for i in range(0, n):
        b.append(int(''.join(map(str, qs[i]))))
        q_user_id = search_for_users_id(b[i])
        q_active = q_is_active(b[i])
        q_answered = q_done(b[i], question.id_user)
        if ((q_user_id == 4) or (q_user_id == question.user_role)) & (q_active is True) & (q_answered is False):
            if len(a) < 5:
                a.append(''.join(q_name(b[i])))
    if not a:
        await bot.send_message(question.id_chat, f'На данный момент доступных опросов нет.\n\n',
                               reply_markup=get_questions(a))
    if a:
        await bot.send_message(question.id_chat, f'Ниже представлены доступные Вам на данный момент опросы.\n\n'
                                                       f'Нажмите на один из них для перехода к голосованию:',
                               reply_markup=get_questions(a))


question = Question()


@dp.message_handler(IsPrivate(), text='/start')
async def bot_auth2(message: types.Message):
    try:
        userid2 = search_id(message.from_user.id)
        if userid2:
            userid2 = int(''.join(map(str, userid2)))
            question.id_user = userid2
            question.id_chat = message.chat.id
            status_user = search_status(userid2)
            status_user = int(''.join(map(str, status_user)))
            if status_user == 0:
                await message.answer(f'Попробуйте позже. Ожидается одобрение регистрации.', reply_markup=kb_menu4)
            elif status_user == 1:
                cursor2.execute(mysql4, (userid2,))
                exit_value = cursor2.fetchone()
                exit_value = int(''.join(map(str, exit_value)))
                cursor2.execute(mysql13, (userid2,))
                user_role = cursor2.fetchone()
                user_role = int(''.join(map(str, user_role)))
                question.user_role = user_role
                if exit_value == 0:
                    await bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=ReplyKeyboardRemove())
                    await show_users_questions()
                else:
                    await message.answer(f'Здравствуйте, \n'
                                         f'для авторизации введите свой логин:',  reply_markup=ReplyKeyboardRemove())
                    await AuthorizationPr.user_lg2.set()
        else:
            await message.answer(f'Здравствуйте, \n'
                                 f'для авторизации введите свой логин:', reply_markup=ReplyKeyboardRemove())
            await AuthorizationPr.user_lg2.set()
    except Exception:
        await message.answer(f'Вы не зарегистрированы или ожидается одобрение регистрации..', reply_markup=kb_menu3)


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
        if search_id(message.from_user.id):
            userid2 = search_id(message.from_user.id)
        else:
            userid2 = search_id_by_login(data.get('user_lg2'))
        userid2 = int(''.join(map(str, userid2)))
        question.id_user = userid2
        question.id_chat = message.chat.id
        user_lg2 = data.get('user_lg2')
        user_pswd2 = data.get('user_pswd2')
        cursor2.execute(mysql5, (user_lg2,))
        user_pswd4 = cursor2.fetchone()
        user_pswd4 = ''.join(user_pswd4)
        phpass.verify(user_pswd2, user_pswd4)
        cursor2.execute(mysql13, (userid2,))
        user_role = cursor2.fetchone()
        user_role = int(''.join(map(str, user_role)))
        question.user_role = user_role
        cursor2.execute(mysql2, (userid2, "telegramid", message.from_user.id,))
        db.commit()
        await bot.send_message(message.from_user.id, 'Добро пожаловать!')
        await show_users_questions()
    except Exception:
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.')
    await state.finish()


@dp.callback_query_handler(lambda call: True)
async def answer_poll(callback_query: types.CallbackQuery):
    if callback_query.data != 'kkk':
        global sendpoll
        cqdata = callback_query.data
        answers = []
        cursor2.execute(mysql14, (cqdata,))
        qid = cursor2.fetchone()
        qid = (int(''.join(map(str, qid))))
        question.q_id = qid
        cursor2.execute(mysql15, (qid,))
        raw_answers = cursor2.fetchall()
        n = len(raw_answers)
        for i in range(0, n):
            answers.append(''.join(raw_answers[i]))
        sendpoll = await bot.send_poll(question.id_chat, cqdata, answers, 'regular')
        await bot.answer_callback_query(callback_query.id)
    else:
        await callback_query.message.delete()
        await bot.answer_callback_query(callback_query.id)
        await show_users_questions()


@dp.poll_answer_handler()
async def poll_handler(poll_answer: types.PollAnswer):
    question.answers = (int(''.join(map(str, poll_answer.option_ids))))
    question.q_date = datetime.now()
    cursor2.execute(mysql16, (question.q_id, question.answers, question.id_user))
    db.commit()
    done = await bot.send_message(question.id_chat, text="Ваш голос успешно принят!")
    await sleep(5)
    await sendpoll.delete()
    await done.delete()
