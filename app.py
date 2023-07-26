from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

db_connection_config = {
    "user": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "ssl_ca": "/etc/ssl/cert.pem",
    "connection_timeout": 60  # Increase the timeout to 60 seconds (adjust as needed)
}


conn = mysql.connector.connect(**db_connection_config)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, hashed_password))
        user = cursor.fetchone()

        cursor.close()

        if user:
            session['loggedin'] = True
            session['userid'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            message = 'Logged in successfully!'
            return render_template('user.html', message=message)
        else:
            message = 'Please enter correct email/password!'
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
            account = cursor.fetchone()

            if account:
                message = 'Account already exists!'
            else:
                cursor.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)', (userName, email, hashed_password))
                conn.commit()
                cursor.close()
                message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)

if __name__ == "__main__":
    app.run(host ='127.0.0.1', debug=True)