import mysql.connector


def mentors(cur, student_id):
    """Функция mentors:
            аргументы: курсор БД, id гимназиста;
            значение: словарь (предмет: учитель)"""
    # словарь с сокращением названий языков
    lang = {'en': 'english', 'sp': 'spanish', 'ch': 'chinese', 'fr': 'french', 'ge': 'german', 'it': 'italian'}

    teachers = dict()

    # узнаем направление подготовки ученика
    cur.execute(
        f"SELECT direction FROM students WHERE student_id='{student_id}'"
    )
    direction = cur.fetchone()[0]

    # узнаем всех преподавателей направления подготовки
    cur.execute(
        f"SELECT teacher_id, subject FROM subjects WHERE direction='{direction}'"
    )
    teacher_ids = cur.fetchall()

    # нужно узнать как зовут преподов в этом направлении
    for teacher_id in teacher_ids:
        cur.execute(
            f"SELECT name FROM teachers WHERE id='{teacher_id[0]}'"
        )
        teacher = cur.fetchone()[0]
        teachers[teacher_id[1]] = teacher

    # узнаем преподавателей иностранных языко, сначала узнаем языки и группы у студента
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

    # узнаем преподавателя по английскому языку
    cur.execute(
        f"SELECT teacher FROM foreign_languages WHERE lang='{flang}' AND n_group='{flg}'"
    )
    flangt = cur.fetchone()[0]
    teachers['Английский язык'] = flangt

    # узнаем преподавателя второго языка
    cur.execute(
        f"SELECT teacher, language FROM foreign_languages WHERE lang='{slang}' AND n_group='{slg}'"
    )
    slangt = cur.fetchone()
    teachers[f'Второй иностранный язык ({slangt[1]})'] = slangt[0]

    # узнаем преподавателей по модулям
    cur.execute(
        f"SELECT kvds FROM students WHERE student_id='{student_id}'"
    )
    kvds = cur.fetchone()[0].split(';')

    for kvd in kvds:
        cur.execute(
            f"SELECT name_kvd FROM kvds WHERE id_kvd='{kvd}'"
        )
        name_kvd = cur.fetchone()[0]
        # удалить потом cur.fetchall()
        cur.execute(
            f"SELECT teacher FROM kvds WHERE name_kvd='{name_kvd}'"
        )
        kvd_teachers = ', '.join([item[0] for item in cur.fetchall()])
        teachers[name_kvd] = kvd_teachers
    return teachers


con = mysql.connector.connect(
    host='mysql.79998136443.myjino.ru',
    database='79998136443_telebot',
    user='79998136443',
    password='fwFTy8x8'
)

cursor = con.cursor()

print(mentors(cursor, 4))
