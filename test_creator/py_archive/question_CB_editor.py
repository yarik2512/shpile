from flask import Flask, render_template, request
from create_test import app


@app.route('/create_test/', methods=['POST'])
def create_checkbox_task(TASK):
    print('Привет!')
    return render_template(
        'archive/test_editor.html'
    )


def temo():
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
        # json_test = json.dumps(TEST)
        # TEMP = json.loads(json_test)
        # update_tasks(USER, 'multi', json_test)
        # print(TEMP)
        # print(json_test)

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
            'archive/test_editor.html',
            obj=TEST
        )

    return render_template(
        'archive/multi_chose_editor.html',
        question=TEST[LAST_ID]['Q'],
        lenght=len(TEST[LAST_ID]['A']),
        answers=TEST[LAST_ID]['A'],
        flag=flag
    )
