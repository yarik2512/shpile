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

        return render_template(
            'admin_panel.html',
            flag_create=False,
            user=user,
            dirs=folders
        )
    else:
        return render_template(
            'admin.html',
            flag=True
        )


@app.route('/action_with_dir/', methods=['POST'])
def action_with_dir():
    print(request.form['action'])
    folders = link_server.get_all_folders()

    if request.form['action'] == 'create':
        return render_template(
            'admin_panel.html',
            flag_create=True,
            user=USER,
            dirs=folders
        )
    elif request.form['action'] == 'ok':
        folder_name = request.form['folder']
        link_server.add_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_create=False,
            user=USER,
            dirs=folders
        )
    elif request.form['action'] == 'delete':
        folder_name = request.form['folder_names']
        print(folder_name)
        link_server.remove_folder(folder_name)
        folders = link_server.get_all_folders()
        return render_template(
            'admin_panel.html',
            flag_create=False,
            user=USER,
            dirs=folders
        )


app.run('127.0.0.1', 8080)
