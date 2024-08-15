import sqlite3
import bcrypt

DB_PATH = 'app_database.db'

def create_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def register_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                           (username, email, hashed_password))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"An error occurred while registering the user: {e}")
        return False

def authenticate_user(username, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
                return True
            else:
                return False
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return False
