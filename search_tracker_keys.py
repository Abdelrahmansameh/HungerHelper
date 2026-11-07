import json, re

with open(r'C:\Users\PC\Documents\HungerHelper\data\all_tracker_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total points in tracker data: {len(data)}")

# Let's search points that have 'key' or 'lock' or 'door' in title or description or tags
key_points = []
for p in data:
    txt = json.dumps(p).lower()
    if any(k in txt for k in ['key', 'door', 'lock', 'bronze', 'silver', 'gold', 'undercroft']):
        key_points.append(p)

print(f"Found {len(key_points)} points matching key/door/lock:")
for p in key_points[:40]:
    print(" - Title:", p.get('title'), "| Map:", p.get('map_name') or p.get('map_id'), "| Description:", p.get('description'))
