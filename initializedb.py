import sqlite3

def initialize_database():
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create ProfilePictures table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProfilePictures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image BLOB,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    # Create SearchHistory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SearchHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        query TEXT,
        search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    # Create DataRequests table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DataRequests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data_type TEXT,
        symbol TEXT,
        indicator TEXT,
        currency_pair TEXT,
        start_date DATE,
        end_date DATE,
        provider TEXT,
        request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    # Create Favorites table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        symbol TEXT,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
