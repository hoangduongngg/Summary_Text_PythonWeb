from flask import request, render_template

from DAO import DataDAO
from Model.Data import Data


def update():
    data1 = None
    message = None
    if request.method == 'GET':
        iD = request.args.get('id')
        print(iD)
        if iD is not None:
            if DataDAO.searchByID(iD) is not None:
                data1 = DataDAO.searchByID(iD)
                print(data1.id)
            else:
                message = 'Không tồn tại data với id: ' + str(iD)
    if request.method == 'POST':
        content = request.form["content"]
        summary = request.form["summary"]
        iD = request.args.get('id')
        print(content + ' ' + summary)
        data = Data(content, summary, False)
        data.id = iD
        print(data)
        if DataDAO.updateData(data):
            message = 'Update thành công!'
        else:
            message = 'Data bị trùng! Vui lòng chỉnh sửa lại thông tin'
    return render_template("/server/editData.html", data=data1, message=message)
