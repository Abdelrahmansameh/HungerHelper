import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in c.fetchall()]
print('Tables in hunger_helper.db:', tables)
for t in tables:
    try:
        c.execute(f"PRAGMA table_info({t})")
        cols = [r[1] for r in c.fetchall()]
        c.execute(f"SELECT count(*) FROM {t}")
        cnt = c.fetchone()[0]
        print(f"  {t} ({cnt} rows): {cols}")
    except Exception as e:
        print(f"  {t}: {e}")
conn.close()
