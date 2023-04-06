from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import db
from database import mysql7, mysql8, mysql9, mysql10, mysql11, mysql23

cursor2 = db.cursor(buffered=True)


# Search for which users the poll is available
def search_for_users_id(id_q):
    q_id = id_q
    cursor2.execute(mysql7, (q_id,))
    for_users_id = cursor2.fetchone()
    answer_1 = int(''.join(map(str, for_users_id)))
    if answer_1 > 0:
        answer_2 = answer_1
    return answer_2


# Check relevance of poll
def q_is_active(id_q):
    q_id = id_q
    cursor2.execute(mysql8, (q_id,))
    is_active = int(''.join(map(str, cursor2.fetchone())))
    if is_active > 0:
        actual_q = True
    else:
        actual_q = False
    return actual_q


# Count total number of questions
def q_count():
    cursor2.execute(mysql10)
    q_number = cursor2.fetchone()
    return q_number


# Get question's name
def q_name(id_q):
    q_id = id_q
    cursor2.execute(mysql11, (q_id,))
    name_q = cursor2.fetchone()
    return name_q


# Check if completed
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


def search_qid(user_id):
    query = mysql23
    userid = user_id
    cursor2.execute(query, (userid,))
    qid = cursor2.fetchall()
    n = len(qid)
    c = []
    for i in range(0, n):
        c.append(int(''.join(map(str, qid[i]))))
    return c


def search_q_name(data):
    b = data
    questions = []
    n = len(b)
    for i in range(0, n):
        questions.append(''.join(map(str, q_name(b[i]))))
    return questions


def get_questions(data):
    questions = InlineKeyboardMarkup()
    b0 = InlineKeyboardButton(text='Назад', callback_data='back')
    questions.add(*[InlineKeyboardButton(button, callback_data=button) for button in data]).add(b0)
    return questions
