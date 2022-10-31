import pymysql


def connectDB():
    host = 'localhost'
    dbName = 'TextSummary'
    userName = 'root'
    password = 'dat19022001'
    conn = pymysql.connect(host=host, user=userName, password=password, database=dbName)
    return conn
