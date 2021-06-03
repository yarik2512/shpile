from integration import import_kvds_new_new
from integration import update_students_kvds
import mysql.connector
from mentors import mentors
from file import create_data
from file import make_doc

con = mysql.connector.connect(
    host='mysql.79998136443.myjino.ru',
    database='79998136443_telebot',
    user='79998136443',
    password='fwFTy8x8'
)

cur = con.cursor()

teachers = mentors(cur, 29)
data = create_data("Коваль Яросав Владимирович", "01.01.21", "01.01.22", "надо", teachers)
make_doc(data)
