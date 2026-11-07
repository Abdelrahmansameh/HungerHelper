import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT id, title, map_name, point_type, x, y, description FROM map_points WHERE title LIKE '%undercroft%' OR title LIKE '%dungeon%' OR title LIKE '%pit%' OR title LIKE '%sang rouge%' OR description LIKE '%undercroft%' OR description LIKE '%dungeon%'")
rows = c.fetchall()
print(f"Found {len(rows)} dungeon-related points:")
for r in rows:
    print(r)
