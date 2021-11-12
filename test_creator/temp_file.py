from flask import render_template, request
import json
import link


def engine(test):
    print(test)
    return render_template(
        'test_editor.html',
        obj=test
    )


def rendering_multiple_choice(task):
    return render_template(
        'multi_chose_editor.html',
        question=task['Q'],
        lenght=len(task['A']) - 1,
        answers=task['A'],
        flag=task['flag']
    )


def rendering_one_choice(task):
    return render_template(
        'one_chose_editor.html',
        question=task['Q'],
        lenght=len(task['A']) - 1,
        answers=task['A'],
        point=task['point'],
        flag=task['flag']
    )


def export_task_to_db(task):
    task['A'] = task['A'][:-1]
    json_obj = json.dumps(task)
    link.insert_tasks('user', task['type'], json_obj)


def edit_multiple_choice(test, task, req):
    r = req.form['action']
    if r == 'add_answer' and not task['Q']:
        if not req.form['question']:
            task['flag'] = 1
            return rendering_multiple_choice(task)
        else:
            task['Q'] = req.form['question']
            task['A'].append(['', 0])
            return rendering_multiple_choice(task)
    elif r == 'add_answer':
        summa = 0
        for i in range(len(task['A']) - 1):
            answer = req.form[f"{i}"]
            weight = req.form[f"{i}-weight"]
            task['A'][i][0] = answer
            task['A'][i][1] = weight
            summa += int(weight)
        task['flag'] = 2 if summa != 100 else 0
        task['A'].append(['', 0])
        return rendering_multiple_choice(task)
    elif r == 'save' or r == 'close-with-save':
        summa = 0
        for i in range(len(task['A']) - 1):
            answer = req.form[f"{i}"]
            weight = req.form[f"{i}-weight"]
            task['A'][i][0] = answer
            task['A'][i][1] = weight
            summa += int(weight)
        task['flag'] = 2 if summa != 100 else 3
        print(task)
        if r == 'save':
            return rendering_multiple_choice(task)
        else:
            test['tasks'].append(task)
            export_task_to_db(task)
            return engine(test)
    elif r == 'close-without-save':
        return engine(test)
    elif r == 'cls-editor':
        if task['flag'] != 3:
            task['Q'] = req.form['question']
            for i in range(len(task['A']) - 1):
                answer = req.form[f"{i}"]
                weight = req.form[f"{i}-weight"]
                task['A'][i][0] = answer
                task['A'][i][1] = weight
            task['flag'] = -1
        test['tasks'].append(task)
        export_task_to_db(task)
        return engine(test)
    else:
        for i in range(len(task['A']) - 1):
            answer = req.form[f"{i}"]
            weight = req.form[f"{i}-weight"]
            task['A'][i][0] = answer
            task['A'][i][1] = weight
        index = int(r.split('-')[1])
        task['A'].pop(index)
        return rendering_multiple_choice(task)


def edit_one_choice(test, task, req):
    r = req.form['action']
    if r == 'add_answer' and not task['Q']:
        if not req.form['question']:
            task['flag'] = 1
            return rendering_one_choice(task)
        else:
            task['Q'] = req.form['question']
            task['A'].append(['', 0])
            return rendering_one_choice(task)
    elif r == 'add_answer' or r == 'save' or r == 'close-with-save':
        task['point'] = int(req.form['right-answer'])
        for i in range(len(task['A']) - 1):
            task['A'][i][0] = req.form[f"{i}"]
            if task['point'] == i:
                task['A'][i][1] = 100
            else:
                task['A'][i][1] = 0
        if r == 'add_answer':
            task['A'].append(['', 0])
        elif r == 'save':
            task['flag'] = 3
        else:
            test['tasks'].append(task)
            export_task_to_db(task)
            return engine(test)
        return rendering_one_choice(task)
    elif r == 'close-without-save':
        return engine(test)
    elif r == 'cls-editor':
        if task['flag'] != 3:
            task['point'] = int(req.form['right-answer'])
            task['Q'] = req.form['question']
            for i in range(len(task['A']) - 1):
                task['A'][i][0] = req.form[f"{i}"]
                if task['point'] == i:
                    task['A'][i][1] = 100
                else:
                    task['A'][i][1] = 0
            task['flag'] = -1
            return rendering_one_choice(task)
        test['tasks'].append(task)
        export_task_to_db(task)
        return engine(test)
    elif 'close' in r:
        task['point'] = int(request.form['right-answer'])
        for i in range(len(task['A']) - 1):
            task['A'][i][0] = req.form[f"{i}"]
            if task['point'] == i:
                task['A'][i][1] = 100
            else:
                task['A'][i][1] = 0

        index = int(r.split('-')[1])
        if index == int(task['point']):
            task['point'] = 0
        task['A'].pop(index)
        return rendering_one_choice(task)
