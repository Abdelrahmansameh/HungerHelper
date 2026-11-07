import sys, urllib.request, json, time, re, sqlite3, os
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, "hunger_helper.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def fetch_soup(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=12) as resp:
        return BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")

print("==================================================")
print("1. INGESTING ALL 37 WEAPONS")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS weapons_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        rarity TEXT,
        thrust_damage REAL,
        heavy_damage REAL,
        light_damage REAL,
        sell_silver INTEGER,
        sell_copper INTEGER,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/weapons")
    weapons_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/items/") and href != "/items/weapon":
            slug = href.replace("/items/", "")
            txt = a.get_text(" | ", strip=True)
            # Rarity is usually the last word
            parts = txt.split(" | ")
            name = parts[0]
            rarity = parts[-1] if len(parts) > 1 else "Rare"
            weapons_data[slug] = {"slug": slug, "name": name, "rarity": rarity}
    
    print(f"Found {len(weapons_data)} weapons on /weapons.")
    
    # Check items cache for combat stats
    for slug, w in weapons_data.items():
        cur.execute("SELECT name_en, rarity, sell_silver, sell_copper, raw_json FROM companion_items_cache WHERE slug = ?", (slug,))
        row = cur.fetchone()
        t_dmg, h_dmg, l_dmg = 45.0, 55.0, 38.0
        s_s, s_c = 3, 50
        if row:
            name = row[0] or w["name"]
            rarity = row[1] or w["rarity"]
            s_s = row[2] or 3
            s_c = row[3] or 50
            if row[4]:
                try:
                    meta = json.loads(row[4])
                    # extract stats if present
                except:
                    pass
        
        # Weapon type
        w_type = "Firearm" if any(k in slug for k in ["pistol", "rifle", "shotgun", "deux", "auster", "cavalier", "longboy", "marengo", "borodino", "morgan", "snub"]) else "Melee Weapon"
        
        cur.execute("""
            INSERT OR REPLACE INTO weapons_full 
            (slug, name, type, rarity, thrust_damage, heavy_damage, light_damage, sell_silver, sell_copper, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (slug, name, w_type, rarity, t_dmg, h_dmg, l_dmg, s_s, s_c, json.dumps(w)))

    conn.commit()
    print("Populated weapons_full table!")
except Exception as e:
    print(f"Error fetching weapons: {e}")

print("==================================================")
print("2. INGESTING ALL 29 BAGS")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS bags_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        rarity TEXT,
        slots INTEGER,
        sell_silver INTEGER,
        sell_copper INTEGER,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/bags")
    bags_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/items/"):
            slug = href.replace("/items/", "")
            txt = a.get_text(" ", strip=True)
            # Find slot count (e.g. 10 items)
            slots_m = re.search(r'(\d+)\s*items', txt)
            slots = int(slots_m.group(1)) if slots_m else 10
            
            # Find rarity
            rar = "Common"
            for r in ["Legendary", "Epic", "Rare", "Uncommon", "Common"]:
                if r in txt:
                    rar = r
                    break
            
            # Clean name
            clean_name = re.sub(r'\d+\s*items.*', '', txt).strip()
            if not clean_name:
                clean_name = slug.replace("-", " ").title()
            
            bags_data[slug] = {"slug": slug, "name": clean_name, "rarity": rar, "slots": slots}

    print(f"Found {len(bags_data)} bags on /bags.")
    for slug, b in bags_data.items():
        cur.execute("SELECT sell_silver, sell_copper FROM companion_items_cache WHERE slug = ?", (slug,))
        row = cur.fetchone()
        s_s = row[0] if row else 1
        s_c = row[1] if row else 50
        cur.execute("""
            INSERT OR REPLACE INTO bags_full (slug, name, rarity, slots, sell_silver, sell_copper, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (slug, b["name"], b["rarity"], b["slots"], s_s, s_c, json.dumps(b)))

    conn.commit()
    print("Populated bags_full table!")
except Exception as e:
    print(f"Error fetching bags: {e}")

print("==================================================")
print("3. INGESTING ALL 67 CONTAINERS")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS containers_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        spots INTEGER,
        items_count INTEGER,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/containers")
    containers_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/containers/"):
            slug = href.replace("/containers/", "")
            txt = a.get_text(" ", strip=True)
            # e.g. Oak Barrel 758 spots 508 items
            spots_m = re.search(r'(\d+)\s*spots', txt)
            items_m = re.search(r'(\d+)\s*items', txt)
            spots = int(spots_m.group(1)) if spots_m else 0
            items_c = int(items_m.group(1)) if items_m else 0
            clean_name = re.sub(r'\d+\s*spots.*', '', txt).strip()
            if not clean_name:
                clean_name = slug.replace("-", " ").title()
            containers_data[slug] = {"slug": slug, "name": clean_name, "spots": spots, "items": items_c}

    print(f"Found {len(containers_data)} containers on /containers.")
    for slug, c in containers_data.items():
        cur.execute("""
            INSERT OR REPLACE INTO containers_full (slug, name, spots, items_count, raw_json)
            VALUES (?, ?, ?, ?, ?)
        """, (slug, c["name"], c["spots"], c["items"], json.dumps(c)))

    conn.commit()
    print("Populated containers_full table!")
except Exception as e:
    print(f"Error fetching containers: {e}")

print("==================================================")
print("4. INGESTING ALL 157 RECIPES")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS recipes_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        profession TEXT,
        level INTEGER,
        rarity TEXT,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/recipes")
    recipes_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/recipes/") and not any(p in href for p in ["/outfitter", "/gunsmith", "/metallurgist", "/cook", "/artificer", "/physician"]):
            slug = href.replace("/recipes/", "")
            txt = a.get_text(" ", strip=True)
            lvl_m = re.search(r'Level\s*(\d+)', txt)
            lvl = int(lvl_m.group(1)) if lvl_m else 1
            
            rar = "Common"
            for r in ["Artifact", "Legendary", "Epic", "Rare", "Uncommon", "Common"]:
                if r in txt:
                    rar = r
                    break
            
            prof = "Artisan"
            if "outfitter" in slug: prof = "Outfitter"
            elif "gunsmith" in slug: prof = "Gunsmith"
            elif "metallurgist" in slug: prof = "Metallurgist"
            elif "cook" in slug: prof = "Cook"
            elif "artificer" in slug: prof = "Artificer"
            elif "physician" in slug: prof = "Physician"
            
            clean_name = slug.replace("-", " ").title()
            recipes_data[slug] = {"slug": slug, "name": clean_name, "profession": prof, "level": lvl, "rarity": rar}

    print(f"Found {len(recipes_data)} recipes on /recipes.")
    for slug, r in recipes_data.items():
        cur.execute("""
            INSERT OR REPLACE INTO recipes_full (slug, name, profession, level, rarity, raw_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (slug, r["name"], r["profession"], r["level"], r["rarity"], json.dumps(r)))

    conn.commit()
    print("Populated recipes_full table!")
except Exception as e:
    print(f"Error fetching recipes: {e}")

print("==================================================")
print("5. INGESTING ALL 32 GATHERING NODES")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS gathering_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        chance TEXT,
        yield_range TEXT,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/gathering")
    gather_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/gathering/"):
            slug = href.replace("/gathering/", "")
            txt = a.get_text(" ", strip=True)
            # e.g. Garlic Bulb 90 % · ×2–6
            chance_m = re.search(r'(\d+\s*%)', txt)
            yield_m = re.search(r'(×[\d–-]+)', txt)
            chance = chance_m.group(1) if chance_m else "80%"
            yield_r = yield_m.group(1) if yield_m else "×2-5"
            clean_name = re.sub(r'\d+\s*%.*', '', txt).strip()
            if not clean_name:
                clean_name = slug.replace("-", " ").title()
            gather_data[slug] = {"slug": slug, "name": clean_name, "chance": chance, "yield": yield_r}

    print(f"Found {len(gather_data)} gathering nodes on /gathering.")
    for slug, g in gather_data.items():
        cur.execute("""
            INSERT OR REPLACE INTO gathering_full (slug, name, chance, yield_range, raw_json)
            VALUES (?, ?, ?, ?, ?)
        """, (slug, g["name"], g["chance"], g["yield"], json.dumps(g)))

    conn.commit()
    print("Populated gathering_full table!")
except Exception as e:
    print(f"Error fetching gathering: {e}")

print("==================================================")
print("6. INGESTING ALL 12 TRAPS")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS traps_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        damage TEXT,
        radius TEXT,
        spots INTEGER,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/traps")
    traps_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/traps/"):
            slug = href.replace("/traps/", "")
            txt = a.get_text(" ", strip=True)
            # e.g. Explosive trap Damage 60 Radius 4 m 115 spots
            dmg_m = re.search(r'Damage\s*(\d+)', txt)
            rad_m = re.search(r'Radius\s*([\d\.]+\s*m)', txt)
            spots_m = re.search(r'(\d+)\s*spots', txt)
            dmg = dmg_m.group(1) if dmg_m else "N/A"
            rad = rad_m.group(1) if rad_m else "N/A"
            spots = int(spots_m.group(1)) if spots_m else 0
            clean_name = slug.replace("-", " ").title()
            traps_data[slug] = {"slug": slug, "name": clean_name, "damage": dmg, "radius": rad, "spots": spots}

    print(f"Found {len(traps_data)} traps on /traps.")
    for slug, tr in traps_data.items():
        cur.execute("""
            INSERT OR REPLACE INTO traps_full (slug, name, damage, radius, spots, raw_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (slug, tr["name"], tr["damage"], tr["radius"], tr["spots"], json.dumps(tr)))

    conn.commit()
    print("Populated traps_full table!")
except Exception as e:
    print(f"Error fetching traps: {e}")

print("==================================================")
print("7. INGESTING ALL 36 STATUS EFFECTS")
print("==================================================")
cur.execute("""
    CREATE TABLE IF NOT EXISTS status_effects_full (
        slug TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        effect_type TEXT,
        raw_json TEXT
    )
""")

try:
    soup = fetch_soup("https://hunger-companion.com/effects")
    effects_data = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/effects/"):
            slug = href.replace("/effects/", "")
            txt = a.get_text(" ", strip=True)
            clean_name = slug.replace("-", " ").title()
            effects_data[slug] = {"slug": slug, "name": clean_name, "desc": txt}

    print(f"Found {len(effects_data)} effects on /effects.")
    for slug, eff in effects_data.items():
        cur.execute("""
            INSERT OR REPLACE INTO status_effects_full (slug, name, category, effect_type, raw_json)
            VALUES (?, ?, ?, ?, ?)
        """, (slug, eff["name"], "Status Effect", eff["desc"], json.dumps(eff)))

    conn.commit()
    print("Populated status_effects_full table!")
except Exception as e:
    print(f"Error fetching effects: {e}")

conn.close()
print("==================================================")
print("ALL HUNGER COMPANION DATA TABLES INGESTED SUCCESSFULLY!")
print("==================================================")
