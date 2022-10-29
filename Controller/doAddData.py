from asyncio.windows_events import NULL
from flask import request, render_template

from DAO import DataDAO
from Model.Data import Data

def AddData():
    # if request.method == 'GET':
    #     return render_template("/server/addData.html")
    if request.method == 'POST':
        content = request.form["content"]
        summary = request.form["summary"]
        print(content+' '+summary)
        data = Data(content, summary, False)
        if DataDAO.isDataExist(data) == NULL:
            DataDAO.addData(data)
            print("Thanh cong")
            return render_template("/server/serverHome.html")
        else:
            print("Data da ton tai")
        
    return render_template("/server/addData.html")
    