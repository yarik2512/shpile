from flask import Flask, request, render_template, session

from welldone.materials import materials_add
from welldone.materials import materials_filter
from welldone.test_creator import one_choice_editor

app = Flask(__name__)


def make_some_action():
    ID = session.get('ID')
    act = request.form['action']
    if act == 'add-material':
        return materials_add.engine()
    elif act == 'bank-of-materials':
        return materials_filter.engine()
    elif act == 'add-task':
        return one_choice_editor.upload_page()
    elif act == 'bank-of-tasks':
        return one_choice_editor.load_question_bank()
    return render_template(
        'account.html',
        id=ID
    )


def load_page_account():
    ID = session.get('ID')
    return render_template(
        'account.html',
        id=ID
    )
