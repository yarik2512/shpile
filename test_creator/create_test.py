from flask import Flask, render_template, request
import json
from link import update_tasks
import temp_file

app = Flask(__name__)

USER = 'admin'

TEST = dict()
LAST_ID = 0


@app.route('/')
def engine():
    return temp_file.engine(TEST)
    # return render_template(
    #     'test_editor.html',
    #     obj=TEST
    # )


@app.route('/create_test/', methods=['POST'])
def function():  # надо придумать адекватное название
    global TEST, LAST_ID
    LAST_ID = len(TEST) + 1
    TEST[LAST_ID] = dict()
    TEST[LAST_ID]['Q'] = ''
    TEST[LAST_ID]['A'] = [['', 0]]
    TEST[LAST_ID]['K'] = dict()

    if request.form['action'] == 'checkbox':
        TEST[LAST_ID]['type'] = 'multi'

        return render_template(
            'multi_chose_editor.html',
            question="",
            lenght=0,
            answers=[],
            flag=False
        )
    elif request.form['action'] == 'radio':
        TEST[LAST_ID]['type'] = 'radio'
        return render_template(
            'one_chose_editor.html',
            question="",
            lenght=0,
            answers=[],
            point=0
        )


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
        json_test = json.dumps(TEST)
        # update_tasks(USER, 'radio', json_test)
        print(TEST)
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


@app.route("/editor_checkbox/", methods=['POST'])
def add_new_question():  # надо придумать название функции
    global TEST, LAST_ID
    flag = False
    req = request.form['action']

    if req == 'add_answer' and len(TEST[LAST_ID]['Q']) == 0:
        question = request.form['question']
        TEST[LAST_ID]['Q'] = question
    elif req == 'add_answer':
        temp = []
        summa = 0
        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            weight = request.form[f"{i}-weight"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, weight, right_answer])
            summa += int(weight)
        flag = True if summa != 100 else False
        TEST[LAST_ID]['A'] = temp
        TEST[LAST_ID]['A'].append(['', 0])
    elif req == 'save':
        temp = []
        summa = 0
        for i in range(len(TEST[LAST_ID]['A'])):
            weight = request.form[f"{i}-weight"]
            answer = request.form[f"{i}"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, int(weight), right_answer])

        TEST[LAST_ID]['A'] = temp
        json_test = json.dumps(TEST)
        TEMP = json.loads(json_test)
        # update_tasks(USER, 'multi', json_test)
        print(TEMP)
        print(json_test)

    elif 'close' in req:
        temp = []
        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            weight = request.form[f"{i}-weight"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, weight, right_answer])
        TEST[LAST_ID]['A'] = temp
        index = int(req.split('-')[1])
        TEST[LAST_ID]['A'].pop(index)
    elif req == 'cls-editor':
        return render_template(
            'test_editor.html',
            obj=TEST
        )

    return render_template(
        'multi_chose_editor.html',
        question=TEST[LAST_ID]['Q'],
        lenght=len(TEST[LAST_ID]['A']),
        answers=TEST[LAST_ID]['A'],
        flag=flag
    )


app.run('127.0.0.1', 8090, debug=True)
