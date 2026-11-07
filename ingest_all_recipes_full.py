import sys, urllib.request, json, time, re, sqlite3, os
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, "hunger_helper.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

professions = ["outfitter", "gunsmith", "metallurgist", "cook", "artificer", "physician"]
all_recipes = {}

for prof in professions:
    url = f"https://hunger-companion.com/recipes/{prof}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
            count = 0
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("/recipes/") and href != f"/recipes/{prof}":
                    slug = href.replace("/recipes/", "")
                    txt = a.get_text(" ", strip=True)
                    lvl_m = re.search(r'Level\s*(\d+)', txt)
                    lvl = int(lvl_m.group(1)) if lvl_m else 1
                    
                    rar = "Common"
                    for r in ["Artifact", "Legendary", "Epic", "Rare", "Uncommon", "Common"]:
                        if r in txt:
                            rar = r
                            break
                    
                    clean_name = slug.replace(f"{prof}-recipe-", "").replace("-", " ").title()
                    all_recipes[slug] = {
                        "slug": slug,
                        "name": f"{prof.title()} Recipe - {clean_name}",
                        "profession": prof.title(),
                        "level": lvl,
                        "rarity": rar,
                        "raw_text": txt
                    }
                    count += 1
            print(f"Prof {prof}: found {count} recipes.")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error on {prof}: {e}")

print(f"Total unique recipes scraped across all 6 professions: {len(all_recipes)}")

for slug, r in all_recipes.items():
    cur.execute("""
        INSERT OR REPLACE INTO recipes_full (slug, name, profession, level, rarity, raw_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (slug, r["name"], r["profession"], r["level"], r["rarity"], json.dumps(r)))

conn.commit()
conn.close()

# Also save to data/all_companion_recipes.json
with open("data/all_companion_recipes.json", "w", encoding="utf-8") as out:
    json.dump(all_recipes, out, indent=2, ensure_ascii=False)

print("Saved all recipes to recipes_full and data/all_companion_recipes.json!")
