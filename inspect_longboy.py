import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT map_name, title, point_type, x, y FROM map_points WHERE title LIKE '%longboy%' LIMIT 5")
print(c.fetchall())
