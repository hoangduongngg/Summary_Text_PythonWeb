from flask import Flask, render_template, session, redirect, url_for

from Controller import doEditData, doAddData, doLogin, doLogout

app = Flask(__name__)
app.secret_key = 'Group2_PTHTTM'


@app.route('/')
def home():
    return render_template("/client/index.html")


@app.route('/server')
def server():
    if 'logged_in' in session:
        # User is loggedin show them the home page
        return render_template("/server/serverHome.html")
        # User is not loggedin redirect to login page
    return redirect(url_for('Login'))


@app.route('/addData', methods=['GET', 'POST'])
def addData():
    return doAddData.AddData()


@app.route('/editData', methods=['GET', 'POST'])
def editData():
    return doEditData.update()


@app.route('/deleteData')
def deleteData():
    return render_template("/server/deleteData.html")


@app.route('/versionManagement')
def versionManagement():
    return render_template("/server/versionManagement.html")


@app.route('/login', methods=['GET', 'POST'])
def Login():
    return doLogin.Login()


@app.route('/server/logout', methods=['GET', 'POST'])
def Logout():
    return doLogout.logout()


if __name__ == "__main__":
    app.run()
