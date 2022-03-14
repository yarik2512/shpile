from flask import Flask, request, render_template
from welldone import db_functions

app = Flask(__name__)

CREATE_TEST_FLAG = False
TEST = []
BANK_OF_QUESTIONS = None


def show_question_by_user(USER=15):
    data = []
    for element in db_functions.export_tasks_by_user(USER):
        smth = dict()
        smth['id'] = element[0]
        smth['type'] = element[2]
        smth['question'] = element[3]
        data.append(smth)
    return data


@app.route('/')
def main_load_questions_bank():
    global CREATE_TEST_FLAG, BANK_OF_QUESTIONS
    BANK_OF_QUESTIONS = show_question_by_user()
    return render_template(
        'test_creator_questions_bank.html',
        createTestFlag=CREATE_TEST_FLAG,
        data=BANK_OF_QUESTIONS,
        length=len(BANK_OF_QUESTIONS)
    )


@app.route('/question-bank', methods=['POST'])
def action_question_bank():
    global CREATE_TEST_FLAG
    req = request.form['action']
    if req == 'create-test':
        CREATE_TEST_FLAG = True
    elif req == 'end-create-test':
        CREATE_TEST_FLAG = False
    else:
        cmd, index = req.split('-')
        if cmd == 'add':
            TEST.append(db_functions.get_task_by_id(int(index)))

    return main_load_questions_bank()
