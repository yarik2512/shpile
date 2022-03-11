from welldone.connections import get_con_cur
import json

con, cur = get_con_cur()


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
