from DAO import DAO1


def checkLogin(user):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from user where username = %s and password = %s limit 1', (user.username, user.password))
    result = cursor.fetchall()
    if len(result) != 0:
        for res in result:
            user.id = res[0]
            user.username = res[1]
            user.password = res[2]
        return True
    else:
        return False

