import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            user_id TEXT,
            username TEXT,
            utm TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_activation(user_id, username, utm):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO activations (datetime, user_id, username, utm)
        VALUES (?, ?, ?, ?)
    ''', (now, str(user_id), username, utm))
    conn.commit()
    conn.close()

def get_activations():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT datetime, user_id, username, utm FROM activations ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    return rows
