from flask import Flask, request, render_template, session
from welldone import db_functions
from welldone.tests import create_test

app = Flask(__name__)

CREATE_TEST_FLAG = False
TEST = []
BANK_OF_QUESTIONS = None


def show_question_by_user(USER):
    data = []
    for element in db_functions.export_tasks_by_user(USER):
        smth = dict()
        smth['id'] = element[0]
        smth['type'] = element[2]
        smth['question'] = element[3]
        data.append(smth)
    return data


def main_load_questions_bank():
    global CREATE_TEST_FLAG, BANK_OF_QUESTIONS
    BANK_OF_QUESTIONS = show_question_by_user(session.get('ID'))
    if CREATE_TEST_FLAG:
        return create_test.create_test()
    return render_template(
        'test_creator_questions_bank.html',
        data=BANK_OF_QUESTIONS,
        length=len(BANK_OF_QUESTIONS)
    )


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
            TEST.append(db_functions.task_get_by_id(int(index)))

    return main_load_questions_bank()
