from flask import request, render_template

from DAO import DataDAO

def delete():
  data1 = None
  mess = None
  if request.method == 'GET':
    iD = request.args.get('id')
    print (iD)
    if iD is not None:
      if DataDAO.searchByID(iD) is not None:
        data1 = DataDAO.searchByID(iD)
        print (data1)
      else:
        mess = "Không tìm thấy data với id:" + str(iD)
        print (mess)
  if request.method == 'POST':
    iD = request.args.get('id')
    print(iD)
    if DataDAO.deleteData(iD) is True:
      mess = "Đã Xoá Thành công"
    else:
      mess = "Xoá Thất bại"
  return render_template("/server/deleteData.html", data=data1, mess= mess) 