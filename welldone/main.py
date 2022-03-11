from flask import Flask
from account import load_account
from materials import materials_add

app = Flask(__name__)


@app.route('/')
def function():  # переименовать функцию
    return load_account.load_page_account()


@app.route('/actions', methods=['POST'])
def function_1():
    return load_account.make_some_action()


@app.route('/add_material', methods=['POST'])
def add_material():
    return materials_add.add_material()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
