from flask import Flask, request, render_template, session
from welldone import db_functions

item = {
    'type': '',
    'question': '',
    'answers': []
}


def upload_page():
    return render_template(
        'test_creator_one_choice_editor.html',
        amount_answers=len(item['answers']),
        answers=item['answers'],
        question=item['question']
    )


def create_one_choice_question():
    req = request.form['action']

    if req == 'create':
        amount = int(request.form['amount'])
        item['question'] = request.form['question']
        item['answers'] = [["", 0] for _ in range(amount)]
        return upload_page()
    else:
        item['question'] = request.form['question']
        total = 0
        weight_count = 0
        for i in range(len(item['answers'])):
            text = request.form[f'answer-{i}']
            weight = int(request.form[f'weight-{i}'])
            item['answers'][i][0] = text
            item['answers'][i][1] = weight
            total += weight
            if weight != 0:
                weight_count += 1

        item['type'] = 'multi' if weight_count > 1 else 'one'

        if req == 'add':
            k = int(request.form['add-amount'])
            item['answers'] = item['answers'] + [["", 0] for _ in range(k)]
            return upload_page()

        if 'del' in req:
            index_to_delete = int(req.split('-')[1])
            item['answers'].pop(index_to_delete)
            return upload_page()

        if 'up' in req:
            index_to_up = int(req.split('-')[1])
            item['answers'][index_to_up], item['answers'][(index_to_up - 1) % len(item['answers'])] = \
                item['answers'][(index_to_up - 1) % len(item['answers'])], item['answers'][index_to_up]
            return upload_page()

        if 'down' in req:
            index_to_down = int(req.split('-')[1])
            item['answers'][index_to_down], item['answers'][(index_to_down + 1) % len(item['answers'])] = \
                item['answers'][(index_to_down + 1) % len(item['answers'])], item['answers'][index_to_down]
            return upload_page()

        if req == 'save':
            return load_question_bank()


def load_question_bank():
    USER = session.get('ID')
    db_functions.new_task(USER, item)
    temp = db_functions.export_tasks_by_user(USER)
    data = []
    for element in temp:
        smth = dict()
        smth['id'] = element[0]
        smth['type'] = element[2]
        smth['question'] = element[3]
        data.append(smth)
    return render_template(
        'test_creator_questions_bank.html',
        data=data,
        length=len(data)
    )
