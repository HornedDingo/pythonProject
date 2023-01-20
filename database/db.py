import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rgaatrfla",
    port="3306",
    database="pollbase"
)


cursor = db.cursor()
cursor.execute("USE pollbase")
