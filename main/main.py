from flask import Flask, request, render_template, redirect
from mysql.connector import connect, Error
from db_functions import export_tests_by_user
from create_test_2 import main

app = Flask(__name__)

con = connect(
    host='37.140.192.174',
    database='u1490660_default',
    user='u1490660_default',
    password='Ds3Nb2d5wYj6UW28'
)
cur = con.cursor()

USER = ""
ID = 0

@app.route('/')
def start():
    return render_template(
        'auth.html'
    )


@app.route('/sign-in', methods=['POST'])
def sign_in():
    global con, cur, USER, ID
    mail = request.form['email']
    password = request.form['password']
    role = request.form['role'] + 's'
    cur.execute(
        f"SELECT * FROM `{role}`"
        f"WHERE mail = '{mail}' AND password = '{password}'"
    )
    res = cur.fetchall()
    con.commit()
    if len(res) == 0:
        return render_template(
            'auth.html'
        )
    USER = res[0][2]
    ID = res[0][0]
    data = export_tests_by_user(ID)
    return render_template(
        'user_account.html',
        name=USER,
        teacher=(True if role == 'teachers' else False),
        data=data,
        length=len(data)
    )


@app.route('/test_panel', methods=['POST'])
def create_new_test():
    global USER, ID
    return main(ID)


app.run('127.0.0.1', 8001, debug=True)
