import sqlite3
from datetime import datetime
import os

DB_PATH = 'data/reaction_game.db'

def init_db():
    os.makedirs('data', exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        created_at TEXT
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        started_at TEXT,
                        avg_reaction REAL,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS reactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER,
                        ufo_number INTEGER,
                        reaction_time REAL,
                        FOREIGN KEY(session_id) REFERENCES sessions(id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER,
                        score INTEGER,
                        FOREIGN KEY(session_id) REFERENCES sessions(id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS settings (
                        user_id INTEGER,
                        difficulty TEXT DEFAULT 'normal',
                        sound_on INTEGER DEFAULT 1,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

        conn.commit()

def get_or_create_user(name):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE name = ?", (name,))
        result = c.fetchone()
        if result:
            return result[0]
        else:
            created = datetime.now().isoformat()
            c.execute("INSERT INTO users (name, created_at) VALUES (?, ?)", (name, created))
            conn.commit()
            return c.lastrowid