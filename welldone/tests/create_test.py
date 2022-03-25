from flask import Flask, render_template, request, session
from welldone import db_functions
from welldone.materials import materials_functions
from welldone.account import load_account

app = Flask(__name__)
app.config['SECRET_KEY'] = '123_123_123'
res = []
tasks = []
id = []


@app.route('/test-create')
def create_test():
    global tasks
    tasks = db_functions.export_tasks_by_user(session.get('ID'))
    return render_template(
        'test-creator.html',
    )


@app.route('/make-test', methods=['POST'])
def make_test():  # обработчик для формы
    global id, tasks
    cur = dict()
    title = request.form['name']
    act = request.form['action']
    if act.startswith('add-'):
        temp = tasks[int(act.split('-')[1])]
        id.append(temp[0])
        cur['author'] = temp[1]
        cur['title'] = temp[2]
        cur['level'] = temp[3]
        cur['sub'] = temp[4]
        cur['path'] = temp[5]
        res.append(cur)
    elif act == 'create':
        data = dict()
        data['author'] = session.get('ID')
        data['name'] = title
        data['tasks'] = id
        data['sub'] = request.form['sub']
        data['level'] = request.form['level']
        db_functions.tests_add(data)
        return load_account.load_page_account()
    elif act.startswith('close-'):
        id.pop(int(act.split('-')[1]))
        res.pop(int(act.split('-')[1]))
    return render_template(
        'test-creator.html',
        dob=res,
        tasks=tasks,
        title=title,
    )