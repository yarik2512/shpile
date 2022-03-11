from flask import Flask, request, render_template

from welldone.materials import materials_add

ID = 1

app = Flask(__name__)


@app.route('/actions', methods=['POST'])
def make_some_action():
    act = request.form['action']
    if act == 'add-material':
        return materials_add.engine()
    return render_template(
        'account.html'
    )


def load_page_account():
    return render_template(
        'account.html'
    )
