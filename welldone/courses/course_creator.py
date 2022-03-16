from flask import Flask, render_template, request, session

from welldone import link_server
from welldone import db_functions
from welldone.materials import materials_functions
from welldone.account import load_account
from welldone.test_creator import one_choice_editor

app = Flask(__name__)
app.config['SECRET_KEY'] = '123_123_123'
res_mat = []
res_test = []
flag=''

@app.route('/course-create')
def create_course():
    return render_template(
        'course_creator.html'
    )


@app.route('/make-course', methods=['POST'])
def make_course():  # обработчик для формы
    global res_mat, res_test, flag
    title = request.form['name']
    description = request.form['description']
    act = request.form['action']
    materials = materials_functions.change_subject_to_ru(db_functions.materials_get_by_status(1))
    tests = db_functions.export_tests()
    if act == 'add-material':
        flag = 'mat'
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            dob_tests=res_test,
            materials=materials,
            tests=tests,
            title=title,
            description=description,
            flag=flag
        )
    elif act == 'add-test':
        flag = 'test'
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            dob_tests=res_test,
            tests=tests,
            title=title,
            description=description,
            flag=flag
        )
    elif act.startswith('addm-'):
        res_mat.append(materials[int(act.split('-')[1])])
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            materials=materials,
            tests=tests,
            dob_tests=res_test,
            title=title,
            description=description,
            flag=flag
        )
    elif act.startswith('closem-'):
        res_mat.pop(int(act.split('-')[1]))
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            dob_tests=res_test,
            materials=materials,
            tests=tests,
            title=title,
            description=description,
            flag=flag
        )
    elif act.startswith('addt-'):
        res_test.append(tests[int(act.split('-')[1])])
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            dob_tests=res_test,
            materials=materials,
            tests=tests,
            title=title,
            description=description,
            flag=flag
        )
    elif act.startswith('closet-'):
        res_test.pop(int(act.split('-')[1]))
        return render_template(
            'course_creator.html',
            dob_materials=res_mat,
            dob_tests=res_test,
            materials=materials,
            tests=tests,
            title=title,
            description=description,
            flag=flag
        )
    elif act == 'create':
        data = dict()
        data['name'] = title
        data['materials'] = res_mat
        data['tests'] = res_test
        data['description'] = description
        db_functions.course_add(data)
        return load_account.load_page_account()
