from welldone import connections

con, cur = connections.get_con_cur()


def insert_tasks(user, type, task):
    global con, cur
    cur.execute(
        f"INSERT INTO tasks (id, author, type, obj) "
        f"VALUES (NULL, '{user}', '{type}', '{task}')"
    )
    con.commit()


def update_tests(user, title, test):
    global con, cur
    cur.execute(
        f"INSERT INTO tasks ('author', 'test_title', 'obj') VALUES ('{user}', '{title}', '{test}')"
    )
    con.commit()


def get_questions():
    global con, cur
    cur.execute("SELECT * FROM tasks")
    print(cur.fetchall())
