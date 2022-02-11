from flask import Flask, render_template, request
from db_functions import export_tests_by_user
from create_test_2 import main

app = Flask(__name__)

ID = 15


@app.route('/')
def start():
    data = export_tests_by_user(ID)
    return render_template(
        'test_panel.html',
        data=data,
        length=len(data)
    )


@app.route('/test_panel', methods=['POST'])
def create_new_test():
    return main(ID)


app.run('127.0.0.1', 8001, debug=True)
