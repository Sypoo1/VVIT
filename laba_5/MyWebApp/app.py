import requests
from flask import Flask, render_template, request, redirect
import psycopg2

from conf import Password

app = Flask(__name__)

conn = psycopg2.connect(database="service_db", user="postgres",
                        password=Password, host="localhost", port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get('username')
            password = request.form.get('password')

            if username == '' or password == '':
                return render_template('account.html', error='Login and password must be not blank')

            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if len(records) == 0:
                return render_template('account.html', error='Wrong login or password')

            return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
        elif request.form.get('registration'):
            return redirect('/registration/')
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':

        reg_name = request.form.get('name')
        reg_login = request.form.get('login')
        reg_password = request.form.get('password')

        if '' in [reg_name, reg_login, reg_password]:
            return render_template('registration.html', error='Name, Login and password must be not blank')

        check_name = reg_name.lower()
        for item in 'a bcdefghijklmnopqrstuvwxyz':
            check_name = check_name.replace(item, '')
        if len(check_name) > 0:
            return render_template('registration.html',
                                   error='A name can only consist of letters and spaces')

        flag = True
        try:
            a = int(reg_login)
        except ValueError:
            flag = False
        if flag:
            return render_template('registration.html', error='Login can not be number')

        check_login = reg_login.lower()
        for item in 'abcdefghijklmnopqrstuvwxyz0123456789':
            check_login = check_login.replace(item, '')
        if len(check_login) > 0:
            return render_template('registration.html',
                                   error='Login can not consist only of numbers'
                                         ' and can not contain special characters and spaces')

        if ' ' in reg_password:
            return render_template('registration.html',
                                   error='Password can not contain spaces')

        cursor.execute(f"SELECT * FROM service.users WHERE login='{reg_login}';")
        check_login_2 = list(cursor.fetchall())
        if len(check_login_2) != 0:
            return render_template('registration.html', error='This login is already in use. Please enter a new login')

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',
                       (str(reg_name), str(reg_login), str(reg_password)))
        conn.commit()
        return redirect('/login/')

    return render_template('registration.html')
