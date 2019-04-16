# -*- coding: utf-8 -*-


from flask import Flask, request, session, redirect, render_template, Response
import datetime
from flask_httpauth import HTTPBasicAuth
from dicttoxml import dicttoxml

sess_workaround = None

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
auth = HTTPBasicAuth()

user_name = "TRAIN"
pass_wd = "TuN3L"


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None



@app.route('/', methods=['GET'])
def index():
    return 'Main page'


@app.route('/logout', methods=['POST'])
def logout():
    auth = request.authorization
    if 'logged' not in session:
        print('Not logged yet')
        return redirect('/login')
    else:
        print(auth.password, auth.username)
        session.pop('logged', None)
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if 'logged' not in session:
        print('IF 1')
        if auth.username == user_name and auth.password == pass_wd:
            print('IF 2')
            session['logged'] = True
            return redirect('/hello')
        else:
            print("ELSE 2")
            return "Please provide appropriate credentials", 401
    else:
        print('ELSE 2', session.keys())
        return redirect('/hello')





if __name__ == '__main__':
    app.secret_key = 'super secret key'

    app.run(debug=True)
