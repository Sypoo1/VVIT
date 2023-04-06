import requests
from flask import Flask, render_template, request
import psycopg2

from conf import Password

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
    user="postgres",
    password=Password,
    host="localhost",
    port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == '' or password == '':
        return render_template('account.html', error='Login and password must be not blank')

    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())

    if len(records) == 0:
        return render_template('account.html', error='Wrong login or password')

    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
