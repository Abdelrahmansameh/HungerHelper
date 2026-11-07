import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('Tables:', c.fetchall())

for t in ['map_points', 'items', 'containers', 'quests', 'drop_rates']:
    try:
        c.execute(f"PRAGMA table_info({t});")
        cols = [col[1] for col in c.fetchall()]
        print(f"{t} columns:", cols)
        c.execute(f"SELECT * FROM {t} LIMIT 3;")
        print(f"  sample from {t}:", c.fetchall())
    except Exception as e:
        print(f"  error on {t}:", e)
