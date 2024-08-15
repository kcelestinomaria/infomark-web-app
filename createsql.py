import sqlite3

def initialize_database():
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
