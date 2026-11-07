import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT slug, name_en, name_fr, category, quests_needed FROM companion_items_cache WHERE slug LIKE '%lens%' OR slug LIKE '%piro%' OR name_en LIKE '%lens%' OR name_en LIKE '%piro%'")
rows = c.fetchall()
print(f"Total cache rows: {len(rows)}")
for r in rows:
    print(r)
