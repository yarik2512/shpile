from flask import Flask, render_template, request
import json


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
        point=task['point']
    )


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
        task['flag'] = 3
        json_test = json.dumps(task)
        print(task)
        if r == 'save':
            return rendering_multiple_choice(task)
        else:
            test['tasks'].append(task)
            # TODO загрузить task в БД
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
        # TODO загрузить task в БД
        return engine(test)
    else:
        # TODO проверить как работает удаление элементов из списка
        temp = []
        for i in range(len(task['A'])):
            answer = request.form[f"{i}"]
            weight = request.form[f"{i}-weight"]
            right_answer = True if int(weight) > 0 else False
            temp.append([answer, weight, right_answer])
        task['A'] = temp
        index = int(req.split('-')[1])
        task['A'].pop(index)

        return rendering_multiple_choice(task)
