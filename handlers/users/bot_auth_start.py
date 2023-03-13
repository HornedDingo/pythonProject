import datetime
from asyncio import sleep
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from passlib.handlers.phpass import phpass
from loader import dp, bot
from filters import IsPrivate
from database import db, mysql, mysql2, mysql3, mysql4, mysql5, mysql12, mysql13, mysql15, mysql16, mysql21, mysql22, \
    mysql25, mysql26, mysql27, mysql28
from keyboards import kb_menu, kb_main_btn, kb_menu3, kb_menu4, kb_poll_btn, kb_new_poll
from states import AuthorizationPr
from .bot_user import search_smth, search_id_by_login
from .bot_questions import q_done, q_name, q_is_active, search_for_users_id

cursor2 = db.cursor()


class User:
    def __init__(self):
        self.id_chat = ""
        self.user_db_id = ""
        self.user_tg_id = ""
        self.user_status = ""
        self.user_auth2 = ""
        self.user_role = ""


class Question:
    def __init__(self):
        self.q_id = ""
        self.q_date = ""
        self.q_answers = ""
        self.q_in_post = ""
        self.next_in_p = ""
        self.previous_in_p = ""
        self.available_answers = []
        self.q_multiple = False


user = User()
question = Question()


def all_questions():
    cursor2 = db.cursor()
    cursor2.execute("USE pollbase")
    a = []
    a.clear()
    cursor2.execute(mysql12)
    qs = cursor2.fetchall()
    n = len(qs)
    for i in range(0, n):
        q = int(''.join(map(str, qs[i])))
        q_user_id = search_for_users_id(q)
        q_active = q_is_active(q)
        q_answered = q_done(q, user.user_db_id)
        if ((q_user_id == 4) or (q_user_id == user.user_role)) & (q_active is True) & (q_answered is False):
            if len(a) < 1:
                a.append(str(q))
                break
    b = []
    if a:
        b = a[0]
    print(a, ' ', b)
    return b


async def one_poll(b):
    a = b
    if a:
        c = []
        answers = []
        print(a, ' ', a[0])
        cursor2.execute(mysql21, (a[0],))
        in_p = cursor2.fetchone()
        in_p = int(''.join(map(str, in_p)))
        print(in_p, ' in_p')
        question.next_in_p = in_p
        if question.next_in_p == question.previous_in_p:
            cursor2.execute(mysql22, (in_p,))
            qs = cursor2.fetchall()
            n = len(qs)
            for i in range(0, n):
                if not q_done(int(''.join(map(str, qs[i]))), user.user_db_id):
                    c.append(int(''.join(map(str, qs[i]))))
            print(c, ' c')
            # for j in range(0, n):
            cursor2.execute(mysql15, (c[0],))
            raw_answers = cursor2.fetchall()
            n = len(raw_answers)
            print(c, c[0])
            print(answers)
            global sent_poll
            for i in range(0, n):
                answers.append(''.join(raw_answers[i]))
            print(q_name(c[0]))
            question.q_id = c[0]
            question.q_answered = False
            n = len(answers)
            for i in range(0, n):
                question.available_answers.append(answers[i])
            if search_smth(mysql28, c[0]) == 1:
                question.q_multiple == True
            else:
                question.q_multiple == False
            sent_poll = await bot.send_poll(user.id_chat, ''.join(map(str, q_name(c[0]))), answers, 'regular',
                                            allows_multiple_answers=question.q_multiple, reply_markup=kb_poll_btn)
            answers.clear()
        else:
            global new_poll
            new_poll = await bot.send_message(user.id_chat,
                                              "Найден новый опрос. Продолжить?", reply_markup=kb_new_poll)
    else:
        no_question = await bot.send_message(user.id_chat,
                                             "К сожалению, активные и открытые для Вас голосования сейчас не проводятся.")
        await sleep(5)
        await no_question.delete()
        await main_menu()


async def main_menu():
    global welc
    welc = await bot.send_message(user.id_chat,
                                  'Вы можете посмотреть результаты прошедших опросов или пройти новый.',
                                  reply_markup=kb_main_btn)


