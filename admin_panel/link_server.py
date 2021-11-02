from ftplib import FTP

ftp = FTP('server90.hosting.reg.ru', 'u1490660', passwd='Ds3Nb2d5wYj6UW28')
ftp.login(user='u1490660', passwd='Ds3Nb2d5wYj6UW28')


def add_folder(folder_name):
    ftp.mkd(folder_name)


def remove_folder(folder_name):
    ftp.rmd(folder_name)


def get_all_folders():
    return list(filter(lambda x: not ('.' in x), ftp.nlst()))


def open_folder(folder):
    ftp.cwd('./'+folder)


def cur_folder():
    return ftp.pwd()
