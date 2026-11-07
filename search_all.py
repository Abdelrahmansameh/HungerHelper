import os

terms = ["marengo", "drak", "lash", "bloater", "shambler", "pricker"]
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".py", ".json", ".sql", ".txt", ".md")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                    txt = fp.read().lower()
                    for t in terms:
                        if t in txt:
                            print(f"Found '{t}' in {p}")
            except:
                pass
