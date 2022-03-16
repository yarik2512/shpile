from flask import request, render_template, session

from welldone.materials import materials_add, materials_filter
from welldone.test_creator import one_choice_editor
from welldone import connections

con, cur = connections.get_con_cur()


def get_info():
    global con, cur
    ID = session.get('ID')
    name = session.get('name')
    role = session.get('role')
    surname, name, secondname = name.split(' ')
    level = ''
    if role == 'student':
        cur.execute(
            f"SELECT id_groups FROM `students` WHERE id='{ID}'"
        )
        res = cur.fetchall()
        groups_id = res[0][0].split(';')
        groups = list()
        for group in groups_id:
            cur.execute(
                f"SELECT name FROM `groups` WHERE id='{group}'"
            )
            groups.append(cur.fetchall()[0][0])
        for group in groups:
            if '0' <= group[0] <= '9':
                level = group
                break
    return ID, name, role, surname, name, secondname, level


def make_some_action():
    global con, cur
    ID, name, role, surname, name, secondname, level = get_info()
    act = request.form['action']
    if act == 'add-material':
        return materials_add.engine()
    elif act == 'bank-of-materials':
        return materials_filter.engine()
    elif act == 'add-task':
        return one_choice_editor.upload_page()
    elif act == 'bank-of-tasks':
        return one_choice_editor.load_question_bank()
    return render_template(
        'account.html',
        id=ID,
        name=name,
        surname=surname,
        secondname=secondname,
        role=role,
        level=level
    )


def load_page_account():
    global con, cur
    ID, name, role, surname, name, secondname, level = get_info()
    return render_template(
        'account.html',
        id=ID,
        name=name,
        surname=surname,
        secondname=secondname,
        role=role,
        level=level
    )
