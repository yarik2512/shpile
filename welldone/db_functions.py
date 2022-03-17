from welldone.connections import get_con_cur
import json

con, cur = get_con_cur()


# functions with USERS
def user_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT name FROM users WHERE id={id}"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


# functions with STUDENTS
def student_get_groups_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT id_groups FROM students WHERE id={id}"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0].split(';')


def student_get_courses_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT id_courses FROM `students` WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return []
    return res[0][0].split(';')


# functions with TEACHERS
def teacher_get_courses_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT id_courses FROM `teachers` WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return []
    return res[0][0].split(';')


# functions with GROUPS
def group_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT name FROM `groups` WHERE id={id}"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


def groups_get_by_teacher_id(id):
    global con, cur
    cur.execute(
        f"SELECT classes FROM teachers WHERE id='{id}'"
    )
    data = cur.fetchall()[0][0].split(',')
    for i in range(len(data)):
        cur.execute(
            f"SELECT name FROM `groups` WHERE id='{data[i]}'"
        )
        data[i] = cur.fetchone()[0]
    return data


# functions with TASKS
def task_get_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT * FROM tasks WHERE id={id}"
    )
    data = cur.fetchone()
    print(data)
    return data


def new_task(user, obj):
    global con, cur
    author = user
    typ = obj['type']
    question = obj['question']
    content = json.dumps(obj)
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


# functions with TESTS
def export_tests():
    global con, cur
    cur.execute(
        f"SELECT * FROM tests"
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


def test_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT test_title FROM tests WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


def test_get_author_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT author FROM tests WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return user_get_name_by_id(res[0][0])


# functions with MATERIALS
def material_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT title FROM materials WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


def material_get_author_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT id_author FROM materials WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return user_get_name_by_id(res[0][0])


def material_get_path_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT path FROM materials WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


def materials_get_by_author(id_author):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE id_author='{id_author}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_subject(subject):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE subject='{subject}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_level(level):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE level='{level}' AND level='{level}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_status(status):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE status='{status}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_subject_status(subject, status):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE subject='{subject}' AND status='{status}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_level_status(level, status):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE level='{level}' AND status='{status}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_subject_level(subject, level):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE subject='{subject}' AND level='{level}'"
    )
    data = cur.fetchall()
    return data


def materials_get_by_subject_level_status(subject, level, status):
    global con, cur
    cur.execute(
        f"SELECT * FROM materials WHERE subject='{subject}' AND level='{level}' AND status='{status}'"
    )
    data = cur.fetchall()
    return data


def materials_update_status(status):
    global con, cur
    cur.execute(
        f"UPDATE materials SET status='{status}'"
    )


def materials_add(data):
    global con, cur
    cur.execute(
        f"INSERT INTO materials (id, id_author, title, level, subject, path, status) VALUES "
        f"(NULL, '{data['author']}', '{data['name']}', '{data['level']}', '{data['subject']}', '{data['link']}', 0)"
    )
    con.commit()


# functions with COURSES
def course_add(data, dob_gr):
    global con, cur
    temp = ''
    dob_gr = set(dob_gr)
    for gr in dob_gr:
        cur.execute(
            f"SELECT id FROM `groups` WHERE name='{gr}'"
        )
        temp = temp + str(cur.fetchone()[0]) + ','
    temp = temp[:-1]
    content = json.dumps(data)
    cur.execute(
        f"INSERT INTO courses (name, obj, id_groups) VALUES "
        f"('{data['name']}', '{content}', '{temp}')"
    )
    con.commit()


def course_get_obj_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT obj FROM courses WHERE id={id}"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return {}
    return json.loads(res[0][0])


def course_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT name FROM `courses` WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]
