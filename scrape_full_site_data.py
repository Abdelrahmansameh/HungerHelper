import os, sys, json, sqlite3, requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
BASE_URL = 'https://hunger-companion.com'
DOC_DIR = r'C:\Users\PC\Documents\HungerHelper'
DATA_DIR = os.path.join(DOC_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DOC_DIR, 'hunger_helper.db')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create extra tables for complete game data
cur.execute('''
CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE,
    name TEXT,
    location TEXT,
    role TEXT,
    description TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS npc_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_slug TEXT,
    item_name TEXT,
    price_copper INTEGER,
    price_silver INTEGER,
    category TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS creatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE,
    name TEXT,
    category TEXT,
    notes TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS creature_drops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creature_slug TEXT,
    item_slug TEXT,
    item_name TEXT,
    drop_rate_text TEXT,
    drop_rate_float REAL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS map_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    map_id INTEGER,
    map_name TEXT,
    point_type TEXT,
    quest_slug TEXT,
    x REAL,
    y REAL,
    description TEXT
)
''')
conn.commit()

# 1. Fetch & Store all 3,459 points from the API
print("1. Ingesting all map points from tracker API...")
cur.execute("SELECT slug FROM quests")
all_slugs = [r[0] for r in cur.fetchall()]
try:
    r = requests.get(f"{BASE_URL}/api/tracker", params={'slugs': ','.join(all_slugs)}, headers=HEADERS, timeout=30)
    if r.status_code == 200:
        data = r.json()
        with open(os.path.join(DATA_DIR, 'all_tracker_data.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        points = data.get('points', [])
        map_lookup = {1: 'Sarlat Farm', 2: 'Jacques Bridge', 3: 'Sombre Forest'}
        cur.execute("DELETE FROM map_points")
        for p in points:
            m_id = p.get('map_id', 0)
            cur.execute('''
                INSERT INTO map_points (title, map_id, map_name, point_type, quest_slug, x, y, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                p.get('title'),
                m_id,
                map_lookup.get(m_id, 'Unknown'),
                p.get('type'),
                p.get('quest'),
                p.get('x'),
                p.get('y'),
                p.get('description', '')
            ))
        conn.commit()
        print(f"  Inserted {len(points)} map points into database.")
except Exception as e:
    print(f"  Error fetching points: {e}")

# 2. Ingest NPCs and their shop inventories
print("2. Ingesting all NPCs and merchant shop inventories...")
npcs = [
    ('heinrich-voss', 'Heinrich Voss', 'Cauldron', 'Artificer Master'),
    ('bear', 'Bear', 'Outer Ramparts', 'Survivor'),
    ('claude', 'Claude', 'Cauldron', 'Rogue'),
    ('grillard', 'Grillard', 'Cauldron', 'Cook & Provisioner'),
    ('eloise', 'Eloise', 'Outer Ramparts', 'Story Quest Giver'),
    ('filthy-francois', 'Filthy François', 'Outer Ramparts', 'Miner & Scavenger Merchant'),
    ('voyant-the-rifleman', 'Voyant the Rifleman', 'Cauldron', 'Gunsmith Master'),
    ('hector', 'Hector', 'Cauldron', 'Blacksmith & Enforcer'),
    ('henri', 'Henri', 'Cauldron', 'Merchant'),
    ('henriette', 'Henriette', 'Outer Ramparts', 'Herbalist & Forager'),
    ('jean-fondeur', 'Jean Fondeur', 'Outer Ramparts', 'Metallurgy & Weaponsmith'),
    ('louis', 'Louis', 'Outer Ramparts', 'Stashmaster & Locksmith'),
    ('mr-sweet', 'Mr Sweet', 'Outer Ramparts', 'Artificer & Curiosities'),
    ('octave-de-villiers', 'Octave de Villiers', 'Outer Ramparts', 'Outfitter & Leatherworker'),
    ('sirene', 'Sirène', 'Cauldron', 'Master Tailor'),
    ('doctor-lucien-moreau', 'Doctor Lucien Moreau', 'Cauldron', 'Chief Physician'),
    ('piro', 'Piro', 'Outer Ramparts', 'The Leper Physician'),
    ('reynauld', 'Reynauld', 'Outer Ramparts', 'Expedition Master'),
    ('savant', 'Savant', 'Cauldron', 'Scholar'),
    ('the-white-hat-crone', 'The White Hat Crone', 'Cauldron', 'Apothecary')
]

for slug, name, loc, role in npcs:
    cur.execute('''
        INSERT OR REPLACE INTO npcs (slug, name, location, role, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (slug, name, loc, role, f"{name} located at {loc}"))
    
    # Scrape their shop page if available
    try:
        r = requests.get(f"{BASE_URL}/npcs/{slug}", headers=HEADERS, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if '/items/' in a['href']:
                    item_text = a.get_text(strip=True)
                    cur.execute('''
                        INSERT INTO npc_items (npc_slug, item_name, price_copper, price_silver, category)
                        VALUES (?, ?, 0, 0, 'Shop Item')
                    ''', (slug, item_text))
    except Exception:
        pass
conn.commit()
print("  NPC data inserted.")

# 3. Ingest Creatures & Bestiary
print("3. Ingesting creatures and drop tables...")
creature_slugs = [
    'bloat', 'brute', 'pitchskin', 'dreg', 'iron-dreg', 'drooler', 'pale-lady',
    'shambler', 'iron-shambler', 'waif'
]

for c in creature_slugs:
    cur.execute('''
        INSERT OR REPLACE INTO creatures (slug, name, category, notes)
        VALUES (?, ?, 'Creature', 'Encountered on raids')
    ''', (c, c.replace('-', ' ').title()))
conn.commit()
conn.close()

print("Full site data ingestion finished!")
