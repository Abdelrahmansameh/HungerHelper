import sqlite3

conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()
c.execute("SELECT * FROM map_points WHERE title LIKE '%piro%' OR description LIKE '%piro%' OR quest_slug LIKE '%piro%'")
for r in c.fetchall():
    print(r)
