from flask import Flask, render_template, request
import json
from link import update_tasks

app = Flask(__name__)

USER = 'admin'

TEST = dict()
LAST_ID = 0


@app.route('/')
def engine():
    return render_template(
        'test_editor.html'
    )


@app.route('/create_test/', methods=['POST'])
def function():  # надо придумать адекватное название
    if request.form['action'] == 'checkbox':
        global TEST, LAST_ID
        LAST_ID = len(TEST) + 1
        TEST[LAST_ID] = dict()
        TEST[LAST_ID]['type'] = 'multi'
        TEST[LAST_ID]['Q'] = ''
        TEST[LAST_ID]['A'] = [['', 0]]
        TEST[LAST_ID]['K'] = dict()
        return render_template(
            'multi_chose_editor.html',
            question="",
            lenght=0,
            answers=[],
            flag=False
        )


@app.route("/editor_checkbox/", methods=['POST'])
def add_new_question():  # надо придумать название функции
    global TEST, LAST_ID
    req = request.form['action']
    if req == 'add_answer' and len(TEST[LAST_ID]['Q']) == 0:
        question = request.form['question']
        TEST[LAST_ID]['Q'] = question
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            flag=False
        )
    elif req == 'add_answer':
        temp = []
        for i in range(len(TEST[LAST_ID]['A'])):
            answer = request.form[f"{i}"]
            weight = request.form[f"{i}-weight"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, weight, right_answer])
        TEST[LAST_ID]['A'] = temp
        TEST[LAST_ID]['A'].append(['', 0])

        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            flag=False
        )
    elif req == 'save':
        temp = []
        summa = 0
        for i in range(len(TEST[LAST_ID]['A'])):
            weight = request.form[f"{i}-weight"]
            answer = request.form[f"{i}"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, int(weight), right_answer])
            summa += int(weight)

        TEST[LAST_ID]['A'] = temp
        json_test = json.dumps(TEST)
        update_tasks(USER, 'multi', json_test)
        print(json_test)
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            flag=True if summa != 100 else False
        )
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
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A'],
            flag=False
        )


app.run('127.0.0.1', 8090, debug=True)
