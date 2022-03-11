from flask import Flask
from account import load_account

app = Flask(__name__)


@app.route('/')
def function():  # переименовать функцию
    return load_account.load_page_account()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
