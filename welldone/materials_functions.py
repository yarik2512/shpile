def change_subject_to_ru(materials):
    m = []
    for i in range(0, len(materials)):
        m.append(list(materials[i]))
        subject = materials[i][4]
        if subject == 'alg':
            m[i][4] = 'Алгебра'
        elif subject == 'geom':
            m[i][4] = 'Геометрия'
        elif subject == 'soc':
            m[i][4] = 'Обществознание'
        elif subject == 'inf':
            m[i][4] = 'Информатика'
    return m
