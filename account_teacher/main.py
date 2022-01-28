from flask import Flask, request, render_template, redirect
from mysql.connector import connect, Error

app = Flask(__name__)

con = connect(
    host='37.140.192.174',
    database='u1490660_default',
    user='u1490660_default',
    password='Ds3Nb2d5wYj6UW28'
)
cur = con.cursor()


@app.route('/')
def start():
    return render_template(
        'auth.html'
    )


@app.route('/sign-in', methods=['POST'])
def sign_in():
    global con, cur
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
    else:
        return render_template(
            'user_account.html',
            name=res[0][2],
            teacher=(True if role == 'teachers' else False)
        )


app.run('127.0.0.1', 8001, debug=True)
