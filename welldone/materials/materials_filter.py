from flask import Flask, render_template, request, session

from welldone import db_functions
from welldone.materials import materials_functions

app = Flask(__name__)

ID = session.get('ID')


def engine():
    materials = db_functions.materials_get_by_status(ID)
    materials = materials_functions.change_subject_to_ru(materials)
    return render_template(
        'materials_bank.html',
        materials=materials
    )


def materials_filter():
    subject = request.form['subject']
    level = request.form['level']
    if subject == 'all' and level == 'all':
        materials = db_functions.materials_get_by_status(1)
    elif subject == 'all':
        materials = db_functions.materials_get_by_level_status(level, 1)
    elif level == 'all':
        materials = db_functions.materials_get_by_subject_status(subject, 1)
    else:
        materials = db_functions.materials_get_by_subject_level_status(subject, level, 1)
    materials = materials_functions.change_subject_to_ru(materials)
    return render_template(
        'materials_bank.html',
        materials=materials
    )
