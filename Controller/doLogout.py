from flask import session, redirect, url_for


def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('Login'))
