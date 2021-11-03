from flask import Flask, render_template, request
import json
from link import update_tasks
import temp_file

app = Flask(__name__)

USER = 'admin'

TEST = dict()
TEST['tasks'] = []
LAST_ID = 0
TASK = dict()


@app.route('/')
def engine():
    return temp_file.engine(TEST)


@app.route('/create_test/', methods=['POST'])
def function():  # надо придумать адекватное название
    # global TEST, LAST_ID
    # LAST_ID = len(TEST) + 1
    # TEST[LAST_ID] = dict()
    TASK['Q'] = ''
    TASK['A'] = [['', 0]]
    TASK['K'] = dict()

    if request.form['action'] == 'checkbox':
        TASK['type'] = 'multi'
        TASK['flag'] = 0
        return temp_file.rendering_multiple_choice(TASK)

    elif request.form['action'] == 'radio':
        TASK['type'] = 'radio'
        TASK['point'] = 0
        return temp_file.rendering_one_choice(TASK)
    # TODO реализовать нажатие кнопки закрыть, упаковать тест и загрузить в БД


@app.route("/editor_one_chose/", methods=['POST'])
def edit_multiple_choice():
    return temp_file.func_4_radio(TEST, TASK, request)


#
# @app.route("/close-editor-multi", methods=['POST'])
# def close_editor_function():
#     global TASK
#     if request.form['action'] == 'close-with-save':
#         TASK['flag'] = 3
#         print(request.form)
#         return temp_file.rendering_multiple_choice(TASK)
#     elif request.form['action'] == 'close-without-save':
#         TASK = {}
#         return temp_file.engine(TEST)


@app.route("/editor_checkbox/", methods=['POST'])
def edit_multiple_choice():
    return temp_file.edit_multiple_choice(TEST, TASK, request)


app.run('127.0.0.1', 8088, debug=True)
