from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import link_server
import users

app = Flask(__name__)

USER = 'admin'
PSWRD = 'admin123'
user = ""
pswrd = ""
flag = False
rights = "t" if users.is_teacher(USER) else "s"


@app.route('/')
def engine():
    return render_template(
        'admin.html',
        rights=rights,
        flag=flag
    )


@app.route('/login/', methods=['POST'])
def log_in_function():
    global user, pswrd
    user = request.form['user']
    pswrd = request.form['pass']
    if user == USER and pswrd == PSWRD:

        folders = link_server.get_all_folders()
        files = link_server.get_all_files()

        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(USER),
            user=user,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    else:
        return render_template(
            'admin.html',
            rights=rights,
            flag=True
        )


@app.route('/action_with_dir/', methods=['POST'])
def action_with_dir():
    global user, pswrd
    folders = link_server.get_all_folders()
    files = link_server.get_all_files()

    if request.form['action'] == 'create':
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=True,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'ok':
        folder_name = request.form['folder']
        link_server.add_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'delete':
        folder_name = request.form['folder_names']
        print(folder_name)
        link_server.remove_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'open':
        print(request.form['folder_names'])
        folder_name = request.form['folder_names']
        link_server.open_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'back':
        folder_name = '../'
        link_server.open_folder(folder_name)
        folders = link_server.get_all_folders()
        files = link_server.get_all_files()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )


@app.route('/action_with_files/', methods=['POST'])
def action_with_files():
    global user, pswrd
    folders = link_server.get_all_folders()
    files = link_server.get_all_files()

    if request.form['action'] == 'create':
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=True,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'ok':
        file = request.files['file']
        link_server.add_file(file, secure_filename(file.filename))
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )
    elif request.form['action'] == 'open':
        file_name = request.form['file_names']
        print(file_name)
        link_server.download_file(file_name)
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            is_teacher=users.is_teacher(user),
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            rights=rights,
            files=files
        )


app.run('127.0.0.1', 8080)
