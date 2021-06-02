from integration import import_kvds_new_new
from integration import update_students_kvds
import mysql.connector

con = mysql.connector.connect(
    host='mysql.79998136443.myjino.ru',
    database='79998136443_telebot',
    user='79998136443',
    password='fwFTy8x8'
)

cur = con.cursor()

update_students_kvds(con, cur)
