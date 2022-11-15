from flask import request, session, render_template, redirect, url_for

from DAO import UserDAO
from Model.User import User


def Login():
    message = None
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User(username, password)
        print(username + ' ' + password)
        print(user)
        if UserDAO.checkLogin(user):
            session['logged_in'] = True
            session['id'] = user.id
            session['username'] = user.username
            return redirect(url_for('server'))
        else:
            message = 'Sai thông tin đăng nhập'
    return render_template("/server/login.html", message=message)
