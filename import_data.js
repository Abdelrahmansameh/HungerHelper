import fetch from 'node-fetch';
import cheerio from 'cheerio';
import { initDb, DB_PATH } from './database.js';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import { fileURLToPath } from 'url';

const BASE = 'https://hunger-companion.com';
const HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36' };

async function fetchHTML(p) {
  const res = await fetch(`${BASE}${p}`, { headers: HEADERS });
  if (!res.ok) throw new Error(`Failed ${p}: ${res.status}`);
  return await res.text();
}

async function parseQuestTree() {
  const html = await fetchHTML('/quests/tree');
  const $ = cheerio.load(html);
  const quests = [];
  $('a[data-quest]').each((_, el) => {
    const $el = $(el);
    const slug = $el.attr('data-quest');
    const after = $el.attr('data-after') || null;
    const name = slug;
    quests.push({ slug, after, name });
  });
  return quests;
}

async function storeQuests(db, quests) {
  const stmt = await db.prepare('INSERT OR IGNORE INTO quests (slug, name, prerequisite_slug) VALUES (?,?,?)');
  for (const q of quests) {
    await stmt.run(q.slug, q.name, q.after);
  }
  await stmt.finalize();
}

async function fetchAndStoreObjectives(db) {
  const rows = await db.all('SELECT id, slug FROM quests');
  const stmt = await db.prepare('INSERT OR IGNORE INTO quest_objectives (quest_id, obj_id, description, required_item) VALUES (?,?,?,?)');
  for (const { id: questId, slug } of rows) {
    const html = await fetchHTML(`/quests/${slug}`);
    const $ = cheerio.load(html);
    $('li[class*="obj"]').each((_, li) => {
      const $li = $(li);
      const objId = $li.attr('data-obj-id') || $li.attr('data-obj') || null;
      const desc = $li.text().trim();
      const link = $li.find('a[href*="/items/"]');
      const reqItem = link.length ? link.attr('href').split('/').pop() : null;
      stmt.run(questId, objId, desc, reqItem);
    });
  }
  await stmt.finalize();
}

async function fetchAndStoreItems(db) {
  const rows = await db.all('SELECT DISTINCT required_item FROM quest_objectives WHERE required_item IS NOT NULL');
  const stmtItem = await db.prepare('INSERT OR IGNORE INTO items (slug, name, type, rarity) VALUES (?,?,?,?)');
  const stmtDrop = await db.prepare('INSERT INTO item_drops (item_id, location, drop_rate, source) VALUES (?,?,?,?)');
  for (const r of rows) {
    const slug = r.required_item;
    try {
      const res = await fetch(`${BASE}/api/item-card/`, { headers: HEADERS, method: 'GET', timeout: 15000 });
      if (!res.ok) continue;
      const data = await res.json();
      const { slug: itemSlug, name, type, rarity, drops = [] } = data;
      await stmtItem.run(itemSlug, name, type, rarity);
      const itemRow = await db.get('SELECT id FROM items WHERE slug = ?', itemSlug);
      for (const dr of drops) {
        await stmtDrop.run(itemRow.id, dr.location, dr.chance, dr.source);
      }
    } catch (e) {
      console.warn('Item fetch error for', slug, e.message);
    }
  }
  await stmtItem.finalize();
  await stmtDrop.finalize();
}

(async () => {
  console.log('Initializing DB…');
  await initDb();
  const db = await open({ filename: DB_PATH, driver: sqlite3.Database });

  console.log('Downloading quest tree…');
  const tree = await parseQuestTree();
  console.log(`Found ${tree.length} quests`);
  await storeQuests(db, tree);

  console.log('Fetching objectives…');
  await fetchAndStoreObjectives(db);

  console.log('Fetching items…');
  await fetchAndStoreItems(db);

  await db.close();
  console.log('Import complete.');
})();
