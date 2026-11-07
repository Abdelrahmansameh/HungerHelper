import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

print("--- SEARCH 1: Points with Chapel, Candle, Book, Altar, Sinai ---")
c.execute("""
SELECT id, title, map_name, x, y, point_type, quest_slug, description 
FROM map_points 
WHERE title LIKE '%chapel%' 
   OR title LIKE '%candle%' 
   OR title LIKE '%book%' 
   OR title LIKE '%altar%' 
   OR title LIKE '%sinai%' 
   OR title LIKE '%rozier%'
   OR title LIKE '%census%'
   OR title LIKE '%catechisme%'
   OR title LIKE '%montesquieu%'
   OR title LIKE '%buffon%'
   OR title LIKE '%rondelet%'
   OR title LIKE '%codex%'
   OR quest_slug LIKE '%candle%'
   OR quest_slug LIKE '%sinai%'
   OR quest_slug LIKE '%sanctuary%';
""")
rows = c.fetchall()
for r in rows:
    print(r)

print("\n--- SEARCH 2: All quest names in DB ---")
c.execute("SELECT id, slug, name, location FROM quests WHERE name LIKE '%Shadow%' OR name LIKE '%Candle%' OR name LIKE '%Sinai%';")
for q in c.fetchall():
    print(q)
