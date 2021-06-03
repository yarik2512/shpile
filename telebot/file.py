import json


def create_data(file_id, student, dep, arr, reason, subjects):
    """
    Функция создания словаря из нужных данных
    :param file_id: id бегунка
    :param student: имя ученика
    :param dep: дата отъезда
    :param arr: дата прибытия
    :param reason: причина
    :param subjects: словарь вида {'предмет': 'учитель'}
    :return: созданный словарь
    """
    data = dict()
    data["id"] = file_id
    data["student"] = student
    data["dep"] = dep
    data["arr"] = arr
    data["reason"] = reason
    data["tasks"] = dict()
    for subject in subjects:
        data["tasks"][subject.capitalize()] = ("", subjects[subject].capitalize())
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


def add_task(subject, task, path):
    """
    Функция добавления задания
    :param subject: предмет
    :param task: задание
    :param path: путь к json файлу
    """
    print(subject, task)
    data = json_to_data(path)
    data['tasks'][subject.capitalize()][0] = task.capitalize()
    data_to_json(data, path)
