import urllib.request
from bs4 import BeautifulSoup
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

os.makedirs("assets/skins", exist_ok=True)
os.makedirs("assets/items", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_soup(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")

full_skins = {}

# 1. Weapon & Bag skins from items
items_to_check = ["longboy", "brown-betty", "axe", "cavalier", "damp-knapsack", "ragged-sack", "old-satchel", "heavy-crossbow", "zweihander", "spear"]

for it in items_to_check:
    url = f"https://hunger-companion.com/items/{it}"
    try:
        soup = fetch_soup(url)
        figures = soup.find_all("figure", class_=lambda c: c and "skg__c" in c)
        for fig in figures:
            b = fig.find("b")
            if not b: continue
            name = b.text.strip()
            rar = fig.find(class_=lambda c: c and "rar" in c)
            rarity = rar.text.strip() if rar else "Common"
            img = fig.find("img")
            img_url = img.get("src") if img else ""
            
            # Mats
            mats = []
            for mat_a in fig.find_all("a", class_="mat"):
                mat_img = mat_a.find("img")
                mat_qty = mat_a.find("i")
                mats.append({
                    "name": mat_a.get("title", "").split("×")[0].strip(),
                    "qty": mat_qty.text.strip() if mat_qty else "1",
                    "img_url": mat_img.get("src") if mat_img else "",
                    "slug": mat_a.get("href", "").replace("/items/", "")
                })
            
            fee_el = fig.find(class_="skg__p")
            lore_el = fig.find(class_="skg__l")
            
            full_skins[name.lower()] = {
                "name": name,
                "type": "weapon" if it not in ["damp-knapsack", "ragged-sack", "old-satchel"] else "bag",
                "target": it.capitalize(),
                "rarity": rarity,
                "img_url": img_url,
                "fee": fee_el.text.strip() if fee_el else "Atelier d'Artisan",
                "lore": lore_el.text.strip() if lore_el else "",
                "materials": mats
            }
            print(f"Loaded skin: {name} ({len(mats)} mats)")
    except Exception as e:
        print(f"Error {it}: {e}")

# 2. Character skins
characters = ["eva", "marie", "hugo", "gabriel", "otto", "serine"]
for ch in characters:
    url = f"https://hunger-companion.com/characters/{ch}"
    try:
        soup = fetch_soup(url)
        articles = soup.find_all("article", class_=lambda c: c and "chx" in c)
        for art in articles:
            h3 = art.find("h3")
            if not h3: continue
            name = h3.text.strip()
            rar = art.find(class_=lambda c: c and "rar" in c)
            rarity = rar.text.strip() if rar else "Common"
            img = art.find("img")
            img_url = img.get("src") if img else ""
            
            mats = []
            for li in art.find_all("li"):
                mat_span = li.find(class_="chx-mn")
                mat_b = li.find("b")
                mat_img = li.find("img")
                if mat_span:
                    mats.append({
                        "name": mat_span.text.strip(),
                        "qty": mat_b.text.replace("×", "").strip() if mat_b else "1",
                        "img_url": mat_img.get("src") if mat_img else "",
                        "slug": ""
                    })
            
            full_skins[f"{name.lower()} ({ch})"] = {
                "name": name,
                "type": "character",
                "target": ch.capitalize(),
                "rarity": rarity,
                "img_url": img_url,
                "fee": "Atelier du Tailleur",
                "lore": f"Tenue de confection officielle pour {ch.capitalize()}.",
                "materials": mats
            }
            # Also key by skin name
            if name.lower() not in full_skins:
                full_skins[name.lower()] = full_skins[f"{name.lower()} ({ch})"]
        print(f"Loaded {len(articles)} skins for {ch}")
    except Exception as e:
        print(f"Error {ch}: {e}")

with open("data/full_skins_database.json", "w", encoding="utf-8") as out:
    json.dump(full_skins, out, ensure_ascii=False, indent=2)

print(f"Total full skins stored: {len(full_skins)}")
