from flask import Flask, render_template

from Controller import doEditData, doAddData

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("/client/index.html")


@app.route('/server')
def server():
    return render_template("/server/serverHome.html")


@app.route('/addData', methods=['GET', 'POST'])
def addData():
    mess = ""
    return doAddData.AddData(mess)


@app.route('/editData', methods=['GET', 'POST'])
def editData():
    return doEditData.update()


@app.route('/deleteData')
def deleteData():
    return render_template("/server/deleteData.html")


@app.route('/versionManagement')
def versionManagement():
    return render_template("/server/versionManagement.html")


if __name__ == "__main__":
    app.run()
