import sqlite3

conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()

def dump_table(t):
    print(f"=== TABLE: {t} ===")
    c.execute(f"PRAGMA table_info({t})")
    cols = [r[1] for r in c.fetchall()]
    print("Columns:", cols)
    c.execute(f"SELECT * FROM {t} LIMIT 10")
    for row in c.fetchall():
        print(row)
    print()

dump_table("weapons")
dump_table("creatures")
dump_table("creatures_detailed")
