from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import link_server
import db_functions

app = Flask(__name__)


ID = 1


@app.route('/')
def engine():
    return render_template(
        'add_materials.html'
    )


@app.route('/add_material', methods=['POST'])
def add_material():
    global ID
    data = dict()
    data['name'] = request.form['name']
    data['author'] = ID
    data['level'] = request.form['level']
    data['subject'] = request.form['subject']
    data['file'] = request.files['file']
    data['link'] = 'materials/' + data['level'] + '/' + data['subject'] + '/' + secure_filename(data['file'].filename)
    # link_server.add_file(data['file'], '/www/shpile.space/' + data['link'])
    db_functions.materials_add(data)
    return render_template(
        'add_materials.html'
    )


app.run('127.0.0.1', 8080)
