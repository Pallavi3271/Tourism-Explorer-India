from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.close()


# ================= ROUTES =================

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user, pwd)
            )
            conn.commit()
        except:
            conn.close()
            return "User already exists"

        conn.close()
        return redirect('/login')

    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        )
        data = cursor.fetchone()

        conn.close()

        if data:
            session['user'] = user
            return redirect('/destinations')
        else:
            return "Invalid Login"

    return render_template('login.html')


# Destinations Page
@app.route('/destinations')
def destinations():
    if 'user' in session:
        return render_template('destinations.html', user=session['user'])
    else:
        return redirect('/login')


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ================= RUN =================
if __name__ == '__main__':
    init_db()

    # 🔥 IMPORTANT for deployment (Render)
    app.run(host='0.0.0.0', port=10000)