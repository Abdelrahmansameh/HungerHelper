import sys, json, sqlite3
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT slug, name_en, category, lore_desc, usage_desc, best_container, quests_needed FROM companion_items_cache WHERE slug LIKE '%lens%' OR slug LIKE '%piro%'")
for r in c.fetchall():
    print(r)

# Check all json files in data
import glob
for f in glob.glob("data/*.json"):
    try:
        txt = open(f, encoding='utf-8', errors='ignore').read()
        if "lens" in txt.lower():
            print("Found in", f)
    except:
        pass
