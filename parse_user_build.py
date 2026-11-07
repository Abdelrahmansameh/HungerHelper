import json

with open('mastery_data.json', 'r', encoding='utf-8') as f:
    trees_data = json.load(f)

tree_by_slug = {t['slug']: t for t in trees_data}

code = "00000000000000000000.000000000000000000.0505000530000000000.05041000500051404011400001.0155005505005230010"
CODE_ORDER = ['cunning', 'martial', 'physiology', 'survival', 'arms']

parts = code.split('.')

total_points = 0
results = []

for idx, slug in enumerate(CODE_ORDER):
    tree = tree_by_slug[slug]
    part_str = parts[idx] if idx < len(parts) else ""
    k = 0
    tree_points = 0
    tree_talents = []
    
    for ti, tier in enumerate(tree['tiers']):
        for node in tier['nodes']:
            if node['max'] > 0:
                rank = int(part_str[k]) if k < len(part_str) else 0
                k += 1
                if rank > 0:
                    tree_points += rank
                    tree_talents.append({
                        'tier': ti,
                        'tier_name': f"Tier {ti+1}",
                        'id': node['id'],
                        'name': node['name'],
                        'desc': node['desc'],
                        'rank': rank,
                        'max': node['max'],
                        'icon': node['icon'],
                        'values': node.get('values', []),
                        'req': node.get('req'),
                        'reqId': node.get('reqId'),
                        'reqPts': node.get('reqPts', 0)
                    })
    total_points += tree_points
    results.append({
        'tree_name': tree['name'],
        'slug': slug,
        'color': tree['color'],
        'points': tree_points,
        'talents': tree_talents
    })

print(f"Total points spent: {total_points}")
for r in results:
    print(f"\n=== {r['tree_name']} ({r['points']} points) ===")
    for t in r['talents']:
        print(f"  [{t['tier_name']}] {t['name']}: {t['rank']}/{t['max']} - {t['desc']}")
        print(f"    Icon: {t['icon']}")
