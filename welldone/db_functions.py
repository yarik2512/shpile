from welldone.connections import get_con_cur
import json

con, cur = get_con_cur()


def user_get_name_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT name FROM `users` WHERE id='{id}'"
    )
    res = cur.fetchall()
    if len(res) == 0:
        return ''
    return res[0][0]


def get_task_by_id(id):
    global con, cur
    cur.execute(
        f"SELECT * FROM tasks WHERE id={id}"
    )
    data = cur.fetchone()
    print(data)
    return data


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


def course_add(data):
    global con, cur
    content = json.dumps(data)
    cur.execute(
        f"INSERT INTO courses (name, obj, id_groups) VALUES "
        f"('{data['name']}', '{content}', 1)"
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
