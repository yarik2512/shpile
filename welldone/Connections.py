from mysql.connector import connect
from ftplib import FTP


def getConnectionDB():
    con = connect(
        host='37.140.192.174',
        database='u1490660_default',
        user='u1490660_default',
        password='Ds3Nb2d5wYj6UW28'
    )
    return con.cursor()


def getFTP():
    ftp = FTP('server90.hosting.reg.ru', 'u1490660', passwd='Ds3Nb2d5wYj6UW28')
    ftp.login(user='u1490660', passwd='Ds3Nb2d5wYj6UW28')
    return ftp

