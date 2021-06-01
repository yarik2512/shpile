import sqlite3


def clear_result(temp):
    return [t[0] for t in temp]


class ForeignLanguages:
    """Класс ForeignLanguages используется для взаимодействия с соответствующей таблицей таблицей БД """

    def __init__(self):
        self.con = sqlite3.connect('telebot_db.db')
        self.cur = self.con.cursor()

    def get_id_group_by_n_group(self, lang, n_group):
        group_id = self.cur.execute(
            f"SELECT id FROM foreign_languages WHERE n_group={n_group} and lang='{lang}'"
        ).fetchone()[0]
        return group_id

    def get_id_group_by_lang(self, lang):
        ids = self.cur.execute(
            f"SELECT id FROM foreign_languages WHERE lang='{lang}'"
        ).fetchall()
        return clear_result(ids)

    def get_id_group_by_teacher(self, teacher):
        ids = self.cur.execute(
            f"SELECT id FROM foreign_languages WHERE teacher='{teacher}'"
        ).fetchall()
        return clear_result(ids)

    def get_id_group_by_id_teacher(self, id_teacher):
        ids = self.cur.execute(
            f"SELECT id FROM foreign_languages WHERE id_teacher='{id_teacher}'"
        ).fetchall()
        return clear_result(ids)


fl = ForeignLanguages()
print(fl.get_id_group_by_id_teacher(2))
