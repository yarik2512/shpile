from flask import Flask, request, render_template, session
from welldone import connections
from welldone.account import load_account

con, cur = connections.get_con_cur()
USER = None
ID = None


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
    if len(res) == 0:
        return render_template(
            'auth.html',
            error=2
        )
    USER = res[0][2]
    ID = res[0][0]
    session['ID'] = ID
    return load_account.load_page_account()
