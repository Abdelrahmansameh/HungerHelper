import { open } from 'sqlite';
import sqlite3 from 'sqlite3';
import { DB_PATH } from './database.js';
import { program } from 'commander';

program
  .option('--all', 'Plan for all quests')
  .option('--quests <list>', 'Comma separated quest slugs')
  .parse();

const opts = program.opts();

async function loadData() {
  const db = await open({ filename: DB_PATH, driver: sqlite3.Database });
  const quests = await db.all('SELECT id, slug, name, prerequisite_slug, location FROM quests');
  const objectives = await db.all('SELECT quest_id, required_item FROM quest_objectives');
  const items = await db.all('SELECT id, slug, name FROM items');
  const drops = await db.all('SELECT item_id, location, drop_rate FROM item_drops');
  await db.close();
  return { quests, objectives, items, drops };
}

function expandSet(selected, questMap) {
  const full = new Set();
  const stack = [...selected];
  while (stack.length) {
    const slug = stack.pop();
    if (full.has(slug)) continue;
    full.add(slug);
    const prereq = questMap.get(slug)?.prerequisite_slug;
    if (prereq) stack.push(prereq);
  }
  return full;
}

function aggregateItems(selectedIds, objectives) {
  const need = new Map();
  for (const obj of objectives) {
    if (selectedIds.has(obj.quest_id) && obj.required_item) {
      need.set(obj.required_item, (need.get(obj.required_item) || 0) + 1);
    }
  }
  return need;
}

function groupByLocation(needMap, items, drops) {
  const locMap = new Map();
  for (const [slug, qty] of needMap.entries()) {
    const item = items.find(i => i.slug === slug);
    if (!item) continue;
    const possible = drops.filter(d => d.item_id === item.id);
    if (!possible.length) continue;
    const best = possible.reduce((a, b) => (a.drop_rate > b.drop_rate ? a : b));
    const loc = best.location || 'unknown';
    if (!locMap.has(loc)) locMap.set(loc, { quests: [], items: [] });
    locMap.get(loc).items.push({ name: item.name, qty, chance: best.drop_rate });
  }
  return locMap;
}

(async () => {
  const { quests, objectives, items, drops } = await loadData();
  const questMap = new Map(quests.map(q => [q.slug, q]));
  const idMap = new Map(quests.map(q => [q.id, q]));
  let selectedSlugs;
  if (opts.all) selectedSlugs = quests.map(q => q.slug);
  else if (opts.quests) selectedSlugs = opts.quests.split(',').map(s => s.trim());
  else { console.error('Specify --all or --quests'); process.exit(1); }

  const fullSlugs = expandSet(selectedSlugs, questMap);
  const selectedIds = new Set([...fullSlugs].map(s => questMap.get(s).id));

  // add quests to location groups
  const locMap = new Map();
  for (const slug of fullSlugs) {
    const q = questMap.get(slug);
    const loc = q.location || 'unknown';
    if (!locMap.has(loc)) locMap.set(loc, { quests: [], items: [] });
    locMap.get(loc).quests.push(q.name);
  }

  const needed = aggregateItems(selectedIds, objectives);
  const itemGroups = groupByLocation(needed, items, drops);
  // merge item groups into locMap
  for (const [loc, data] of itemGroups.entries()) {
    if (!locMap.has(loc)) locMap.set(loc, { quests: [], items: [] });
    locMap.get(loc).items.push(...data.items);
  }

  const finalPlan = [];
  for (const [loc, data] of locMap.entries()) {
    if (!data.quests.length && !data.items.length) continue;
    finalPlan.push({ location: loc, quests: data.quests, items: data.items.map(i => `${i.name}×${i.qty} (${(i.chance*100).toFixed(1)}% drop)`) });
  }

  console.log(JSON.stringify(finalPlan, null, 2));
})();
