import mysql.connector

class DAO:
    def __init__(self):
        self.con=mysql.connector.connect(
            host="localhost",
            user="root",
            password="vinhcoi123",
            database="textsummaryDB",
            auth_plugin='mysql_native_password'
        )
