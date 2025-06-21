import sqlite3
from datetime import datetime

DB_PATH = "users.db"

def create_chat_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS active_users (
                    username TEXT PRIMARY KEY
                )''')
    conn.commit()
    conn.close()

def add_message(sender, receiver, role, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messages (sender, receiver, role, message, timestamp) VALUES (?, ?, ?, ?, ?)",
              (sender, receiver, role, message, timestamp))
    conn.commit()
    conn.close()

def get_messages_between(sender, receiver):
    if not sender or not receiver:
        return []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT sender, role, message, timestamp FROM messages
        WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
        ORDER BY id ASC
    ''', (sender, receiver, receiver, sender))
    results = c.fetchall()
    conn.close()
    return results

def mark_user_active(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO active_users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def remove_user_active(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM active_users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_active_users(current_user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM active_users WHERE username != ?", (current_user,))
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users
