import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT id, title, map_name, x, y, description FROM map_points WHERE quest_slug = 'down-from-mount-sinai' OR title LIKE '%Census%' OR title LIKE '%Rozier%' OR title LIKE '%Doctrine%' OR title LIKE '%Montesquieu%' OR title LIKE '%Buffon%' OR title LIKE '%Rondelet%' OR title LIKE '%Medicamentarius%'")
rows = c.fetchall()
print(f"Found {len(rows)} map points related to Mount Sinai:")
for r in rows:
    print(f"ID: {r[0]} | Title: {r[1]} | Map: {r[2]} | X: {r[3]}, Y: {r[4]}")
    print(f"  Description: {r[5]}")
