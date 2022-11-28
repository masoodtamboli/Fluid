from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = "fluid_mech"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "Fluid Logins"

mysql = MySQL(app)

@app.route('/')
@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == 'POST':
        username = request.args.get("username")
        password = request.args.get("password")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = % s AND password = % s", (username, password, ))
        account = cursor.fetchone()

        if account:
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            return {
                "status": 200,
                "message": "Loggen in Successfully"
            }
        else:
            return{
                "status": 0,
                "message": "Incorrect username or password"
            }
    else:
        return {
            "status":0,
            "message":"Server Error!"
        }

@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return {
        "status": 200,
        "message": "Logged Out!"
    }

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return {
                "status": 200,
                "message": msg,
                }
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return {
            "status": 0,
            "message": msg,
            }   
    



if __name__ == "__main__":
    app.run(debug = True)
