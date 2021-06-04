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


def data_to_json(data, path):
    """
    Функция записи в json файл
    :param data: словарь данных
    :param path: путь к json файлу
    """
    with open(path, "w") as write_file:
        json.dump(data, write_file)


def json_to_data(path):
    """
    Функция чтения json файла
    :param path: путь к файлу
    :return: словарь из json объекта
    """
    with open(path) as f:
        data = json.load(f)
    return data


def add_task(subject, task, date, path):
    """
    Функция добавления задания
    :param subject: предмет
    :param task: задание
    :param date: дата сдачи задания
    :param path: путь к json файлу
    """
    print(subject, task)
    data = json_to_data(path)
    data['tasks'][subject.capitalize()][0] = task.capitalize()
    data['tasks'][subject.capitalize()][2] = date
    data_to_json(data, path)


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
