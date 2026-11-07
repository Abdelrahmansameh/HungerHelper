import sqlite3

conn = sqlite3.connect("hunger_helper.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

print("--- FLOUR RECORD ---")
c.execute("SELECT * FROM companion_items_cache WHERE slug = 'flour'")
r = c.fetchone()
if r:
    for k in r.keys():
        print(f"{k}: {r[k]}")

print("\n--- ALL QUESTS ---")
for q in c.execute("SELECT * FROM quests"):
    print(f"ID: {q['id']}, Name: {q['name']}, Giver: {q['giver']}, Desc: {q['description']}")

conn.close()
