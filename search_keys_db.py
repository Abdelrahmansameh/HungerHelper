import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT count(*) FROM map_points")
print("Total map points:", c.fetchone()[0])

c.execute("SELECT id, title, map_name, description FROM map_points WHERE title LIKE '%key%' OR description LIKE '%key%' OR title LIKE '%door%' OR title LIKE '%lock%'")
rows = c.fetchall()
print(f"Matched {len(rows)} rows:")
for r in rows:
    print(r)
