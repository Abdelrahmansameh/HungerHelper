import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

targets = [
    'Flour', 'Charcoal', 'Bullion', 'Jewellery', 'China Bowl', 'Wall Cabinet',
    'Damp Rag', 'Saltpetre', 'Tallow Balm', 'Medicinals', 'Opium Pipe', 'Opium',
    'Votive Candle', 'Census', 'Rozier', 'Catechisme', 'Laws', 'Buffon', 'Rondelet', 'Codex',
    'Tactical Map', 'Gunline Fort', 'Gavroche'
]

for map_name in ['Sarlat Farm', 'Jacques Bridge', 'Sombre Forest']:
    print(f"\n=================== {map_name} ===================")
    c.execute("SELECT id, title, point_type, x, y FROM map_points WHERE map_name = ?", (map_name,))
    rows = c.fetchall()
    matched = []
    for r in rows:
        title = r[1]
        for t in targets:
            if t.lower() in title.lower():
                matched.append(r)
                break
    print(f"Total matched points: {len(matched)}")
    # Group by category/title
    summary = {}
    for r in matched:
        summary[r[1]] = summary.get(r[1], 0) + 1
    for k, v in sorted(summary.items(), key=lambda x: -x[1])[:30]:
        print(f"  {k} : {v} spots")
