import pymysql


def connectDB():
    host = 'localhost'
    dbName = 'TextSummarydb'
    userName = 'root'
    password = ''
    conn = pymysql.connect(host=host, user=userName, password=password, database=dbName)
    return conn
