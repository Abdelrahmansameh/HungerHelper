import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import os
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}
ROOT_DIR = r"c:\Users\PC\Documents\HungerHelper"

slugs = [
    'zweihander', 'halberd', 'sabre', 'axe', 'rapier', 'spear', 'war-axe', 'longsword', 'mace', 'short-sword', 'club', 'dagger', 'pricker',
    'volcan', 'borodino', 'marengo', 'morgan', 'cavalier', 'deux', 'auster', 'longboy', 'snub',
    'belier', 'drak', 'farsight-drak', 'jager', 'farsight-swan', 'farsight-voir', 'lasher', 'lionne', 'swan', 'voir', 'kompas', 'vepr', 'louisville', 'volant', 'brown-betty'
]

results = {}

for slug in slugs:
    url = f"https://hunger-companion.com/items/{slug}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            print(f"Failed {slug}: {r.status_code}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        main_text = soup.get_text(separator="\n", strip=True)
        lines = [l.strip() for l in main_text.splitlines() if l.strip()]

        # Name
        h1 = soup.find("h1")
        name = h1.get_text().strip() if h1 else slug.replace("-", " ").title()

        # Rarity & Category from nav.crumb or text
        category = "Weapons"
        weapon_type = "Firearm"
        crumb = soup.find("nav", class_="crumb")
        if crumb:
            c_text = crumb.get_text()
            if "Melee" in c_text:
                weapon_type = "Melee Weapon"
            elif "Pistols" in c_text:
                weapon_type = "Pistol"
            elif "Rifles" in c_text:
                weapon_type = "Rifle"
            elif "Shotguns" in c_text:
                weapon_type = "Shotgun"

        # Determine Rarity
        rarity = "Common"
        for r_cand in ["Legendary", "Epic", "Rare", "Uncommon", "Common"]:
            if r_cand in main_text[:300]:
                rarity = r_cand
                break

        # Extract stats
        dmg = 0
        clip = 1
        reload_s = "3.0s"
        ammo = "Heavy Ammunition"
        desc = ""

        # Search for ammo
        ammo_match = re.search(r'Takes\s+([A-Za-z\s]+?Ammunition)', main_text, re.IGNORECASE)
        if ammo_match:
            ammo = ammo_match.group(1).strip()

        # Search for damage
        for i, l in enumerate(lines):
            if l.lower() in ["damage per bullet", "damage"]:
                if i + 1 < len(lines):
                    val_str = lines[i+1].replace(",", ".")
                    val_match = re.search(r'(\d+(?:\.\d+)?)', val_str)
                    if val_match:
                        dmg = float(val_match.group(1))
            if l.lower() in ["clip size", "capacity"]:
                if i + 1 < len(lines):
                    c_match = re.search(r'(\d+)', lines[i+1])
                    if c_match:
                        clip = int(c_match.group(1))
            if l.lower() in ["full reload", "reload time"]:
                if i + 1 < len(lines):
                    reload_s = f"{lines[i+1]}s"

        # Lore / Description
        for i, l in enumerate(lines):
            if "a hefty" in l.lower() or "an early" in l.lower() or "a heavy" in l.lower() or "takes" in l.lower():
                desc = l
                break

        # Headshot damage
        hs_dmg = int(dmg * 1.75) if dmg > 0 else 0

        # Melee checks
        is_two_handed = slug in ["zweihander", "halberd", "spear", "war-axe", "longsword"]
        is_one_handed = slug in ["sabre", "axe", "rapier", "mace", "short-sword", "club", "dagger", "pricker"]

        results[slug] = {
            "slug": slug,
            "name": name,
            "type": weapon_type,
            "rarity": rarity,
            "is_two_handed": is_two_handed,
            "is_one_handed": is_one_handed,
            "damage": dmg,
            "headshot": hs_dmg,
            "clip": clip,
            "reload": reload_s,
            "ammo": ammo,
            "desc": desc
        }
        print(f"Scraped {slug}: {name} ({weapon_type}, {rarity}) -> Dmg: {dmg}, HS: {hs_dmg}, Ammo: {ammo}")
    except Exception as e:
        print(f"Error scraping {slug}: {e}")

# Save JSON
out_json = os.path.join(ROOT_DIR, "data", "all_weapons_complete.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} weapons to {out_json}")
