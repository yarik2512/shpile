from mysql.connector import connect, Error
import json

con = connect(
    host='37.140.192.174',
    database='u1490660_default',
    user='u1490660_default',
    password='Ds3Nb2d5wYj6UW28'
)
cur = con.cursor()


def new_task(user, obj):
    author = user
    typ = obj['type']
    question = obj['question']
    content = json.dumps(obj)
    global con, cur
    cur.execute(
        f"INSERT INTO tasks (id, author, type, question, content) "
        f"VALUES (NULL, '{author}', '{typ}', '{question}','{content}')"
    )
    con.commit()


def export_tasks_by_user(user):
    global con, cur
    cur.execute(
        f"SELECT * FROM tasks WHERE author='{user}'"
    )
    data = cur.fetchall()
    return data

def export_tests_by_user(id):
    global con, cur
    cur.execute(
        f"SELECT * FROM tests WHERE author='{id}'"
    )
    data = cur.fetchall()
    return data