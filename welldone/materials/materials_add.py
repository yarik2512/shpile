from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename

from welldone import link_server
from welldone import db_functions

app = Flask(__name__)


def engine():
    ID = session.get('ID')
    materials = db_functions.materials_get_by_author(ID)
    return render_template(
        'materials_add.html',
        materials=materials
    )


@app.route('/add-material', methods=['POST'])
def add_material():
    ID = session.get('ID')
    data = dict()
    data['name'] = request.form['name']
    data['author'] = ID
    data['level'] = request.form['level']
    data['subject'] = request.form['subject']
    data['file'] = request.files['file']
    data['link'] = 'materials/' + data['level'] + '/' + data['subject'] + '/' + secure_filename(data['file'].filename)
    link_server.add_file(data['file'], '/www/shpile.space/' + data['link'])
    db_functions.materials_add(data)
    materials = db_functions.materials_get_by_author(ID)
    return render_template(
        'materials_add.html',
        materials=materials
    )
