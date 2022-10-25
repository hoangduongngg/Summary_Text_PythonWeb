from flask import Flask, redirect, url_for, render_template

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

@app.route('/editData')
def editData():
    return render_template("/server/editData.html")

@app.route('/deleteData')
def deleteData():
    return render_template("/server/deleteData.html")

@app.route('/versionManagement')
def versionManagement():
    return render_template("/server/versionManagement.html")

if __name__ == "__main__":
    app.run()