import os
from flask import Flask, request, render_template

# Используем несколько временных переменных, значение которых далее будет загружаться из базы данных
TITLE = 'Биология'

app = Flask(__name__)


def renumerate(catalogs):
    for i in range(len(catalogs)):
        number = i + 1
        str_number = str(number // 10) + str(number % 10)
        title = catalogs[i].split('_')[1]
        os.rename(f"{TITLE}/{catalogs[i]}", f"{TITLE}/{str_number}_{title}")


def load_course_editor_html():
    catalogs = [item.split('_') for item in os.listdir(f'{TITLE}')]
    return render_template(
        'courseEditor.html',
        courseTitle=TITLE,
        courseChapters=catalogs
    )


def load_chapter_editor_html(title):
    return render_template(
        'chapterEditor.html',
        courseTitle=TITLE,
        chapterTitle=title
    )


@app.route('/')
def load_course():
    return load_course_editor_html()


@app.route('/chapter-create', methods=['POST'])
def add_chapter():
    title = request.form['chapterTitle']
    number = len(os.listdir(f"{TITLE}")) + 1
    str_number = str(number // 10) + str(number % 10)
    if os.path.isdir(f'{TITLE}/{str_number}_{title}'):
        # TODO реализовать сообщение об ошибке
        return load_course_editor_html()
    else:
        os.mkdir(f'{TITLE}/{str_number}_{title}')
        return load_course_editor_html()


@app.route('/actions-with-chapter', methods=["POST"])
def action_with_chapters():
    btn, title = request.form['action'].split('_')
    catalogs = os.listdir(f"{TITLE}")
    fullname_catalog = None
    for item in catalogs:
        if title in item:
            fullname_catalog = item

    if btn == 'del':
        os.rmdir(f'{TITLE}/{fullname_catalog}')
        catalogs = os.listdir(f"{TITLE}")
        renumerate(catalogs)
    elif btn == 'up':
        catalogs = os.listdir(f"{TITLE}")
        index = catalogs.index(fullname_catalog)
        if index > 0:
            catalogs[index], catalogs[index - 1] = catalogs[index - 1], catalogs[index]
            renumerate(catalogs)
    elif btn == 'down':
        catalogs = os.listdir(f"{TITLE}")
        index = catalogs.index(fullname_catalog)
        if index < len(catalogs) - 1:
            catalogs[index], catalogs[index + 1] = catalogs[index + 1], catalogs[index]
            renumerate(catalogs)
    elif btn == 'edit':
        return load_chapter_editor_html(fullname_catalog)
    return load_course_editor_html()


if __name__ == '__main__':
    app.run()
