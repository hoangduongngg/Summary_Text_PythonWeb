from flask import Flask, render_template, session, redirect, url_for

from Controller import doEditData, AddDataController, doLogin, doLogout

app = Flask(__name__)
app.secret_key = 'Group2_PTHTTM'


@app.route('/')
def home():
    return render_template("/client/index.html")


@app.route('/server')
def server():
    if 'logged_in' in session:
        return render_template("/server/serverHome.html")
    return redirect(url_for('Login'))


@app.route('/addData', methods=['GET', 'POST'])
def addData():
    if 'logged_in' not in session:
        return redirect(url_for('Login'))
    return AddDataController.AddDataController()


@app.route('/editData', methods=['GET', 'POST'])
def editData():
    if 'logged_in' not in session:
        return redirect(url_for('Login'))
    return doEditData.update()


@app.route('/deleteData')
def deleteData():
    if 'logged_in' not in session:
        return redirect(url_for('Login'))
    return render_template("/server/deleteData.html")


@app.route('/versionManagement')
def versionManagement():
    if 'logged_in' not in session:
        return redirect(url_for('Login'))
    return render_template("/server/versionManagement.html")

@app.route('/reTrain')
def reTrain():
    return render_template("/server/reTrain.html")

@app.route('/login', methods=['GET', 'POST'])
def Login():
    return doLogin.Login()


@app.route('/server/logout', methods=['GET', 'POST'])
def Logout():
    return doLogout.logout()


if __name__ == "__main__":
    app.run(debug=True)
