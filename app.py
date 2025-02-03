from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server address
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'note_app'  # Replace with your database name

# Initialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return "Passwords do not match", 400

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
                (username, email, password)
            )
            mysql.connection.commit()
        except Exception as e:
            logging.error(f"Error during signup: {e}")
            return f"An error occurred: {e}", 500
        finally:
            cur.close()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cur.execute(
                "SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s",
                (username_or_email, username_or_email, password)
            )
            user = cur.fetchone()
        finally:
            cur.close()

        if user:
            session['loggedin'] = True
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect username/email or password!", 401
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        note_title = request.form['note_title']
        note_content = request.form['note_content']
        cur.execute(
            "INSERT INTO notes(user_id, title, content) VALUES(%s, %s, %s)",
            (session['user']['id'], note_title, note_content)
        )
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    
    cur.execute("SELECT * FROM notes WHERE user_id = %s", (session['user']['id'],))
    notes = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', notes=notes, current_user=session['user'])

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
