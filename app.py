from telnetlib import STATUS
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)

sql_Pass = "123456789"
sql_Schema = "textSummary"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:" + sql_Pass + "@localhost/" + sql_Schema + "charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


    



@app.route('/')
def home():
    return render_template("/client/index.html")

@app.route('/server')
def server():
    return render_template("/server/serverHome.html")

@app.route('/addData', methods = ["POST", "GET"])
def addData():
    if request.method == "POST":
        content = request.form["content"]
        summary = request.form["summary"]
        if content and summary:
            # flash("Add data success!")
            return redirect(url_for("server")) #test
        else:
            # flash("Data already exists!")
            return redirect(url_for("addData"))
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