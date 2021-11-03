from flask import Flask, render_template, request
import link_server

app = Flask(__name__)

USER = 'admin'
PSWRD = 'admin123'
flag = False


@app.route('/')
def engine():
    return render_template(
        'admin.html',
        flag=flag
    )


@app.route('/login/', methods=['POST'])
def log_in_function():
    user = request.form['user']
    pswrd = request.form['pass']
    if user == USER and pswrd == PSWRD:

        folders = link_server.get_all_folders()
        files = link_server.get_all_files()

        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            user=user,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )
    else:
        return render_template(
            'admin.html',
            flag=True
        )


@app.route('/action_with_dir/', methods=['POST'])
def action_with_dir():
    folders = link_server.get_all_folders()
    files = link_server.get_all_files()

    if request.form['action'] == 'create':
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=True,
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
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
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
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
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
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
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )
    elif request.form['action'] == 'back':
        folder_name = '../'
        link_server.open_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )


@app.route('/action_with_files/', methods=['POST'])
def action_with_files():
    folders = link_server.get_all_folders()
    files = link_server.get_all_files()

    if request.form['action'] == 'create':
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=True,
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )
    elif request.form['action'] == 'ok':
        file_name = request.form['file']
        link_server.add_file(file_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )
    elif request.form['action'] == 'open':
        file_name = request.form['file_names']
        # print(file_name)
        print(link_server.download_file(file_name))
        return render_template(
            'admin_panel.html',
            flag_not_root=True if link_server.cur_folder() != '/' else False,
            flag_create=False,
            user=USER,
            dirs=folders,
            path=link_server.cur_folder(),
            files=files
        )


app.run('127.0.0.1', 8080)
