from flask import Flask, render_template, request

app = Flask(__name__)

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
        TEST[LAST_ID]['RA'] = []
        TEST[LAST_ID]['K'] = dict()
        return render_template(
            'multi_chose_editor.html',
            question="",
            lenght=0,
            answers=[]
        )


@app.route("/editor_checkbox/", methods=['POST'])
def add_new_question():  # надо придумать название функции
    global TEST, LAST_ID
    if request.form['action'] == 'add_answer' and len(TEST[LAST_ID]['Q']) == 0:
        question = request.form['question']
        TEST[LAST_ID]['Q'] = question
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A']
        )
    elif request.form['action'] == 'add_answer':
        right_answer = request.form[f"{len(TEST[LAST_ID]['A']) - 1}-box"]
        answer = request.form[f"{len(TEST[LAST_ID]['A']) - 1}"]
        weight = request.form[f"{len(TEST[LAST_ID]['A']) - 1}-weight"]
        TEST[LAST_ID]['A'][-1][0] = answer
        TEST[LAST_ID]['A'][-1][1] = weight
        TEST[LAST_ID]['A'].append(['', 0])
        print(right_answer, answer, weight)
        print(TEST[LAST_ID]['A'])
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A']
        )
    elif request.form['action'] == 'save':
        print(TEST)
        return render_template(
            'multi_chose_editor.html',
            question=TEST[LAST_ID]['Q'],
            lenght=len(TEST[LAST_ID]['A']),
            answers=TEST[LAST_ID]['A']
        )


app.run('127.0.0.1', 8090, debug=True)
