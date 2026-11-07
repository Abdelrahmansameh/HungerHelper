import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print(f"Total tables: {len(tables)}")
for t in tables:
    c.execute(f'SELECT count(*) FROM "{t}"')
    cnt = c.fetchone()[0]
    print(f"  - {t}: {cnt} rows")
