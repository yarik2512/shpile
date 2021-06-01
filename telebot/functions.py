import sqlite3


# TODO функция добавления студента в языковую группу
# TODO функция добавления курса внеурочной деятельности
# TODO функция добавления студента на курс внеурочной деятельности
# TODO нужно написать функции для обновления информации о проектах, языковых группах и тд.
# TODO написать функции о получении информации о том, какие квд посещает студент и какие языки изучает
# TODO написать функцию для добавления учебного предмета


def add_new_language_group(cur, lang, n_group, language, id_teacher='NULL', teacher='NULL'):
    """Функция добавляет языковую группу в таблицу foreign_languages. Аргументы id_teacher и teacher не являются
    обязательными, то есть можно добавить группу, а преподавателя уже потом."""
    cur.execute(
        f"INSERT INTO foreign_languages "
        f"VALUES (NULL, '{lang}', {n_group}, '{language}', {id_teacher}, '{teacher}')"
    )
    cur.connection.commit()


def change_language_teacher(cur, lang, n_group, teacher):
    """Функция изменения преподавателя в языковой группе. Также работает как и как функция добавления
    преподавателя в языковую группу, если ранее его не было."""
    cur.execute(
        f"UPDATE foreign_languages SET teacher='{teacher}' WHERE lang='{lang}' and n_group={n_group}"
    )
    cur.connection.commit()


def change_language_n_group(cur, id_group, new_number):
    """Функция позволяет изменить номер языковой группы по id группы."""
    cur.execute(
        f"UPDATE foreign_languages SET n_group={new_number} WHERE id={id_group}"
    )
    cur.connection.commit()


def get_ids_group_foreign_language(cur, lang):
    """Получение id языковой групп по полю lang"""
    pass


def enrollment_project(con, cur, id_project, id_student):
    """Функция для записи гимназиста на проект"""
    cur.execute(
        f"UPDATE students SET project={id_project} WHERE student_id={id_student}"
    )
    con.commit()


def get_student_id(cur, student):
    """Функция для получения id студента в БД"""
    surname, name, last_name = student.split()
    cur.execute(
        f"SELECT student_id FROM students "
        f"WHERE surname='{surname}' and name='{name}' and lastname='{last_name}'"
    )
    id = cur.fetchone()
    if not (id is None):
        id = id[0]
    return id


def add_subject_temp(*args):
    """Функция принимает все необходимые для БД поля, заполняет таблицу subjects: предмет, преподаватель, класс,
    профиль, подпрофиль (0 - если предмет для всего профиля)"""
    con = sqlite3.connect("telebot_db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO subjects "
        f"VALUES (NULL, '{args[0]}', NULL, '{args[1]}', '{args[2]}', "
        f"'{args[3]}', '{args[4]}')"
    )
    cur.connection.commit()
    con.close()


def get_student_kvd(cur, id_student):
    result = cur.execute(
        "SELECT kvds "
        "FROM students "
        f"WHERE student_id='{id_student}'"
    ).fetchone()[0]

    return result


def get_student_subjects(cur, id_student):
    # нужно многие команды отсюда вынести в отдельные функции
    subjects = dict()

    # узнаем класс, профиль и подпрофиль ученика
    course, direction, sub_direction = cur.execute(
        f"SELECT course, direction, subdirection "
        f"FROM students "
        f"WHERE student_id='{id_student}'"
    ).fetchone()

    # получаем список предметов общий для профиля
    common_subjects = cur.execute(
        f"SELECT subject, teacher "
        f"FROM subjects "
        f"WHERE course='{course}' and direction='{direction}' and subdirection=0"
    ).fetchall()
    subjects['Общие предметы'] = sorted(common_subjects)

    # получаем список предметов для подпрофиля
    personal_subjects = cur.execute(
        f"SELECT subject, teacher "
        f"FROM subjects "
        f"WHERE course='{course}' and direction='{direction}' and subdirection='{sub_direction}'"
    ).fetchall()
    subjects['Профильные предметы'] = sorted(personal_subjects)

    # получаем список изучаемых языков
    languages = ['english', 'chinese', 'french', 'german', 'italian', 'spanish']

    # узнаем номер языковых групп
    lang_group = []
    for lang in languages:
        group = cur.execute(
            f"SELECT {lang} "
            f"FROM students "
            f"WHERE student_id={id_student}"
        ).fetchone()
        if not (group[0] is None):
            lang_group.append((lang, group[0]))

    # узнаем сами языки и их преподавателей, добавляем в общий список предметов
    f_lang = []
    for elem in lang_group:
        item = cur.execute(
            f"SELECT language, teacher "
            f"FROM foreign_languages "
            f"WHERE lang='{elem[0]}' and n_group={elem[1]}"
        ).fetchone()
        f_lang.append(item)
    subjects['Иностранные языки'] = sorted(f_lang)

    # получаем список курсов внеурочной деятельности для ученика, добавляем в общий список предметов
    kvds = cur.execute(
        f"SELECT kvds "
        f"FROM students "
        f"WHERE student_id={id_student}"
    ).fetchone()[0].split(';')
    del kvds[0]  # было лень исправлять ошибку, проще удалить первый элемент, он пустой
    temp_kvd = []
    for kvd in kvds:
        item = cur.execute(
            f"SELECT name_kvd, teacher FROM kvds WHERE id_kvd={kvd}"
        ).fetchone()
        temp_kvd.append(item)
    subjects['Модули'] = sorted(temp_kvd)
    return subjects


def students_kvds(cur, student):
    """Функция: студент => курсы внеурочной деятельности с преподавателем и часами"""
    # узнаем id гимназиста
    id_student = get_student_id(cur, student)
    kvds = cur.execute(
        f"SELECT kvds "
        f"FROM students "
        f"WHERE student_id={id_student}"
    ).fetchone()[0].split(';')[1:]
    temp_kvd = []
    for kvd in kvds:
        item = cur.execute(
            f"SELECT name_kvd, teacher FROM kvds WHERE id_kvd={kvd}"
        ).fetchone()
        temp_kvd.append(item)
    return temp_kvd


def students_languages(cur, student):
    id_student = get_student_id(cur, student)
    # получаем список изучаемых языков
    languages = ['english', 'chinese', 'french', 'german', 'italian', 'spanish']

    # узнаем номер языковых групп
    lang_group = []
    for lang in languages:
        group = cur.execute(
            f"SELECT {lang} "
            f"FROM students "
            f"WHERE student_id={id_student}"
        ).fetchone()
        if not (group[0] is None):
            lang_group.append((lang, group[0]))

    # узнаем сами языки и их преподавателей, добавляем в общий список предметов
    f_lang = []
    for elem in lang_group:
        item = cur.execute(
            f"SELECT language, teacher "
            f"FROM foreign_languages "
            f"WHERE lang='{elem[0]}' and n_group={elem[1]}"
        ).fetchone()
        f_lang.append(item)
    return f_lang


def get_info_about_student_curriculum(cur, student, course):
    id_student = get_student_id(cur, student)
    year, direction, sub_direction, languages = cur.execute(
        f"SELECT year_enrollment, direction, subdirection, languages FROM students WHERE student_id={id_student}"
    ).fetchone()
    data = cur.execute(
        f"SELECT * FROM curriculum WHERE direction='{direction}' and subdirection={sub_direction} and "
        f"course={course} and year={year}"
    ).fetchall()

    result = []
    for item in data:
        print(item)
        result.append([item[0]])

    first, second = languages.split(';')
    f_lang, n_first = first.split('-')
    s_lang, n_second = second.split('-')
    print(f_lang, n_first, s_lang, n_second)

