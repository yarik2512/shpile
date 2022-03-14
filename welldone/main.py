from flask import Flask, render_template, session
from account import load_account
from materials import materials_add, materials_filter
from auth import auth
from test_creator import load_questions_bank, one_choice_editor

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


@app.route('/editor-one-choice', methods=['POST'])
def create_one_choice_question():
    return one_choice_editor.create_one_choice_question()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
