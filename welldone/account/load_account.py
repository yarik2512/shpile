from flask import Flask, request, render_template, session

from welldone.materials import materials_add
from welldone.materials import materials_filter

ID = session.get('ID')

app = Flask(__name__)


def make_some_action():
    act = request.form['action']
    if act == 'add-material':
        return materials_add.engine()
    elif act == 'bank-of-materials':
        return materials_filter.engine()
    return render_template(
        'account.html',
        id=ID
    )


def load_page_account():
    return render_template(
        'account.html',
        id=ID
    )
