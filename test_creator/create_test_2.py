# /questionBank

from flask import Flask, render_template, request
import temp_file
import db_functions

app = Flask(__name__)


def show_questions_by_user(user_id):
    """
    Функция загружает личный банк вопросов от пользователя по его id.
    Возвращается размер списка и сам список.
    """
    request_to_db = db_functions.export_tasks_by_user(user_id)
    personal_bank_of_questions = []
    for element in request_to_db:
        smth = dict()
        smth['id'] = element[0]
        smth['type'] = element[2]
        smth['question'] = element[3]
        personal_bank_of_questions.append(smth)
    return personal_bank_of_questions, len(personal_bank_of_questions)


@app.route('/')
def main(ID):
    bank_of_questions, length = show_questions_by_user(ID)

    return render_template(
        'questionsBank.html',
        data=bank_of_questions,
        length=length
    )


if __name__ == '__main__':
    app.run()
