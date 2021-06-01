import sqlite3

import mysql.connector
import functions as func
import integration as into

con = mysql.connector.connect(host='mysql.79998136443.myjino.ru', database='79998136443_telebot', user='79998136443',
                              password='fwFTy8x8')

cur = con.cursor()

# into.import_students(con, cur)
# into.import_kvds(con, cur)
# into.import_kvds_new(con, cur)
# into.update_kvds_in_students(con, cur)

# into.import_subjects(con, cur)
# into.import_foreign_languages(con, cur)
con.close()
