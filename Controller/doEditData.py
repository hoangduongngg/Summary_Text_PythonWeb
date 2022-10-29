from flask import request, render_template

from DAO import DataDAO
from Model.Data import Data

def update():
    data1 = None
    if request.method == 'GET':
        iD = request.args.get('id')
        print(iD)
        if iD is not None:
            data1 = DataDAO.searchByID(iD)
            print(data1.id)
    if request.method == 'POST':
        content = request.form["content"]
        summary = request.form["summary"]
        iD = request.args.get('id')
        print(content+' '+summary)
        data = Data(iD, content, summary, False)
        print(data)
        DataDAO.updateData(data)
    return render_template("/server/editData.html", data=data1)
