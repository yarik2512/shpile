from flask import Flask, render_template, request, session
from welldone import db_functions
from welldone.materials import materials_functions
from welldone.account import load_account

app = Flask(__name__)
app.config['SECRET_KEY'] = '123_123_123'
res = []
flag = ''
dob_gr = []
groups = []
tests = []
materials = []
length=0

@app.route('/course-create')
def create_course():
    global materials, groups, tests
    materials = materials_functions.change_subject_to_ru(db_functions.materials_get_by_status(1))
    tests = db_functions.export_tests()
    groups = db_functions.get_groups_by_teacher(session.get('ID'))
    return render_template(
        'course_creator.html',
        length=0
    )


@app.route('/make-course', methods=['POST'])
def make_course():  # обработчик для формы
    global flag, length
    cur = dict()
    title = request.form['name']
    description = request.form['description']
    act = request.form['action']
    for i in range(length):
        print("i:"+str(i))
        if i == len(dob_gr):
            dob_gr.append('')
        if request.form['group-'+str(i)] != 'Выберите группу' and request.form['group-'+str(i)] != '':
            dob_gr[i] = request.form['group-'+str(i)]
    print(dob_gr)
    if act == 'add-material':
        flag = 'mat'
    elif act == 'add-test':
        flag = 'test'
    elif act.startswith('addm-'):
        temp = materials[int(act.split('-')[1])]
        cur['type'] = 'mat'
        cur['author'] = temp[1]
        cur['title'] = temp[2]
        cur['level'] = temp[3]
        cur['sub'] = temp[4]
        cur['path'] = temp[5]
        res.append(cur)
    elif act.startswith('addt-'):
        temp = tests[int(act.split('-')[1])]
        cur['type'] = 'test'
        cur['author'] = temp[1]
        cur['title'] = temp[2]
        cur['level'] = temp[3]
        cur['sub'] = temp[4]
        cur['obj'] = temp[5]
        res.append(cur)
    elif act == 'create':
        data = dict()
        data['name'] = title
        data['structure'] = res
        data['description'] = description
        db_functions.course_add(data, dob_gr)
        return load_account.load_page_account()
    elif act == 'add-group':
        print(length)
        if length < len(groups):
            length = length+1
    elif act.startswith('close-gr-'):
        dob_gr.pop(int(act.split('-')[2]))
        length = length-1
    elif act.startswith('close-'):
        res.pop(int(act.split('-')[1]))
    return render_template(
        'course_creator.html',
        dob=res,
        materials=materials,
        tests=tests,
        title=title,
        description=description,
        flag=flag,
        length=length,
        groups=groups,
        dob_gr=dob_gr
    )