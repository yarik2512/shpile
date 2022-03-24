from flask import request, render_template, session

from welldone.materials import materials_add, materials_filter
from welldone.test_creator import one_choice_editor
from welldone import db_functions


def get_info():
    ID = session.get('ID')
    name = session.get('name')
    role = session.get('role')
    surname, name, secondname = name.split(' ')
    level = ''
    if role == 'student':
        groups_id = db_functions.student_get_groups_by_id(ID)
        groups = list()
        for group_id in groups_id:
            group_name = db_functions.group_get_name_by_id(group_id)
            if group_name != '':
                groups.append(group_name)
        for group in groups:
            if '0' <= group[0] <= '9':
                level = group
                break
    courses = list()
    if role == 'student':
        courses_id = db_functions.student_get_courses_by_id(ID)
        for course_id in courses_id:
            tmp = dict()
            tmp['id'] = course_id
            tmp['name'] = db_functions.course_get_name_by_id(course_id)
            if tmp['name'] == '':
                continue
            courses.append(tmp)
    elif role == 'teacher':
        courses_id = db_functions.teacher_get_courses_by_id(ID)
        for course_id in courses_id:
            tmp = dict()
            tmp['id'] = course_id
            tmp['name'] = db_functions.course_get_name_by_id(course_id)
            if tmp['name'] == '':
                continue
            courses.append(tmp)
    return ID, role, surname, name, secondname, level, courses


def make_some_action():
    ID, role, surname, name, secondname, level, courses = get_info()
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
        level=level,
        courses=courses
    )


def load_page_account():
    ID, role, surname, name, secondname, level, courses = get_info()
    return render_template(
        'account.html',
        id=ID,
        name=name,
        surname=surname,
        secondname=secondname,
        role=role,
        level=level,
        courses=courses
    )
