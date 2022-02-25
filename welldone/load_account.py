from flask import Flask, request, render_template
import add_materials

ID = 1

app = Flask(__name__)


@app.route('/actions', methods=['POST'])
def make_some_action():
    act = request.form['action']
    if act == 'add-material':
        return add_materials.engine()
    return render_template(
        'account.html'
    )


@app.route('/')
def load_page_account():
    return render_template(
        'account.html'
    )


if __name__ == '__main__':
    app.run('127.0.0.1', 8080, debug=True)
