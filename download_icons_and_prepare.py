import json
import os
import urllib.request

with open('mastery_data.json', 'r', encoding='utf-8') as f:
    trees_data = json.load(f)

tree_by_slug = {t['slug']: t for t in trees_data}

code = "00000000000000000000.000000000000000000.0505000530000000000.05041000500051404011400001.0155005505005230010"
CODE_ORDER = ['cunning', 'martial', 'physiology', 'survival', 'arms']
parts = code.split('.')

os.makedirs('talent_icons', exist_ok=True)

build_trees = []

for idx, slug in enumerate(CODE_ORDER):
    tree = tree_by_slug[slug]
    part_str = parts[idx] if idx < len(parts) else ""
    k = 0
    tree_talents = []
    
    for ti, tier in enumerate(tree['tiers']):
        for node in tier['nodes']:
            if node['max'] > 0:
                rank = int(part_str[k]) if k < len(part_str) else 0
                k += 1
                if rank > 0:
                    icon_filename = os.path.basename(node['icon'])
                    local_icon_path = os.path.join('talent_icons', icon_filename)
                    if not os.path.exists(local_icon_path):
                        url = f"https://hunger-companion.com{node['icon']}"
                        try:
                            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req) as resp:
                                with open(local_icon_path, 'wb') as img_f:
                                    img_f.write(resp.read())
                            print(f"Downloaded icon: {icon_filename}")
                        except Exception as e:
                            print(f"Failed to download {url}: {e}")
                    
                    tree_talents.append({
                        'tier': ti + 1,
                        'id': node['id'],
                        'name': node['name'],
                        'desc': node['desc'],
                        'rank': rank,
                        'max': node['max'],
                        'icon': icon_filename,
                        'values': node.get('values', [])
                    })
    if tree_talents:
        build_trees.append({
            'name': tree['name'],
            'slug': slug,
            'color': tree['color'],
            'points': sum(t['rank'] for t in tree_talents),
            'talents': tree_talents
        })

with open('user_talents_summary.json', 'w', encoding='utf-8') as f:
    json.dump(build_trees, f, indent=2)

print("Saved user_talents_summary.json successfully.")
