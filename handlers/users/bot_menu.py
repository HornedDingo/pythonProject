from database.db import db
from database.get import mysql7, mysql8, mysql10, mysql11, mysql12
from handlers.users.bot_authorization import q_done
from handlers.users.start import search_id


cursor2 = db.cursor()
cursor2.execute("USE pollbase")


def search_for_users_id(id_q):
    q_id = id_q
    cursor2.execute(mysql7, (q_id,))
    for_users_id = cursor2.fetchone()
    answer_1 = int(''.join(map(str, for_users_id)))
    if answer_1 > 0:
        answer_2 = answer_1
    return answer_2


def q_is_active(id_q):
    q_id = id_q
    cursor2.execute(mysql8, (q_id,))
    is_active = int(''.join(map(str, cursor2.fetchone())))
    if is_active > 0:
        actual_q = True
    else:
        actual_q = False
    return actual_q


def q_count():
    cursor2.execute(mysql10)
    q_number = cursor2.fetchone()
    return q_number


def q_name(id_q):
    q_id = id_q
    cursor2.execute(mysql11, (q_id,))
    name_q = cursor2.fetchone()
    return name_q


def show_list(user_id):
    b = []
    a = []
    cursor2.execute(mysql12)
    qs = cursor2.fetchall()
    n = len(qs)
    for i in range(0, n):
        b.append(int(''.join(map(str, qs[i]))))
        q_user_id = search_for_users_id(b[i])
        q_active = q_is_active(b[i])
        q_answered = q_done(b[i], search_id(user_id))
        print(q_answered)
        if ((q_user_id == 4) or (q_user_id == 1)) & (q_active is True) & (q_answered is False):
            a.append(''.join(q_name(b[i])))
    return a
