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
length = 0
otv = []


def create_course():
    global materials, groups, tests
    materials = materials_functions.change_subject_to_ru(db_functions.materials_get_by_status(1))
    tests = db_functions.export_tests()
    groups = db_functions.groups_get_by_teacher_id(session.get('ID'))
    return render_template(
        'course_creator.html',
        length=0
    )


def make_course():
    global flag, length
    cur = dict()
    a = dict()
    title = request.form['name']
    description = request.form['description']
    act = request.form['action']
    for i in range(length):
        if i == len(dob_gr):
            dob_gr.append('')
        if request.form['group-' + str(i)] != 'Выберите группу' and request.form['group-' + str(i)] != '':
            dob_gr[i] = request.form['group-' + str(i)]
    if act == 'add-material':
        flag = 'mat'
    elif act == 'add-test':
        flag = 'test'
    elif act.startswith('addm-'):
        temp = materials[int(act.split('-')[1])]
        a['mat'] = temp[0]
        otv.append(a.copy())
        a.clear()
        a['mat'] = temp[0]
        otv.append(a.copy())
        a.clear()
        cur['type'] = 'mat'
        cur['author'] = temp[1]
        cur['title'] = temp[2]
        cur['level'] = temp[3]
        cur['sub'] = temp[4]
        cur['path'] = temp[5]
        res.append(cur)
    elif act.startswith('addt-'):
        temp = tests[int(act.split('-')[1])]
        a['test'] = temp[0]
        otv.append(a.copy())
        a.clear()
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
        data['structure'] = otv
        data['description'] = description
        db_functions.course_add(data, dob_gr)
        return load_account.load_page_account()
    elif act == 'add-group':
        if length < len(groups):
            length = length + 1
    elif act.startswith('close-gr-'):
        dob_gr.pop(int(act.split('-')[2]))
        length = length - 1
    elif act.startswith('close-'):
        otv.pop(int(act.split('-')[1]))
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


def course_action():
    action = request.form['action']
    print(action)
    if action.startswith('show'):
        id = action.split('-')[1]
        course = db_functions.course_get_obj_by_id(id)
        if len(course) == 0:
            return render_template(
                "404.html"
            )
        course_tests = list()
        course_materials = list()
        name = course['name']
        description = course['description']
        for obj in course['structure']:
            if list(obj.keys())[0] == 'test':
                id = obj['test']
                tmp = dict()
                tmp['id'] = id
                tmp['title'] = db_functions.test_get_name_by_id(id)
                tmp['author'] = db_functions.test_get_author_by_id(id)
                course_tests.append(tmp)
            else:
                id = obj['mat']
                tmp = dict()
                tmp['id'] = id
                tmp['title'] = db_functions.material_get_name_by_id(id)
                tmp['author'] = db_functions.material_get_author_by_id(id)
                tmp['path'] = db_functions.material_get_path_by_id(id)
                course_materials.append(tmp)
        return render_template(
            "course.html",
            materials=course_materials,
            tests=course_tests,
            name=name,
            description=description
        )
