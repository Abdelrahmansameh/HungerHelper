import sqlite3
import glob
import os

print("Searching DBs...")
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".db") or f.endswith(".sqlite") or f.endswith(".json"):
            p = os.path.join(root, f)
            if "venv" in p or ".git" in p: continue
            if f.endswith(".json"):
                try:
                    with open(p, "r", encoding="utf-8") as jf:
                        content = jf.read()
                        if "moist" in content.lower():
                            print(f"Found 'moist' in JSON: {p}")
                except Exception:
                    pass
            else:
                try:
                    conn = sqlite3.connect(p)
                    cur = conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cur.fetchall()
                    for t in tables:
                        tname = t[0]
                        try:
                            cur.execute(f"SELECT * FROM [{tname}] WHERE 1=0")
                            cols = [c[0] for c in cur.description]
                            for col in cols:
                                try:
                                    cur.execute(f"SELECT [{col}], * FROM [{tname}] WHERE CAST([{col}] as TEXT) LIKE '%moist%' LIMIT 5")
                                    res = cur.fetchall()
                                    if res:
                                        print(f"Found in {p} -> {tname}.{col}: {len(res)} results")
                                        for r in res[:2]:
                                            print("   ", r[:5])
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    pass
