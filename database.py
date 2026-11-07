import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'hunger_helper.db')

def get_connection():
    # Increase timeout to wait for locked database and enable WAL for better concurrency
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Create tables
    cur.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        name TEXT,
        giver TEXT,
        prerequisite_slug TEXT,
        location TEXT,
        reward_item TEXT,
        reward_quantity INTEGER
    );

    CREATE TABLE IF NOT EXISTS quest_objectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quest_id INTEGER NOT NULL REFERENCES quests(id) ON DELETE CASCADE,
        obj_id TEXT NOT NULL,
        description TEXT,
        required_item TEXT,
        UNIQUE(quest_id, obj_id)
    );

    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        name TEXT,
        type TEXT,
        rarity TEXT
    );

    CREATE TABLE IF NOT EXISTS item_drops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
        location TEXT,
        drop_rate REAL,
        source TEXT
    );

    CREATE TABLE IF NOT EXISTS maps (
        name TEXT PRIMARY KEY,
        region TEXT,
        raid_type TEXT
    );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f'Database initialized at {DB_PATH}')
