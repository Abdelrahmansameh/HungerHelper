with open("co_pilot/map_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

# Inspect around generate_location_poi_map
old_poi_block = '''    # 2. General database lookup in map_points
    tokens = [t for t in q.replace("ou", "").replace("se", "").replace("trouve", "").replace("trouver", "").replace("o?", "").split() if len(t) > 2]
    matched_points = []
    target_map = target_map_hint or "Jacques Bridge"

    for tok in tokens:
        c.execute("""
            SELECT map_name, title, point_type, x, y, description
            FROM map_points
            WHERE title LIKE ? OR quest_slug LIKE ? OR description LIKE ?
            LIMIT 5
        """, (f"%{tok}%", f"%{tok}%", f"%{tok}%"))
        pts_found = c.fetchall()
        if pts_found:
            matched_points = [dict(p) for p in pts_found]
            target_map = matched_points[0]["map_name"]
            break'''

# Let's check how the block actually appears in utf-8
idx = text.find("# 2. General database lookup in map_points")
print("Found block at:", idx)
print(text[idx:idx+500])
