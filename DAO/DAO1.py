import pymysql


def connectDB():
    host = 'localhost'
    dbName = 'TextSummary'
    userName = 'root'
    password = 'tan20011234'
    conn = pymysql.connect(host=host, user=userName, password=password, database=dbName)
    return conn
