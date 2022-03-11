from flask import Flask, render_template, request

import db_functions
import materials_functions

app = Flask(__name__)

ID = 1


@app.route('/')
def engine():
    materials = db_functions.materials_get_by_status(1)
    materials = materials_functions.change_subject_to_ru(materials)
    return render_template(
        'materials_bank.html',
        materials=materials
    )


@app.route('/materials-filter', methods=['POST'])
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


app.run('127.0.0.1', 8080, debug=True)
