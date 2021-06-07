import json
from docxtpl import DocxTemplate
from docx import Document
import jinja2
from mentors import mentors


def create_data(student, dep, arr, reason, subjects):
    """
    Функция создания словаря из нужных данных
    :param student: имя ученика
    :param dep: дата отъезда
    :param arr: дата прибытия
    :param reason: причина
    :param subjects: словарь вида {'предмет': 'учитель'}
    :return: созданный словарь
    """
    data = dict()
    data["student"] = student
    data["dep"] = dep
    data["arr"] = arr
    data["reason"] = reason
    data["tasks"] = dict()
    for subject in subjects:
        data["tasks"][subject.capitalize()] = ("", subjects[subject], "")
    return data


def make_json(data, con, cur):
    """
    Функция записи в json файл
    :param data: словарь данных
    :param con: mysql.connector
    :param cur: con.cursor()
    """
    name = data['student']
    cur.execute(
        f"SELECT student_id FROM students WHERE fullname='{name}'"
    )
    student_id = cur.fetchone()[0]
    cur.execute(
        f"INSERT INTO files "
        f"VALUES (NULL, {student_id}, '{json.dumps(data)}'"
    )
    con.commit()


def update_json(data, runner_id, con, cur):
    """
    Функция изменения json в БД
    :param data: словарь данных
    :param runner_id: id бегунка
    :param con: mysql.connector
    :param cur: con.cursor()
    """
    cur.execute(
        f"UPDATE files SET json='{json.dumps(data)}' WHERE id='{runner_id}'"
    )
    con.commit()


def json_to_data(runner_id, con, cur):
    """
    Функция чтения json файла
    :param runner_id: id бегунка
    :param con: mysql.connector
    :param cur: con.cursor()
    :return: словарь из json объекта
    """
    cur.execute(
        f"SELECT json FROM files WHERE id='{runner_id}'"
    )
    data = cur.fetchone()[0]
    return data


def add_task(subject, task, date, runner_id, con, cur):
    """
    Функция добавления задания
    :param subject: предмет
    :param task: задание
    :param date: дата сдачи задания
    :param runner_id: id бегунка
    :param con: mysql.connector
    :param cur: con.cursor()
    """
    print(subject, task)
    data = json_to_data(runner_id, con, cur)
    data['tasks'][subject.capitalize()][0] = task.capitalize()
    data['tasks'][subject.capitalize()][2] = date
    update_json(data, runner_id, con, cur)


def make_doc(data):
    doc = DocxTemplate("docs/template.docx")
    context = {
        'name': data['student'],
        'dep': data['dep'],
        'arr': data['arr'],
        'reason': data['reason'],
        'tbl_contents': []
    }
    i = 0
    for subject, task in data['tasks'].items():
        context['tbl_contents'].append({'cols': [subject, task[0], task[1], task[2], "telgram-бот"]})
        # context['tbl_contents'][i]['cols'] = [subject, task[0], task[1], "telgram-бот"]
        i += 1
    for item in context['tbl_contents']:
        print(item)
    doc.render(context)
    doc.save("docs/output.docx")
