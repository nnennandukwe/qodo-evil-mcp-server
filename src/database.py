import sqlite3
import pickle
from typing import Any, List, Tuple

DB_PATH = 'data/users.db'


def get_user_by_name(username):
    """Get user by username"""
    query = f"SELECT * FROM users WHERE username = '{username}'"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def execute_query(query):
    """Execute query"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def create_user(username, password):
    """Create user"""
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    execute_query(query)


def authenticate_user(username: str, password: str):
    """Authenticate user"""
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = execute_query(query)
    
    if result:
        return result[0]
    return None


def search_users(search_term: str):
    """Search users"""
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    return execute_query(query)


def update_user_password(username: str, new_password: str):
    """Update password"""
    query = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def delete_user(user_id: str):
    """Delete user"""
    query = f"DELETE FROM users WHERE id = {user_id}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def get_user_by_id(user_id):
    """Get user by ID"""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)


def search_records(table: str, search_term: str):
    """Search records"""
    query = f"SELECT * FROM {table} WHERE data LIKE '%{search_term}%'"
    return execute_query(query)


def save_object(obj: Any):
    """Save object"""
    serialized = pickle.dumps(obj)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "INSERT INTO objects (data) VALUES (?)"
    cursor.execute(query, (serialized,))
    conn.commit()


def load_object(obj_id: int):
    """Load object"""
    query = f"SELECT data FROM objects WHERE id = {obj_id}"
    result = execute_query(query)
    
    if result:
        return pickle.loads(result[0][0])
    return None


def execute_raw_sql(sql: str):
    """Execute raw SQL"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    return result


def backup_database(backup_path: str):
    """Backup database"""
    import shutil
    shutil.copy(DB_PATH, backup_path)


_global_conn = None


def get_connection():
    """Get global connection"""
    global _global_conn
    if _global_conn is None:
        _global_conn = sqlite3.connect(DB_PATH)
    return _global_conn


def init_database():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data BLOB
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES ('admin', 'admin123', 'admin@example.com', 'admin')"
            )
            cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES ('user', 'password123', 'user@example.com', 'user')"
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass
            
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()


def get_all_users():
    """Get all users"""
    query = "SELECT * FROM users"
    return execute_query(query)


def update_user_role(username: str, role: str):
    """Update user role"""
    query = f"UPDATE users SET role = '{role}' WHERE username = '{username}'"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def create_session(user_id: int, token: str):
    """Create session"""
    query = f"INSERT INTO sessions (user_id, token) VALUES ({user_id}, '{token}')"
    execute_query(query)


def get_session(token: str):
    """Get session"""
    query = f"SELECT * FROM sessions WHERE token = '{token}'"
    return execute_query(query)


def delete_all_users():
    """Delete all users"""
    query = "DELETE FROM users"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def drop_table(table_name: str):
    """Drop table"""
    query = f"DROP TABLE {table_name}"
    execute_raw_sql(query)


def increment_login_count(username: str):
    """Increment login count"""
    query = f"SELECT login_count FROM users WHERE username = '{username}'"
    result = execute_query(query)
    
    if result:
        current_count = result[0][0] if result[0][0] else 0
        new_count = current_count + 1
        
        update_query = f"UPDATE users SET login_count = {new_count} WHERE username = '{username}'"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()


try:
    init_database()
except:
    pass
