from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def upload_page(answers=0):
    return render_template(
        'oneChoiceEditor.html',
        amount_answers=answers
    )


@app.route('/editor_one_choice/', methods=['POST'])
def create_one_choice_question():
    req = request.form['action']
    if req == 'create':
        amount = int(request.form['amount'])
        return upload_page(amount)


if __name__ == '__main__':
    app.run()
