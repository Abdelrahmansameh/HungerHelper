import sqlite3, os, re

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT id, slug, name, type, rarity FROM items WHERE name LIKE '%piro%' OR name LIKE '%lens%' OR name LIKE '%lentille%' OR slug LIKE '%lens%' OR slug LIKE '%piro%'")
print('Items matching in db:', c.fetchall())

c.execute("SELECT id, slug, name, giver, location FROM quests WHERE name LIKE '%piro%' OR name LIKE '%lens%' OR slug LIKE '%piro%' OR slug LIKE '%lens%'")
print('Quests matching in db:', c.fetchall())

# Let's search tracker.js
if os.path.exists('tracker.js'):
    with open('tracker.js', 'r', encoding='utf-8', errors='ignore') as f:
        tjs = f.read()
        for m in re.finditer(r'lens|piro', tjs, re.I):
            idx = m.start()
            print('tracker.js match:', tjs[max(0, idx-50):min(len(tjs), idx+100)])

# Search all files for Peasant's Burden and spawn
print('--- Searching for Peasant Burden / Peasant spawn ---')
for root, dirs, files in os.walk('.'):
    if any(ign in root for ign in ['.git', 'node_modules', '.gemini', '__pycache__']):
        continue
    for fn in files:
        if fn.endswith(('.js', '.json', '.html', '.py', '.txt')):
            fp = os.path.join(root, fn)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'peasant' in content.lower() and ('drop' in content.lower() or 'spawn' in content.lower() or '100%' in content.lower() or 'burden' in content.lower()):
                        for m in re.finditer(r'peasant', content, re.I):
                            idx = m.start()
                            snippet = content[max(0, idx-60):min(len(content), idx+120)]
                            if any(k in snippet.lower() for k in ['drop', 'spawn', '100%', 'chest', 'sarlat', 'bridge', 'sombre', 'burden', 'loot']):
                                print(f"{fp}: {snippet.strip()}")
            except Exception:
                pass
