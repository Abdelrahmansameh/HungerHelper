"""
Hunger Companion Live Intel & Asset Scraper
Provides rich, faithful game data matching hunger-companion.com:
- Items, Weapons, Pistols, Quests, Recipes, Containers, Drop Rates, Vendors, Lore.
- Caches locally in hunger_helper.db with offline fallback.
- Automatically downloads official game render icons.
"""

import os
import re
import json
import sqlite3
import requests
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "hunger_helper.db")
ASSETS_ITEMS_DIR = os.path.join(ROOT_DIR, "assets", "items")
os.makedirs(ASSETS_ITEMS_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
BASE_URL = "https://hunger-companion.com"

# Common French to English alias mapping
ITEM_ALIASES: Dict[str, str] = {
    "lentille de piro": "piro-s-lens",
    "lentille": "piro-s-lens",
    "piro's lens": "piro-s-lens",
    "piros lens": "piro-s-lens",
    "heavy ammo": "heavy-ammunition",
    "heavy ammunition": "heavy-ammunition",
    "munitions lourdes": "heavy-ammunition",
    "munition lourde": "heavy-ammunition",
    "peasant's burden": "peasant-s-burden-spear",
    "peasant burden": "peasant-s-burden-spear",
    "peasant's burden spear": "peasant-s-burden-spear",
    "peasant burden spear": "peasant-s-burden-spear",
    "metallurgist recipe spear": "metallurgist-recipe-spear",
    "metallurgist recipe": "metallurgist-recipe-spear",
    "spear recipe": "metallurgist-recipe-spear",
    "recette de lance": "metallurgist-recipe-spear",
    "cook recipe brioche": "cook-recipe-brioche",
    "brioche recipe": "cook-recipe-brioche",
    "artificer recipe damascus armour plate": "artificer-recipe-damascus-armour-plate",
    "damascus armour plate recipe": "artificer-recipe-damascus-armour-plate",
    "fardeau du paysan": "peasant-s-burden-spear",
    "fardeau": "peasants-burden",
    "club": "club",
    "gourdin": "club",
    "rapier": "rapier",
    "rapiere": "rapier",
    "rapière": "rapier",
    "vepr": "vepr",
    "solstice": "solstice-vepr",
    "loup": "loup-rapier",
    "basilisk": "basilisk-rapier",
    "deux": "deux",
    "le deux": "deux",
    "pistolet deux": "deux",
    "family ring": "family-ring",
    "anneau de famille": "family-ring",
    "bague de famille": "family-ring",
    "farine": "flour",
    "flour": "flour",
    "salpetre": "saltpetre",
    "salpêtre": "saltpetre",
    "saltpetre": "saltpetre",
    "charbon": "charcoal",
    "charcoal": "charcoal",
    "zweihander": "zweihander",
    "zweihänder": "zweihander",
    "zwei": "zweihander",
    "lance": "spear",
    "spear": "spear",
    "hallebarde": "halberd",
    "halberd": "halberd",
    "dague": "dagger",
    "dagger": "dagger",
    "longboy": "longboy",
    "long boy": "longboy",
    "fusil": "longboy",
    "clef d'or": "gold-key",
    "cle d'or": "gold-key",
    "clef d'argent": "silver-key",
    "cle d'argent": "silver-key",
    "clef de bronze": "bronze-key",
    "cle de bronze": "bronze-key",
    "bezoard": "bezoar",
    "bezoar": "bezoar",
    "opium": "opium",
    "pipe a opium": "opium-pipe",
    "pipe d'opium": "opium-pipe",
    "bol en porcelaine": "china-bowl",
    "chiffon humide": "damp-rag",
    "baume de suif": "tallow-balm",
    "bougie votive": "votive-candle",
    "tete de rodeur": "dreg-head",
    "machoire de baveux": "drooler-jaw",
    "main de titubant": "shambler-hand",
    "pied de brute": "brute-foot",
    "auster": "auster",
    "cavalier": "cavalier",
    "marengo": "marengo",
    "morgan": "morgan",
    "borodino": "borodino",
    "snub": "snub",
    "vepr": "vepr"
}

def init_companion_cache_table():
    """Ensure companion_items_cache table exists in SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companion_items_cache (
            slug TEXT PRIMARY KEY,
            name_en TEXT,
            name_fr TEXT,
            category TEXT,
            rarity TEXT,
            lore_desc TEXT,
            usage_desc TEXT,
            base_value INTEGER,
            sell_silver INTEGER,
            sell_copper INTEGER,
            max_stack INTEGER,
            best_container TEXT,
            best_creature TEXT,
            vendor_buy TEXT,
            quests_needed TEXT,
            combat_stats TEXT,
            image_filename TEXT,
            raw_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_companion_cache_table()

def normalize_query_to_slug(query: str) -> str:
    """Resolve user query string to clean companion item slug with strict word boundaries."""
    clean = query.lower().strip()
    clean = re.sub(r'^(combien\s+se\s+vend|combien\s+coute|combien\s+vaut|prix\s+de|prix\s+du|fiche\s+de|stats\s+du|stats\s+de|le|la|les|un|une|l[\'\’])\s+', '', clean).strip()
    
    clean_spaced = clean.replace("-", " ")
    if clean in ITEM_ALIASES:
        return ITEM_ALIASES[clean]
    if clean_spaced in ITEM_ALIASES:
        return ITEM_ALIASES[clean_spaced]
        
    for k in sorted(ITEM_ALIASES.keys(), key=len, reverse=True):
        k_spaced = k.replace("-", " ")
        if re.search(r'\b' + re.escape(k_spaced) + r'\b', clean_spaced):
            return ITEM_ALIASES[k]
            
    # Try slugifying
    return clean.replace(" ", "-").replace("'", "-")

def fetch_and_cache_companion_item(slug: str) -> Optional[Dict[str, Any]]:
    """
    Fetch comprehensive item metadata from hunger-companion.com and cache in SQLite.
    Returns structured dictionary matching the web summary layout.
    """
    url = f"{BASE_URL}/items/{slug}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=7)
        if r.status_code != 200:
            return None
    except Exception as e:
        print(f"[Companion Scraper] Network error fetching {slug}: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    # 1. Main Header
    hdr = soup.find("header", class_="fh")
    hdr_text = hdr.get_text() if hdr else text

    # Name
    h1 = soup.find("h1")
    name_en = h1.get_text().strip() if h1 else slug.replace("-", " ").title()

    # Rarity
    rarity = "Common"
    for r_check in ["Upcoming", "Legendary", "Epic", "Rare", "Uncommon", "Common"]:
        if r_check in hdr_text:
            rarity = r_check
            break

    # Category (from nav.crumb)
    category = "Item"
    crumb_nav = soup.find("nav", class_="crumb")
    if crumb_nav:
        c_links = [a.get_text().strip() for a in crumb_nav.find_all("a")]
        valid_cats = [c for c in c_links if c not in ["Items", "Previous", "Next"] and not re.search(r'\d+\s+of\s+\d+', c)]
        if valid_cats:
            category = " > ".join(valid_cats)
    else:
        cat_match = re.search(r"Items\s*›\s*([^›\n\r]+)", text)
        if cat_match:
            category = cat_match.group(1).strip()

    # In-Game Lore Quote (blockquote.lore)
    lore_desc = ""
    bq = soup.find("blockquote")
    if bq:
        lore_desc = bq.get_text().strip()

    # Usage summary (first descriptive paragraph)
    usage_desc = ""
    for p in soup.find_all("p"):
        p_txt = p.get_text().strip()
        if len(p_txt) > 20 and not any(skip in p_txt for skip in ["Discord", "surest", "Privacy", "Log in", "Playtest"]):
            usage_desc = p_txt
            break

    # Base value & sell price
    val_m = re.search(r"Base value\s*(\d+)", text)
    base_val = int(val_m.group(1)) if val_m else 0
    sell_silver = base_val // 100
    sell_copper = base_val % 100

    # Max stack
    stack_m = re.search(r"Max stack\s*(\d+)", text)
    max_stack = int(stack_m.group(1)) if stack_m else 1

    # Best container & chance
    best_container = None
    cont_m = re.search(r"containers\s*Best:\s*([^1-9\n\r]+)\s*(1/[\d\.,]+)", text)
    if cont_m:
        best_container = f"{cont_m.group(1).strip()} ({cont_m.group(2).strip()})"

    # Best creature
    best_creature = None
    creat_m = re.search(r"creatures\s*Best:\s*([^1-9\n\r]+)\s*(1/[\d\.,]+)", text)
    if creat_m:
        best_creature = f"{creat_m.group(1).strip()} ({creat_m.group(2).strip()})"

    # Vendor stock
    vendor_buy = None
    vend_m = re.search(r"In vendor stock[^\n\r]*\d+ vendor\s*([^\d\n\r]+)\s*(\d+)", text)
    if vend_m:
        v_name = vend_m.group(1).strip()
        v_cost = int(vend_m.group(2).strip())
        vendor_buy = f"{v_name} ({v_cost//100}s {v_cost%100}c)"

    # Quests needed
    quests_needed = []
    for qm in re.finditer(r"(?:Asked by \d+ quests?|Needed for quests\s*\d+)\s*([A-Za-z0-9 \'\-]+)", text):
        q = qm.group(1).strip()
        if "Browse" in q:
            q = q.split("Browse")[0].strip()
        if q and q not in quests_needed and len(q) < 40:
            quests_needed.append(q)

    # Combat stats (for firearms and weapons)
    combat_stats = {}
    dmg_m = re.search(r"Damage per bullet\s*([\d\.]+)", text)
    clip_m = re.search(r"Clip size\s*(\d+)", text)
    rel_m = re.search(r"Full reload\s*([\d\.]+)s?", text)
    between_m = re.search(r"Between shots\s*([\d\.]+)s?", text)
    ammo_m = re.search(r"Fires\s*([^\n\r\·]+)", text)

    if dmg_m: combat_stats["damage"] = dmg_m.group(1)
    if clip_m: combat_stats["clip"] = clip_m.group(1)
    if rel_m: combat_stats["reload"] = rel_m.group(1)
    if between_m: combat_stats["rate"] = between_m.group(1)
    if ammo_m: combat_stats["ammo"] = ammo_m.group(1).strip()

    # Image extraction & download
    img_url = None
    if hdr:
        for img in hdr.find_all("img"):
            src = img.get("src", "")
            if "/media/" in src and "currency" not in src:
                img_url = src.split("?")[0]
                break
    if not img_url:
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if "/media/items/" in src or "/media/renders/" in src:
                img_url = src.split("?")[0]
                break

    image_filename = None
    if img_url:
        image_filename = os.path.basename(img_url)
        local_target = os.path.join(ASSETS_ITEMS_DIR, image_filename)
        if not os.path.exists(local_target):
            try:
                full_img_url = BASE_URL + img_url
                ir = requests.get(full_img_url, headers=HEADERS, timeout=10)
                if ir.status_code == 200:
                    with open(local_target, "wb") as f:
                        f.write(ir.content)
            except Exception as e:
                print(f"[Companion Scraper] Error downloading asset {img_url}: {e}")

    # Remove stray emojis/unicode symbols from text fields
    def clean_txt(s: str) -> str:
        if not s: return ""
        return re.sub(r'[^\x00-\x7F\u00C0-\u017F\u0100-\u024F]+', ' ', s).strip()

    lore_desc = clean_txt(lore_desc)
    usage_desc = clean_txt(usage_desc)
    best_container = clean_txt(best_container) if best_container else None
    best_creature = clean_txt(best_creature) if best_creature else None
    vendor_buy = clean_txt(vendor_buy) if vendor_buy else None

    # French translation heuristic
    name_fr = name_en
    for fr_term, en_term in ITEM_ALIASES.items():
        if en_term == slug and len(fr_term) > 3:
            name_fr = fr_term.title()
            break

    item_data = {
        "slug": slug,
        "name_en": name_en,
        "name_fr": name_fr,
        "category": category,
        "rarity": rarity,
        "lore_desc": lore_desc or usage_desc or "Objet officiel HUNGER répertorié au Château.",
        "usage_desc": usage_desc,
        "base_value": base_val,
        "sell_silver": sell_silver,
        "sell_copper": sell_copper,
        "max_stack": max_stack,
        "best_container": best_container or "Conteneurs de raid",
        "best_creature": best_creature,
        "vendor_buy": vendor_buy,
        "quests_needed": json.dumps(quests_needed),
        "combat_stats": json.dumps(combat_stats),
        "image_filename": image_filename,
        "raw_json": json.dumps({
            "name": name_en, "rarity": rarity, "category": category,
            "lore": lore_desc, "quests": quests_needed, "combat": combat_stats
        })
    }

    # Store in SQLite cache
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO companion_items_cache
            (slug, name_en, name_fr, category, rarity, lore_desc, usage_desc, base_value,
             sell_silver, sell_copper, max_stack, best_container, best_creature, vendor_buy,
             quests_needed, combat_stats, image_filename, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_data["slug"], item_data["name_en"], item_data["name_fr"], item_data["category"],
            item_data["rarity"], item_data["lore_desc"], item_data["usage_desc"], item_data["base_value"],
            item_data["sell_silver"], item_data["sell_copper"], item_data["max_stack"],
            item_data["best_container"], item_data["best_creature"], item_data["vendor_buy"],
            item_data["quests_needed"], item_data["combat_stats"], item_data["image_filename"],
            item_data["raw_json"]
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Companion Scraper] SQLite insert error: {e}")

    return item_data

def get_companion_item_intel(query_or_slug: str) -> Optional[Dict[str, Any]]:
    """
    Look up item intelligence:
    1. Check SQLite companion_items_cache directly by raw slug or normalized slug.
    2. If not found, fetch live from hunger-companion.com and cache.
    """
    raw_slug = query_or_slug.lower().strip()
    slug = normalize_query_to_slug(query_or_slug)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Try exact raw slug, then normalized slug
    cur.execute("SELECT * FROM companion_items_cache WHERE slug = ? OR slug = ? LIMIT 1", (raw_slug, slug))
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT * FROM companion_items_cache WHERE slug LIKE ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1",
                    (f"%{slug}%", f"%{slug}%", f"%{slug}%"))
        row = cur.fetchone()
    conn.close()

    if row:
        d = dict(row)
        try:
            d["quests_needed"] = json.loads(d["quests_needed"] or "[]")
            d["combat_stats"] = json.loads(d["combat_stats"] or "{}")
        except:
            d["quests_needed"] = []
            d["combat_stats"] = {}
        return d

    # If not in cache, fetch live
    return fetch_and_cache_companion_item(slug)
