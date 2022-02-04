from flask import Flask, render_template, request
from db_functions import export_tests_by_user

app = Flask(__name__)

ID = 1


@app.route('/')
def start():
    data = export_tests_by_user(ID);
    return render_template(
        'test_panel.html',
        data=data,
        length=len(data)
    )


app.run('127.0.0.1', 8001, debug=True)
