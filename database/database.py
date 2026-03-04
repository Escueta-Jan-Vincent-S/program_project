import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pos.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'student',
            is_current INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO accounts (email, role, is_current)
        VALUES ('admin@gmail.com', 'admin', 1)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO accounts (email, role, is_current)
        VALUES ('student@gmail.com', 'student', 0)
    """)

    conn.commit()
    conn.close()

def get_all_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role, is_current FROM accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def switch_account(account_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET is_current = 0")
    cursor.execute("UPDATE accounts SET is_current = 1 WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()