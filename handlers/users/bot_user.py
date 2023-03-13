from database.db import db
from database.get import mysql20

cursor2 = db.cursor()
cursor2.execute("USE pollbase")


# Search user's property by some parameters
def search_smth(query, user_tg_id):
    query = query
    user_id = user_tg_id
    cursor2.execute(query, (user_id,))
    user_id = cursor2.fetchone()
    user_id = int(''.join(map(str, user_id)))
    return user_id


# Search user's db id by login
def search_id_by_login(ex_login):
    user_log = ex_login
    cursor2.execute(mysql20, (user_log,))
    userid = cursor2.fetchone()
    userid = int(''.join(map(str, userid)))
    return userid

#
# def get_questions(data):
#     questions = InlineKeyboardMarkup()
#     b0 = InlineKeyboardButton(text='Обновить', callback_data='kkk')
#     questions.add(*[InlineKeyboardButton(button, callback_data=button) for button in data]).add(b0)
#     return questions
#
#
# async def show_users_questions():
#     b = []
#     a = []
#     cursor2.execute(mysql12)
#     qs = cursor2.fetchall()
#     n = len(qs)
#     for i in range(0, n):
#         b.append(int(''.join(map(str, qs[i]))))
#         q_user_id = search_for_users_id(b[i])
#         q_active = q_is_active(b[i])
#         q_answered = q_done(b[i], question.id_user)
#         if ((q_user_id == 4) or (q_user_id == question.user_role)) & (q_active is True) & (q_answered is False):
#             if len(a) < 5:
#                 a.append(''.join(q_name(b[i])))
#     if not a:
#         await bot.send_message(question.id_chat, f'На данный момент доступных опросов нет.\n\n',
#                                reply_markup=get_questions(a))
#     if a:
#         await bot.send_message(question.id_chat, f'Ниже представлены доступные Вам на данный момент опросы.\n\n'
#                                                  f'Нажмите на один из них для перехода к голосованию:',
#                                reply_markup=get_questions(a))
#
#
# question = Question()
#
# @dp.callback_query_handler(lambda call: True)
# async def answer_poll(callback_query: types.CallbackQuery):
#     if callback_query.data != 'kkk':
#         global sendpoll
#         cqdata = callback_query.data
#         answers = []
#         cursor2.execute(mysql14, (cqdata,))
#         qid = cursor2.fetchone()
#         qid = (int(''.join(map(str, qid))))
#         question.q_id = qid
#         cursor2.execute(mysql15, (qid,))
#         raw_answers = cursor2.fetchall()
#         n = len(raw_answers)
#         for i in range(0, n):
#             answers.append(''.join(raw_answers[i]))
#         sendpoll = await bot.send_poll(question.id_chat, cqdata, answers, 'regular')
#         await bot.answer_callback_query(callback_query.id)
#     else:
#         await callback_query.message.delete()
#         await bot.answer_callback_query(callback_query.id)
#         await show_users_questions()
#
