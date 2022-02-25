from flask import Flask, request
from test_creator.py_archive import temp_file

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
    TASK['Q'] = ''
    TASK['A'] = [['', 0]]
    TASK['K'] = dict()

    if request.form['action'] == 'checkbox':
        TASK['type'] = 'multi'
        TASK['flag'] = 0
        return temp_file.rendering_multiple_choice(TASK)

    elif request.form['action'] == 'radio':
        TASK['type'] = 'radio'
        TASK['flag'] = 0
        TASK['point'] = 0
        return temp_file.rendering_one_choice(TASK)
    # TODO реализовать нажатие кнопки закрыть, упаковать тест и загрузить в БД


@app.route("/editor_one_chose/", methods=['POST'])
def edit_one_choice():
    return temp_file.edit_one_choice(TEST, TASK, request)


@app.route("/editor_checkbox/", methods=['POST'])
def edit_multiple_choice():
    return temp_file.edit_multiple_choice(TEST, TASK, request)


if __name__ == '__main__':
    app.run('127.0.0.10', 8090, debug=True)
