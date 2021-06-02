import mysql.connector


def mentors(cur, student_id):
    lang = {'en': 'english', 'sp': 'spanish', 'ch': 'chinese', 'fr': 'french', 'ge': 'german', 'it': 'italian'}
    teachers = set()
    cur.execute(
        f"SELECT direction FROM students WHERE student_id='{student_id}'"
    )
    direction = cur.fetchone()[0]
    cur.execute(
        f"SELECT teacher_id FROM subjects WHERE direction='{direction}'"
    )
    teacher_ids = cur.fetchall()
    for teacher_id in teacher_ids:
        cur.execute(
            f"SELECT name FROM teachers WHERE id='{teacher_id[0]}'"
        )
        teacher = cur.fetchone()[0]
        teachers.add(teacher)
    cur.execute(
        f"SELECT languages FROM students WHERE student_id='{student_id}'"
    )
    tmp = cur.fetchone()[0]
    fl = tmp[0:2]
    flg = tmp[2]
    sl = tmp[3:5]
    slg = tmp[5]
    flang = lang[fl]
    slang = lang[sl]
    cur.execute(
        f"SELECT teacher FROM foreign_languages WHERE lang='{flang}' AND n_group='{flg}'"
    )
    flangt = cur.fetchone()[0]
    cur.execute(
        f"SELECT teacher FROM foreign_languages WHERE lang='{slang}' AND n_group='{slg}'"
    )
    slangt = cur.fetchone()[0]
    teachers.add(flangt)
    teachers.add(slangt)
    print(flangt, slangt)

    return teachers


con = mysql.connector.connect(
    host='mysql.79998136443.myjino.ru',
    database='79998136443_telebot',
    user='79998136443',
    password='fwFTy8x8'
)

cursor = con.cursor()


print(mentors(cursor, 29))
