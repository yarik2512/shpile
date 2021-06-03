import json


def data_to_json(data_):
    data = dict()
    data["id"] = 0
    data["student"] = ""
    data["dep"] = ""
    data["arr"] = ""
    data["reason"] = ""
    data["tasks"] = dict()
    for subject, teacher in data_:
        data[subject][0] = ""
        data[subject][1] = teacher
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)
