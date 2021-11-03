from flask import Flask, render_template, request
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
            #link.update_tasks('User', 'multi', json_test)
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
        #link.update_tasks('User', 'multi', json_test)
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


def func_4_radio(test, task, req):
    r = req.form['action']
    if r == 'add_answer' and not task['Q']:
        if not req.form['question']:
            task['flag'] = 1
            return rendering_one_choice(task)
        else:
            task['Q'] = req.form['question']
            task['A'].append(['', 0])
            return rendering_one_choice(task)
    elif r == 'add_answer':
        temp = []
        point = int(req.form['right-answer'])
        for i in range(len(task['A']) - 1):
            answer = req.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])
        task['A'] = temp
        task['A'].append(['', 0])
        return rendering_one_choice(task)
    elif r == 'save' or r == 'close-with-save':
        temp = []
        point = int(req.form['right-answer'])
        for i in range(len(task['A']) - 1):
            answer = request.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])

        task['A'] = temp
        json_test = json.dumps(task)
        task['flag'] = 3
        print(task)
        if r == 'save':
            return rendering_one_choice(task)
        else:
            test['tasks'].append(task)
            # link.update_tasks('User', 'multi', json_test)
            # TODO загрузить task в БД
            return engine(test)
        # TODO №1 Исправить функцию сборки вопроса: собираем json по
        #  вопросу, и отправляем его в БД. В словарь TEST теперь должен быть
        #  таким: {id_теста: номер, test_title: название теста (у нас оно
        #  нигде не вводится), tasks: список id-вопросов.
    elif r == 'close-without-save':
        return engine(test)
    elif r == 'cls-editor':
        if task['flag'] != 3:
            temp = []
            point = int(req.form['right-answer'])
            task['Q'] = req.form['question']
            for i in range(len(task['A']) - 1):
                answer = req.form[f"{i}"]
                if point == i:
                    temp.append([answer, 100, True])
                else:
                    temp.append([answer, 0, False])
            task['flag'] = -1
        test['tasks'].append(task)
        #link.update_tasks('User', 'multi', json_test)
        # TODO загрузить task в БД
        return engine(test)
    elif 'close' in r:
        temp = []
        point = int(request.form['right-answer'])

        for i in range(len(task['A']) - 1):
            answer = request.form[f"{i}"]
            if point == i:
                temp.append([answer, 100, True])
            else:
                temp.append([answer, 0, False])
        task['A'] = temp
        index = int(req.split('-')[1])
        if index == int(point):
            point = 0
        task['A'].pop(index)
        return rendering_one_choice(task)
