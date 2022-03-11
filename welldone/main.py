from flask import Flask, render_template, session
from account import load_account
from materials import materials_add, materials_filter
from auth import auth

app = Flask(__name__)


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


@app.route('/add_material', methods=['POST'])
def add_material():
    return materials_add.add_material()


@app.route('/materials-filter', methods=['POST'])
def materials_filter_main():
    return materials_filter.materials_filter()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
