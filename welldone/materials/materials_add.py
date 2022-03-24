from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import os

from welldone import db_functions


def engine():
    ID = session.get('ID')
    materials = db_functions.materials_get_by_author(ID)
    return render_template(
        'materials_add.html',
        materials=materials
    )


def add_material():
    ID = session.get('ID')
    data = dict()
    data['name'] = request.form['name']
    data['author'] = ID
    data['level'] = request.form['level']
    data['subject'] = request.form['subject']
    data['file'] = request.files['file']
    data['link'] = 'materials/' + data['level'] + '/' + data['subject'] + '/' + secure_filename(data['file'].filename)
    data['file'].save(os.path.join(data['link']))
    db_functions.materials_add(data)
    materials = db_functions.materials_get_by_author(ID)
    return render_template(
        'materials_add.html',
        materials=materials
    )
