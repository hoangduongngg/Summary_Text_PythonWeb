import pymysql


def connectDB():
    # Tân 
    # host = 'localhost'
    # dbName = 'TextSummary'
    # userName = 'root'
    # password = 'tan20011234'
    # conn = pymysql.connect(host=host, user=userName, password=password, database=dbName)
    # return conn

    # Dương 
    host = 'localhost'
    dbName = 'textsummarydb'
    userName = 'root'
    password = '123456789'
    conn = pymysql.connect(host=host, user=userName, password=password, database=dbName)
    return conn
