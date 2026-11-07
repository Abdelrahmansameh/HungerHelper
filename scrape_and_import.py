"""Scraper and database importer for HUNGER Companion (hunger-companion.com).

Extracts:
1. Full quest tree & prerequisites.
2. Quests, givers, locations, and objectives.
3. Item metadata (names, types, rarities).
4. Raid maps, loot drop locations, and odds.
Populates SQLite database 'hunger_helper.db'.
"""

import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from database import get_connection, init_db

BASE_URL = 'https://hunger-companion.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

def load_prerequisites():
    """Load quest prerequisite mapping from tree_quests_parsed.json if present."""
    prereqs = {}
    json_path = os.path.join(os.path.dirname(__file__), 'tree_quests_parsed.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            tree = json.load(f)
            for item in tree:
                prereqs[item['slug']] = item.get('after')
    return prereqs

def run_import():
    print("1. Initializing database schema...")
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    prereqs = load_prerequisites()
    slugs = list(prereqs.keys())
    print(f"Loaded {len(slugs)} quests from tree definition.")

    print("2. Fetching comprehensive tracker data from hunger-companion.com...")
    session = requests.Session()
    session.headers.update(HEADERS)

    resp = session.get(f"{BASE_URL}/api/tracker", params={'slugs': ','.join(slugs)}, timeout=30)
    resp.raise_for_status()
    tracker_data = resp.json()

    api_quests = tracker_data.get('quests', [])
    api_maps = tracker_data.get('maps', [])
    api_points = tracker_data.get('points', [])
    print(f"Retrieved {len(api_quests)} quests, {len(api_maps)} maps, and {len(api_points)} points.")

    # 3. Store Maps
    map_lookup = {}
    for m in api_maps:
        map_lookup[m['id']] = m['name']
        cur.execute(
            "INSERT OR REPLACE INTO maps (name, region, raid_type) VALUES (?, ?, ?)",
            (m['name'], 'Mainland', 'Raid Map')
        )
    cur.execute(
        "INSERT OR REPLACE INTO maps (name, region, raid_type) VALUES (?, ?, ?)",
        ('Château (Hub)', 'Outer Ramparts', 'Safe Zone')
    )
    conn.commit()

    # 4. Map quest locations & parse loot drops
    # Match pattern: e.g. "Flour · 1/2.1 (Flour Sack)"
    pattern = re.compile(r'^(.*?)\s*[\xb7\u00b7·]\s*1/([\d.]+)\s*\((.*?)\)')

    quest_locations = {}
    loot_drop_defs = {}

    for p in api_points:
        q_slug = p.get('quest')
        m_id = p.get('map_id')
        m_name = map_lookup.get(m_id, 'Unknown Map')

        if q_slug and m_id:
            quest_locations.setdefault(q_slug, set()).add(m_name)

        if p.get('type') == 'loot':
            title = p.get('title', '')
            match = pattern.search(title)
            if match:
                raw_item_name = match.group(1).strip()
                odds = float(match.group(2))
                drop_rate = round(1.0 / odds, 4) if odds > 0 else 0.0
                source = match.group(3).strip()
                key = (raw_item_name.lower(), m_name, source)
                loot_drop_defs[key] = {
                    'name': raw_item_name,
                    'location': m_name,
                    'drop_rate': drop_rate,
                    'source': source,
                    'okey': p.get('okey')
                }

    print(f"Parsed {len(loot_drop_defs)} unique item drop sources across raid maps.")

    # 5. Store Quests & Objectives
    items_to_create = {}
    quest_id_map = {}

    for q in api_quests:
        slug = q['slug']
        name = q.get('title', slug)
        giver = q.get('npc_name')
        prereq = prereqs.get(slug)

        locs = quest_locations.get(slug, set())
        if not locs:
            location = 'Château (Hub)'
        elif len(locs) == 1:
            location = list(locs)[0]
        else:
            location = ', '.join(sorted(locs))

        reward_item = None
        reward_qty = 0
        rewards = q.get('rewards', [])
        for r in rewards:
            if r.get('slug'):
                reward_item = r['slug']
                reward_qty = r.get('amount', 1)
                items_to_create.setdefault(reward_item, {
                    'slug': reward_item,
                    'name': r.get('name', reward_item),
                    'type': 'reward',
                    'rarity': r.get('rarity', 'common')
                })
                break

        cur.execute(
            """INSERT OR REPLACE INTO quests 
               (slug, name, giver, prerequisite_slug, location, reward_item, reward_quantity) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (slug, name, giver, prereq, location, reward_item, reward_qty)
        )
        cur.execute("SELECT id FROM quests WHERE slug = ?", (slug,))
        qid = cur.fetchone()[0]
        quest_id_map[slug] = qid

        for obj in q.get('objectives', []):
            obj_id = obj.get('okey') or f"{slug}|{obj.get('type')}"
            html_desc = obj.get('html', '')
            desc = BeautifulSoup(html_desc, 'html.parser').get_text(strip=True) if html_desc else obj.get('type_label', '')
            req_item = obj.get('item_slug')
            item_name = obj.get('item_name')

            if req_item:
                items_to_create.setdefault(req_item, {
                    'slug': req_item,
                    'name': item_name or req_item,
                    'type': 'quest_item',
                    'rarity': 'common'
                })

            cur.execute(
                """INSERT OR REPLACE INTO quest_objectives 
                   (quest_id, obj_id, description, required_item) 
                   VALUES (?, ?, ?, ?)""",
                (qid, obj_id, desc, req_item)
            )

    conn.commit()
    print(f"Saved {len(api_quests)} quests and objectives.")

    # 6. Fetch metadata for items from /api/item-card/{slug}
    print(f"Fetching metadata for {len(items_to_create)} discovered items...")
    for idx, (slug, item_info) in enumerate(items_to_create.items(), 1):
        try:
            r = session.get(f"{BASE_URL}/api/item-card/{slug}", timeout=10)
            if r.ok:
                card = r.json()
                item_info['name'] = card.get('t', item_info['name'])
                item_info['rarity'] = card.get('r', item_info['rarity'])
                item_info['type'] = card.get('c', item_info['type'])
        except Exception:
            pass

        cur.execute(
            "INSERT OR REPLACE INTO items (slug, name, type, rarity) VALUES (?, ?, ?, ?)",
            (item_info['slug'], item_info['name'], item_info['type'], item_info['rarity'])
        )
        if idx % 30 == 0 or idx == len(items_to_create):
            conn.commit()
            print(f"  Processed {idx}/{len(items_to_create)} items...")

    # 7. Store item drop locations
    cur.execute("SELECT id, slug, name FROM items")
    item_by_slug = {}
    item_by_name = {}
    for row in cur.fetchall():
        item_by_slug[row['slug']] = row['id']
        item_by_name[row['name'].lower()] = row['id']

    cur.execute("DELETE FROM item_drops")
    drop_count = 0
    for drop in loot_drop_defs.values():
        name_clean = drop['name'].lower()
        item_id = item_by_name.get(name_clean)

        if not item_id and drop.get('okey'):
            okey_parts = drop['okey'].split('|')
            if len(okey_parts) > 1:
                slug_guess = re.sub(r'^id_[a-z]+_', '', okey_parts[1].lower()).replace('_', '-')
                item_id = item_by_slug.get(slug_guess)

        if item_id:
            cur.execute(
                "INSERT INTO item_drops (item_id, location, drop_rate, source) VALUES (?, ?, ?, ?)",
                (item_id, drop['location'], drop['drop_rate'], drop['source'])
            )
            drop_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully recorded {drop_count} item drops in database.")
    print("Scraping and import complete!")

if __name__ == '__main__':
    run_import()
