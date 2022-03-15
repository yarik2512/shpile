from flask import Flask, render_template, request, session

from welldone import link_server
from welldone import db_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = '123_123_123'


@app.route('/course-create')
def create_course():
    return render_template(
        'course_creator.html'
    )

@app.route('/make-course')
def make_course():
    # обработчик для формы
