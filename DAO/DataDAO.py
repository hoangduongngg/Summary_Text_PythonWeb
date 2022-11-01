from DAO import DAO1
from Model.Data import Data


def getAllData():
    text = []
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('Select * from tblData')
    for row in cursor.fetchall():
        text.append({"id": row[0], "content": row[1], "summary": row[2], "isTrained": row[3]})
    for i in text:
        print(i)


def insertData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('insert into tblData (content, summary, isTrained) values (%s, %s, %s)',
                   (data.content, data.summary, data.istrained))
    conn.commit()
    conn.close()


def updateData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    if isDataExist(data) is None:
        cursor.execute('update tblData set content = %s, summary = %s, isTrained = %s where id = %s',
                       (data.content, data.summary, data.istrained, data.id))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def deleteData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('delete from tblData where id = %s', data.id)
    conn.commit()
    conn.close()


def isDataExist(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from tblData where content = %s and summary = %s limit 1', (data.content, data.summary))
    result = cursor.fetchall()
    conn.close()
    if len(result) != 0:
        data = Data(' ', ' ', False)
        for res in result:
            data.id = res[0]
            data.content = res[1]
            data.summary = res[2]
            data.istrained = res[3]
        return data
    else:
        return None


def searchByID(id):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from tblData where id = %s', id)
    result = cursor.fetchall()
    conn.close()
    if len(result) != 0:
        data = Data(' ', ' ', False)
        for res in result:
            data.id = res[0]
            data.content = res[1]
            data.summary = res[2]
            data.istrained = res[3]
        return data
    else:
        return None

# data = Data(1, 'Hôm nay không đẹp trời', 'trời không đẹp', False)
# # insertData(data)
# # updateData('Hôm nay không đẹp trời', 'trời không đẹp', 0, 2)
# # deleteData(1)
#
# # data = Data()
# # data.content = 'Hôm nay không đẹp trời'
# # print(isDataExist(data))
# # searchByID(1)
# # getAllData()
# # updateData(data)
# print(isDataExist(data))