@dp.message_handler(IsPrivate(), text="/start")
async def bot_auth2(message: types.Message):
    try:
        user_id = search_smth(mysql, message.from_user.id)
        if user_id:
            user.user_db_id = user_id
            user.id_chat = message.chat.id
            user.user_status = search_smth(mysql3, user_id)
            if user.user_status == 0:
                await message.answer(f'Попробуйте позже. Ожидается одобрение регистрации.', reply_markup=kb_menu4)
            elif user.user_status == 1:
                user.user_auth2 = search_smth(mysql4, user.user_db_id)
                user.user_role = search_smth(mysql13, user.user_db_id)
                if user.user_auth2 == 0:
                    await bot.send_message(message.from_user.id, 'Добро пожаловать!',
                                           reply_markup=ReplyKeyboardRemove())
                    await main_menu()
                else:
                    await message.answer(f'Здравствуйте, \n'
                                         f'для авторизации введите свой логин:', reply_markup=ReplyKeyboardRemove())
                    await AuthorizationPr.user_lg2.set()
        else:
            await message.answer(f'Здравствуйте, \n'
                                 f'для авторизации введите свой логин:', reply_markup=ReplyKeyboardRemove())
            await AuthorizationPr.user_lg2.set()
    except Exception:
        await message.answer(f'Вы не зарегистрированы или ожидается одобрение регистрации.', reply_markup=kb_menu3)


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
        if search_smth(mysql, message.from_user.id):
            user.user_db_id = search_smth(mysql, message.from_user.id)
        else:
            user.user_db_id = search_id_by_login(data.get('user_lg2'))
            cursor2.execute(mysql2, (user.user_db_id, "telegramid", message.from_user.id,))
            db.commit()
        user.id_chat = message.chat.id
        user_lg2 = data.get('user_lg2')
        user_pswd2 = data.get('user_pswd2')
        cursor2.execute(mysql5, (user_lg2,))
        user_pswd4 = cursor2.fetchone()
        user_pswd4 = ''.join(user_pswd4)
        if phpass.verify(user_pswd2, user_pswd4):
            user.user_role = search_smth(mysql13, user.user_db_id)
            await bot.send_message(message.from_user.id, 'Добро пожаловать!')
            await main_menu()
        else:
            await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.', reply_markup=kb_menu)
    except Exception:
        await message.answer(f'Неверно введены данные. \nПопробуйте ещё раз.', reply_markup=kb_menu)
    await state.finish()


@dp.poll_answer_handler()
async def poll_handler(poll_answer: types.PollAnswer):
    question.q_answers = search_smth(mysql25, question.available_answers[(int(''.join(map(str, poll_answer.option_ids))))])
    votes = search_smth(mysql27, question.q_answers)
    cursor2.execute(mysql26, ((votes + 1), question.q_answers,))
    db.commit()


@dp.callback_query_handler(lambda call: True)
async def main_buttons(callback_query: types.CallbackQuery):
    if callback_query.data == 'show_old_q':
        await welc.delete()
        await bot.send_message(user.id_chat, "text1")
    elif callback_query.data == 'start':
        await bot.send_message(user.id_chat, text=f'Здравствуйте, \n'
                                                  f'для авторизации введите свой логин:')
        await AuthorizationPr.user_lg2.set()
    elif callback_query.data == "show_new_q":
        await welc.delete()
        q_array = all_questions()
        await one_poll(q_array)
    elif callback_query.data == "close_poll":
        await new_poll.delete()
        await main_menu()
    elif callback_query.data == "continue_poll":
        await new_poll.delete()
        question.previous_in_p = question.next_in_p
        await one_poll(all_questions())
    elif callback_query.data == "stop_poll":
        await sent_poll.delete()
        await main_menu()
    elif callback_query.data == "next_question":
        print(question.q_answers, ' ', q_is_active(question.q_id))
        if question.q_answers >= 0:
            await sent_poll.delete()
            question.q_date = datetime.datetime
            cursor2.execute(mysql16, (question.q_id, question.q_answers, user.user_db_id))
            db.commit()
            question.available_answers.clear()
            done = await bot.send_message(user.id_chat, text="Ваш голос успешно принят!")
            await sleep(2)
            await done.delete()
            await one_poll(all_questions())
        elif (question.q_answers is None) and q_is_active(question.q_id):
            print(question.q_answers)
            no_answers = await bot.send_message(user.id_chat,
                                                f"Пожалуйста, выберите вариант ответа.")
            await sleep(2)
            await no_answers.delete()
        else:
            q_closed = await bot.send_message(user.id_chat,
                                              f"Опрос уже завершён.")
            await sleep(2)
            await sent_poll.delete()
            await q_closed.delete()
            await main_menu()
    await bot.answer_callback_query(callback_query.id)
