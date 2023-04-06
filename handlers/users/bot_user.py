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
