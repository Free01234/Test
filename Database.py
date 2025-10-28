import sqlite3
import os

DB_FILE = "plans.db"

def init_db():
    # Crée la base si elle n'existe pas
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            filename TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_plan(keyword, filename):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO plans (keyword, filename) VALUES (?, ?)", (keyword, filename))
    conn.commit()
    conn.close()

def get_plan(keyword):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT filename FROM plans WHERE keyword=?", (keyword,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
