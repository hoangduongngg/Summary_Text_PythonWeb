from flask import request, render_template

from DAO import DataDAO

def delete():
  data1 = None
  if request.method == 'GET':
    iD = request.args.get('id')
    print (iD)
    if iD is not None:
      data1 = DataDAO.searchByID(iD)
      print (data1)
  if request.method == 'POST':
    iD = request.args.get('id')
    print(iD)
    DataDAO.deleteData(iD)
  return render_template("/server/deleteData.html", data=data1) 