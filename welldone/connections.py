from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
mysql.init_app(app)
con = mysql.connect()
cur = con.cursor()


def get_con_cur():
    return con, cur
