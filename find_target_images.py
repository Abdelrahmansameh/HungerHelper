import json, re

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

items = {}
for q in t.get('quests', []):
    for obj in q.get('objectives', []):
        html = obj.get('html', '')
        # find img src and item slug
        matches = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>.*?/items/([a-z0-9\-]+)', html)
        for src, slug in matches:
            items[slug] = src

print('Found item images in quests:', len(items))
target_slugs = [
    'bezoar', 'fresh-egg', 'hartshorn', 'heavy-ammunition', 'longboy', 'saltpetre', 
    'sealed-bloodbag', 'seamstress-needle', 'tallow-balm', 'tavern-wine', 'thick-branch', 
    'thin-mead', 'arsenic', 'bloat-spine', 'brute-foot', 'charcoal', 'china-bowl', 
    'damp-rag', 'dreg-head', 'drooler-jaw', 'flour', 'glass-vial', 'opium', 'opium-pipe', 
    'shambler-hand', 'silver-dish', 'waif-head'
]
for slug in target_slugs:
    print(f'{slug}: {items.get(slug)}')
