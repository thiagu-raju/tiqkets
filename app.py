from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Replace these credentials with your own MySQL database credentials
db_credentials = {
    'host': 'thiaguraju.mysql.pythonanywhere-services.com',
    'user': 'thiaguraju',
    'password': 'Optimus@01',
    'database': 'thiaguraju$tiqkets',
}

# Route for the signup page
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Insert user details into the database
        insert_user(username, password, role)

        return "Signup Successful! You can now log in."
    
    return render_template('home.html')

# Function to insert user details into the database
def insert_user(username, password, role):
    try:
        connection = mysql.connector.connect(**db_credentials)
        cursor = connection.cursor()

        # SQL query to insert user details into the table
        query = "INSERT INTO tblUsers (user_name, password, role) VALUES (%s, %s, %s)"
        values = (username, password, role)
        cursor.execute(query, values)

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    app.run(host ='0.0.0.0', debug=True)
