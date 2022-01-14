import requests
from flask import Flask, request, render_template

app = Flask(__name__)

COURSE = {}


@app.route('/')
def load_course_page():
    COURSE = {}
    return render_template(
        'course.html'
    )


@app.route('/add_chapter', methods=["POST"])
def add_chapter():
    global COURSE
    title_chapter = request.form['title_chapter']
    COURSE[(len(COURSE) + 1, title_chapter)] = []
    return render_template(
        'course.html',
        course=COURSE
    )


if __name__ == '__main__':
    app.run()
