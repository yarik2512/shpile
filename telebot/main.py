from integration import import_kvds_new_new
from integration import update_students_kvds
import mysql.connector
from mentors import mentors
from file import create_data
from file import make_doc
from file import add_task
from file import data_to_json
from file import json_to_data

con = mysql.connector.connect(
    host='mysql.79998136443.myjino.ru',
    database='79998136443_telebot',
    user='79998136443',
    password='fwFTy8x8'
)

cur = con.cursor()

teachers = mentors(cur, 29)
data = create_data("Коваль Ярослав Владимирович", "01.01.21", "01.01.22", "надо", teachers)
data_to_json(data, "data_file.json")
add_task("алгебра", "авыфаовыфалвтыофмтвлфт ваоыфар выфраовыфро авыфо раовырф оврыф рваыоф рвоыф рвоырф аовырф авырф оаврыф лавырф оаврыфол арвоыфр аоврыфл арвол ыфравырф орвыфа овф выфо лавырф  оавылфр оалврыф ваыоылфр аовф", "01.01.21", "data_file.json")
data = json_to_data("data_file.json")
make_doc(data)
