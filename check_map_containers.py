import sqlite3
from collections import Counter

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

# Check distinct container types / point types on each map
for map_id in [1, 2, 3]:
    c.execute("SELECT name FROM maps WHERE id = ?", (map_id,))
    map_name = c.fetchone()[0]
    c.execute("SELECT type, count(*) FROM map_points WHERE map_id = ? GROUP BY type ORDER BY count(*) DESC", (map_id,))
    print(f"\n--- MAP {map_id}: {map_name} ---")
    for row in c.fetchall():
        print(f"  {row[0]}: {row[1]}")
