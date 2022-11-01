from asyncio.windows_events import NULL
from email.mime import message
from flask import request, render_template 

from DAO import DataDAO
from Model.Data import Data

def AddData():
    data = None
    mess = None
    if request.method == 'POST':
        content = request.form["content"]
        summary = request.form["summary"]
        data = Data(content, summary, False)
        
        if DataDAO.isDataExist(data) == None:
            DataDAO.addData(data)
            mess = "success"
        else:
            mess = "fail"
        
    return render_template("/server/addData.html", data = data, mess = mess)
    
