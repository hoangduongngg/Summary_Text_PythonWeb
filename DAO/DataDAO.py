from DAO import DAO1
from Model.Data import Data


def getAllData():
    text = []
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('Select * from Data')
    for row in cursor.fetchall():
        text.append({"id": row[0], "content": row[1], "summary": row[2], "isTrained": row[3]})
    for i in text:
        print(i)


def insertData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('insert into Data (content, summary, isTrained) values (%s, %s, %s)',
                   (data.content, data.summary, data.istrained))
    conn.commit()
    conn.close()


def updateData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('update Data set content = %s, summary = %s, isTrained = %s where id = %s',
                   (data.content, data.summary, data.istrained, data.id))
    conn.commit()
    conn.close()
    print('update thành công')

def searchByID(id):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from Data where id = %s', id)
    result = cursor.fetchall()
    conn.close()
    if len(result) != 0:
        data = Data(0,' ', ' ', False)
        for res in result:
            data.id = res[0]
            data.content = res[1]
            data.summary = res[2]
            data.istrained = res[3]
        return data
    else:
        return None
    
def deleteData(id):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    test = cursor.execute('delete from Data where id = %s', id)
    conn.commit()
    conn.close()
    if test != 0:
        print('delete thanh cong')
        return True
    else: return False


def isDataExist(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from Data where content = %s and summary = %s limit 1', (data.content, data.summary))
    result = cursor.fetchall()
    conn.close()
    if len(result) != 0:
        data = Data(0, ' ', ' ', False)
        for res in result:
            data.id = res[0]
            data.content = res[1]
            data.summary = res[2]
            data.istrained = res[3]
        return data
    else:
        return 'data khong ton tai'


# def searchByID(id):
#     conn = DAO1.connectDB()
#     cursor = conn.cursor()
#     cursor.execute('select * from Data where id = %s', id)
#     data = Data(0, ' ', ' ', False)
#     for res in cursor.fetchall():
#         data.id = res[0]
#         data.content = res[1]
#         data.summary = res[2]
#         data.istrained = res[3]
#     conn.close()
#     return data


# data = Data(1, 'Hôm nay không đẹp trời 24', 'trời không đẹp', False)
# insertData(data)
# # updateData('Hôm nay không đẹp trời', 'trời không đẹp', 0, 2)
# deleteData(1)
#
# # data = Data()
# # data.content = 'Hôm nay không đẹp trời'
# # print(isDataExist(data))
# # searchByID(1)
# getAllData()
# # updateData(data)
# print(isDataExist(data))
