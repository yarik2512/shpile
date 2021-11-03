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


# Реализация Виктора Швец
@app.route("/editor_one_chose/", methods=['POST'])
def func_4_radio():
    global TEST, LAST_ID
    req = request.form['action']

    if req == 'add_answer' and len(TEST[LAST_ID]['Q']) == 0:
        question = request.form['question']
        TEST[LAST_ID]['Q'] = question
        return render_template(
            'one_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            point=0
        )
    elif req == 'add_answer':
        temp = []
        point = int(request.form['right-answer'])
        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])
        TEST[LAST_ID]['A'] = temp
        TEST[LAST_ID]['A'].append(['', 0])

        return render_template(
            'one_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            point=int(point)
        )
    elif req == 'save':
        temp = []
        point = int(request.form['right-answer'])
        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])

        TEST[LAST_ID]['A'] = temp
        json_test = json.dumps(TEST[LAST_ID])
        # update_tasks(USER, 'radio', json_test)
        print(TEST)

        # TODO №1 Исправить функцию сборки вопроса: собираем json по
        #  вопросу, и отправляем его в БД. В словарь TEST теперь должен быть
        #  таким: {id_теста: номер, test_title: название теста (у нас оно
        #  нигде не вводится), tasks: список id-вопросов.

        return render_template(
            'one_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            point=int(point)
        )
    elif 'close' in req:
        temp = []
        point = int(request.form['right-answer'])

        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])
        TEST[LAST_ID]['A'] = temp
        index = int(req.split('-')[1])
        if index == int(point):
            point = 0
        TEST[LAST_ID]['A'].pop(index)
        return render_template(
            'one_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            point=int(point)
        )
    elif req == 'cls-editor':
        return render_template(
            'test_editor.html',
            obj=TEST
        )


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


app.run('127.0.0.1', 8090, debug=True)
