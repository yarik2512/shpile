from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = '37.140.192.174'
app.config['MYSQL_DATABASE_USER'] = 'u1490660_default'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ds3Nb2d5wYj6UW28'
app.config['MYSQL_DATABASE_DB'] = 'u1490660_default'
mysql = MySQL()
mysql.init_app(app)
con = mysql.connect()
cur = con.cursor()


def get_con_cur():
    return con, cur
