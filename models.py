import sqlite3
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

DB_PATH_KEY = 'DATABASE'

class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str, email: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email

    @staticmethod
    def get_by_username(conn: sqlite3.Connection, username: str) -> Optional['User']:
        cur = conn.cursor()
        cur.execute('SELECT id, username, password_hash, email FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2], email=row[3])
        return None

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, user_id: int) -> Optional['User']:
        cur = conn.cursor()
        cur.execute('SELECT id, username, password_hash, email FROM users WHERE id = ?', (user_id,))
        row = cur.fetchone()
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2], email=row[3])
        return None

    @staticmethod
    def create(conn: sqlite3.Connection, username: str, password: str, email: str) -> 'User':
        password_hash = generate_password_hash(password)
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', (username, password_hash, email))
        conn.commit()
        user_id = cur.lastrowid
        return User(id=user_id, username=username, password_hash=password_hash, email=email)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


def get_connection(app) -> sqlite3.Connection:
    db_path = app.config.get(DB_PATH_KEY, 'app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    conn = get_connection(app)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        '''
    )
    # Attempt to migrate existing DBs missing the email column
    try:
        cur.execute('SELECT email FROM users LIMIT 1')
    except sqlite3.OperationalError:
        cur.execute('ALTER TABLE users ADD COLUMN email TEXT')
        # Note: existing rows will have NULL email; enforce uniqueness later by updating data or recreating users.
    conn.commit()
    conn.close()
