from asyncio.windows_events import NULL
from DAO import DAO1
from Model.Data import Data


def getAllData():
    text = []
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    # cursor.execute('Select * from Data')
    cursor.execute('Select * from Data limit 100') 
    for row in cursor.fetchall():
        text.append({"id": row[0], "content": row[1], "summary": row[2], "isTrained": row[3]})
    for i in text:
        print(i)


def addData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('insert into tbldata (content, summary, isTrained) values (%s, %s, %s)',
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


def deleteData(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('delete from Data where id = %s', data.id)
    conn.commit()
    conn.close()


def isDataExist(data):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from tbldata where content = %s and summary = %s limit 1', (data.content, data.summary))
    result = cursor.fetchall()
    conn.close()
    if len(result) != 0:
        # data = Data(0, ' ', ' ', False) 
        # Dương: sửa hàm init, chỉ cần khởi tạo 3 giá trị
        data = Data(' ', ' ', False)
        for res in result:
            data.id = res[0]
            data.content = res[1]
            data.summary = res[2]
            data.istrained = res[3]
        return data
    else:
        # return 'data khong ton tai'
        return NULL


def searchByID(id):
    conn = DAO1.connectDB()
    cursor = conn.cursor()
    cursor.execute('select * from Data where id = %s', id)
    data = Data(0, ' ', ' ', False) 
    # Dương: sửa hàm init, chỉ cần khởi tạo 3 giá trị
    # data = Data(' ', ' ', False)
    for res in cursor.fetchall():
        data.id = res[0]
        data.content = res[1]
        data.summary = res[2]
        data.istrained = res[3]
    conn.close()
    return data


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
