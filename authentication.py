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

def create_role(role_name):
    """Create a new role."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO roles (role_name) VALUES (?)', (role_name,))
            conn.commit()
    except sqlite3.IntegrityError:
        print(f"Role '{role_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the role: {e}")

def assign_role_to_user(username, role_name):
    """Assign a role to a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                cursor.execute('SELECT id FROM roles WHERE role_name = ?', (role_name,))
                role = cursor.fetchone()
                if role:
                    role_id = role[0]
                    cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)', (user_id, role_id))
                    conn.commit()
                    print(f"Assigned role '{role_name}' to user '{username}'.")
                else:
                    print(f"Role '{role_name}' does not exist.")
            else:
                print(f"User '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred while assigning the role: {e}")

# User Roles - Role Management
def create_role(role_name):
    """Create a new role."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO roles (role_name) VALUES (?)', (role_name,))
            conn.commit()
    except sqlite3.IntegrityError:
        print(f"Role '{role_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the role: {e}")

def assign_role_to_user(username, role_name):
    """Assign a role to a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                cursor.execute('SELECT id FROM roles WHERE role_name = ?', (role_name,))
                role = cursor.fetchone()
                if role:
                    role_id = role[0]
                    cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)', (user_id, role_id))
                    conn.commit()
                    print(f"Assigned role '{role_name}' to user '{username}'.")
                else:
                    print(f"Role '{role_name}' does not exist.")
            else:
                print(f"User '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred while assigning the role: {e}")

def get_user_roles(username):
    """Get all roles for a given user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.role_name 
                FROM roles r 
                JOIN user_roles ur ON r.id = ur.role_id 
                JOIN users u ON u.id = ur.user_id 
                WHERE u.username = ?
            ''', (username,))
            roles = cursor.fetchall()
            return [role[0] for role in roles]
    except Exception as e:
        print(f"An error occurred while retrieving user roles: {e}")
        return []

def initiate_password_reset(username):
    """Generate a password reset token for the user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                user_id = user[0]
                reset_token = str(uuid.uuid4())
                expiration = datetime.now() + timedelta(hours=1)
                cursor.execute('INSERT INTO password_resets (user_id, reset_token, expiration) VALUES (?, ?, ?)',
                               (user_id, reset_token, expiration))
                conn.commit()
                return reset_token
            return None
    except Exception as e:
        print(f"An error occurred while initiating password reset: {e}")
        return None

def reset_password(reset_token, new_password):
    """Reset the user's password using the reset token."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id FROM password_resets WHERE reset_token = ? AND expiration > ?', 
                           (reset_token, datetime.now()))
            reset = cursor.fetchone()
            if reset:
                user_id = reset[0]
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
                cursor.execute('DELETE FROM password_resets WHERE reset_token = ?', (reset_token,))
                conn.commit()
                return True
            return False
    except Exception as e:
        print(f"An error occurred while resetting the password: {e}")
        return False


def log_user_action(user_id, action):
    """Log user actions for auditing purposes."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO logs (user_id, action) VALUES (?, ?)', (user_id, action))
            conn.commit()
    except Exception as e:
        print(f"An error occurred while logging user action: {e}")

def update_user_credentials(current_username, new_username=None, new_password=None, profile_pic_path=None):
    try:
        conn = sqlite3.connect('app_database.db')
        cursor = conn.cursor()

        if new_username and new_password and profile_pic_path:
            cursor.execute("UPDATE users SET username=?, password=?, profile_pic=? WHERE username=?", (new_username, new_password, profile_pic_path, current_username))
        elif new_username and new_password:
            cursor.execute("UPDATE users SET username=?, password=? WHERE username=?", (new_username, new_password, current_username))
        elif new_username:
            cursor.execute("UPDATE users SET username=? WHERE username=?", (new_username, current_username))
        elif new_password:
            cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, current_username))
        elif profile_pic_path:
            cursor.execute("UPDATE users SET profile_pic=? WHERE username=?", (profile_pic_path, current_username))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating credentials: {e}")
        return False
