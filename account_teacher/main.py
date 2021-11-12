from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def start():
    return render_template(
        'teacher_account.html'
    )


app.run('127.0.0.1', 8001, debug=True)
