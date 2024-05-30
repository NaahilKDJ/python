from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"
def get_db_connection():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        database="loginpython"
    )
    return mydb

@app.route('/')
def home():
    return render_template("base.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE username = %s', (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        # try:
        #     if user and check_password_hash(user[2], password):
        #         session['username'] = user[1]
        #     flash("Login OK", 'success')
        #     return redirect(url_for('home'))
        # except TypeError:
        #     print(type(user[2]))
        #     print(user)
        
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            flash("Login OK", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login failed", 'danger')
    
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO USERS (username,password) VALUES (%s,%s)', (username,hashed_password))
        conn.commit()
        conn.close()
        flash("Connexion OK",'success')
        return redirect(url_for('login'))
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)