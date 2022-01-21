from mysql.connector import connect, Error

con = connect(
    host='37.140.192.174',
    database='u1490660_default',
    user='u1490660_default',
    password='Ds3Nb2d5wYj6UW28'
)
cur = con.cursor()


def is_teacher(email):
    global con, cur
    cur.execute(
        f'SELECT * FROM `teachers` WHERE `mail` = "{email}"'
    )
    return not(len(cur.fetchall()) == 0)
