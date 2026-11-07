import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export const DB_PATH = path.join(__dirname, 'hunger_helper.db');

export async function initDb() {
  const db = await open({ filename: DB_PATH, driver: sqlite3.Database });
  await db.exec(`PRAGMA foreign_keys = ON;
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
    );`);
  await db.close();
}

if (import.meta.url === `file://${__filename}`) {
  // allow running directly to init db
  (async () => {
    await initDb();
    console.log('Database created at', DB_PATH);
  })();
}
