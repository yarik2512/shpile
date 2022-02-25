import os
from ftplib import FTP

ftp = FTP('server90.hosting.reg.ru', 'u1490660', passwd='Ds3Nb2d5wYj6UW28')
ftp.login(user='u1490660', passwd='Ds3Nb2d5wYj6UW28')


def add_folder(folder_name):
    ftp.mkd(folder_name)


def add_folder_to_path(path, folder_name):
    try:
        ftp.cwd(path)
        ftp.mkd(folder_name)
    except:
        pass


def remove_folder(folder_name):
    ftp.rmd(folder_name)


def get_all_folders():
    return list(filter(lambda x: not ('.' in x), ftp.nlst()))


def open_folder(folder_name):
    ftp.cwd('./' + folder_name)


def cur_folder():
    return ftp.pwd()


def get_file_size(file_name):
    return ftp.sendcmd(f'SIZE {file_name}')


def get_all_files():
    return list(filter(lambda x: '.' in x and not (x[0] == '.'), ftp.nlst()))


def add_file(file, filename):
    ftp.storbinary(f'STOR {filename}', file)


def download_file(file_name):
    print(os.getcwd())

    with open(f'./{file_name}', 'wb+') as file:
        ftp.retrbinary(f'RETR {file_name}', file.write)
        file.close()
    # print(file.read())

    return file
