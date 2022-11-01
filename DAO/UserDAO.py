import DAO1
from Model.User import User


def checkLogin(user):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from user where username = %s and password = %s', (user.username, user.password))
    result = cursor.fetchall()
    if len(result) != 0:
        user = User('', '')
        for res in result:
            user.username = res[1]
            user.password = res[2]
        return user
    else:
        return None

