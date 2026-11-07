import sqlite3

conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()

def search_term(t):
    print(f"=== SEARCH: {t} ===")
    for tbl in ["weapons", "items", "creatures", "creatures_detailed", "quests"]:
        c.execute(f"PRAGMA table_info({tbl})")
        cols = [r[1] for r in c.fetchall()]
        conditions = " OR ".join([f"{col} LIKE '%{t}%'" for col in cols])
        try:
            c.execute(f"SELECT * FROM {tbl} WHERE {conditions}")
            rows = c.fetchall()
            if rows:
                print(f" Found in {tbl}: {len(rows)} rows")
                for r in rows:
                    print(f"   {r}")
        except Exception as e:
            pass

search_term("marengo")
search_term("drak")
search_term("lash")
search_term("pricker")
search_term("piro")
search_term("sweet")
