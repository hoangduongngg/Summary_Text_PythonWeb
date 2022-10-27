from flask import Flask, render_template

from Controller import doEditData

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("/client/index.html")


@app.route('/server')
def server():
    return render_template("/server/serverHome.html")


@app.route('/addData')
def addData():
    return render_template("/server/addData.html")


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
