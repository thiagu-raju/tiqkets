from flask import Flask, render_template, request, redirect, url_for, session
import sqlalchemy
from sqlalchemy import create_engine
import re
import hashlib

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

db_connection_string = "mysql+pymysql://n4ugv3ja4obdcl3qrlz0:pscale_pw_O35f0Iq23vdSnbNNEfVNsJoaWzra101puQ8Aql92JgN@aws.connect.psdb.cloud:3306/tiqkets?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with engine.connect() as conn:
            result = conn.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, hashed_password))
            user = result.fetchone()
            print (user)

        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
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

            with engine.connect() as conn:
                result = conn.execute('SELECT * FROM user WHERE email = %s', (email,))
                account = result.fetchone()

                if account:
                    message = 'Account already exists!'
                else:
                    conn.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)', (userName, email, hashed_password))
                    conn.connection.commit()
                    message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)


if __name__ == "__main__":
    app.run(host ='0.0.0.0', debug=True)
