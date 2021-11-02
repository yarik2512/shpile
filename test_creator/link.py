from mysql.connector import connect, Error


def update_tasks(user, type, task):
    con = connect(
        host='37.140.192.174',
        database='u1490660_default',
        user='u1490660_default',
        password='Ds3Nb2d5wYj6UW28'
    )

    cur = con.cursor()

    cur.execute(
        f"INSERT INTO tasks ('author', 'type', 'obj') VALUES ('{user}', '{type}', '{task}')"
    )

    con.commit()


def get_questions():
    con = connect(
        host='37.140.192.174',
        database='u1490660_default',
        user='u1490660_default',
        password='Ds3Nb2d5wYj6UW28'
    )

    cur = con.cursor()

    cur.execute("SELECT * FROM tasks")

    print(cur.fetchall())

