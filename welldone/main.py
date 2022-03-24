from flask import Flask, render_template, send_file
from account import load_account
from materials import materials_add, materials_filter
from auth import auth
from test_creator import load_questions_bank, one_choice_editor
from courses import course_creator
from tests import create_test

app = Flask(__name__)
app.config['SECRET_KEY'] = '123_123_123'


@app.route('/')
def function():  # переименовать функцию
    return render_template(
        'auth.html'
    )


@app.route('/sign-in', methods=['POST'])
def authorization():
    return auth.sign_in()


@app.route('/actions', methods=['POST'])
def function_1():
    return load_account.make_some_action()


@app.route('/add-material', methods=['POST'])
def add_material():
    return materials_add.add_material()


@app.route('/materials-filter', methods=['POST'])
def materials_filter_main():
    return materials_filter.materials_filter()


@app.route('/question-bank', methods=['POST'])
def action_question_bank():
    return load_questions_bank.action_question_bank()


@app.route('/back', methods=['POST'])
def back():
    return load_account.load_page_account()


@app.route('/course-create', methods=['POST'])
def create_course():
    return course_creator.create_course()


@app.route('/make-course', methods=['POST'])
def make_course():
    return course_creator.make_course()


@app.route('/course-actions', methods=['POST'])
def course_action():
    return course_creator.course_action()


@app.route('/make-test', methods=['POST'])
def make_test():
    return create_test.create_test()


@app.route('/materials/<path:path>', methods=['GET'])
def get_material(path):
    print(path)
    return send_file("materials/" + path, as_attachment=True)


def main():
    app.run('80.78.241.153', 80, debug=True)
    # app.run('127.0.0.1', 80, debug=True)


if __name__ == '__main__':
    main()
