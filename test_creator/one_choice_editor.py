from flask import Flask, request, render_template

app = Flask(__name__)

item = {
    'type': None,
    'question': '',
    'answers': []
}


@app.route('/')
def upload_page(answers=0):
    return render_template(
        'oneChoiceEditor.html',
        amount_answers=len(item['answers']),
        answers=item['answers'],
        question=item['question']
    )


@app.route('/editor_one_choice/', methods=['POST'])
def create_one_choice_question():
    req = request.form['action']

    if req == 'create':
        amount = int(request.form['amount'])
        item['question'] = request.form['question']
        item['answers'] = [["", 0] for _ in range(amount)]
        return upload_page()
    else:
        item['question'] = request.form['question']
        for i in range(len(item['answers'])):
            text = request.form[f'answer-{i}']
            weight = request.form[f'weight-{i}']
            item['answers'][i][0] = text
            item['answers'][i][1] = weight

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



if __name__ == '__main__':
    app.run()
