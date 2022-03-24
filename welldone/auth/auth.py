from flask import Flask, request, render_template, session
from welldone.account import load_account
from welldone.main import get_con_cur

con, cur = get_con_cur()
USER = None
ID = None


def sign_in():
    global con, cur, USER, ID
    mail = request.form['email']
    password = request.form['password']
    cur.execute(
        f"SELECT * FROM `users`"
        f"WHERE mail = '{mail}' AND password = '{password}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return render_template(
            'auth.html',
            error=2
        )
    USER = res[0][2]
    ID = res[0][0]
    if res[0][4] == 2:
        ROLE = 'student'
    elif res[0][4] == 1:
        ROLE = 'teacher'
    else:
        ROLE = 'admin'
    session['ID'] = ID
    session['name'] = USER
    session['role'] = ROLE
    return load_account.load_page_account()
