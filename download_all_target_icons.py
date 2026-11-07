import json, re, os, requests

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

items = {}
for q in t.get('quests', []):
    for obj in q.get('objectives', []):
        html = obj.get('html', '')
        # href="/items/slug" ... src="/media/items/..."
        matches = re.findall(r'href="/items/([a-z0-9\-]+)"[^>]*><img[^>]+src="([^"]+)"', html)
        for slug, src in matches:
            items[slug] = src

target_slugs = [
    'bezoar', 'fresh-egg', 'hartshorn', 'heavy-ammunition', 'longboy', 'saltpetre', 
    'sealed-bloodbag', 'seamstress-needle', 'tallow-balm', 'tavern-wine', 'thick-branch', 
    'thin-mead', 'arsenic', 'bloat-spine', 'brute-foot', 'charcoal', 'china-bowl', 
    'damp-rag', 'dreg-head', 'drooler-jaw', 'flour', 'glass-vial', 'opium', 'opium-pipe', 
    'shambler-hand', 'silver-dish', 'waif-head'
]

print(f"Target items count: {len(target_slugs)}")
missing = []
for slug in target_slugs:
    src = items.get(slug)
    print(f"{slug}: {src}")
    if not src:
        missing.append(slug)

print("Missing:", missing)

# Download any that are found into assets/items
DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")
os.makedirs(ITEM_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = 'https://hunger-companion.com'

for slug in target_slugs:
    src = items.get(slug)
    if src:
        local_path = os.path.join(ITEM_DIR, f"{slug.replace('-', '_')}.png")
        if not os.path.exists(local_path):
            url = BASE_URL + src if src.startswith('/') else src
            try:
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(r.content)
                    print(f"Downloaded {slug} -> {local_path}")
            except Exception as e:
                print(f"Error downloading {slug}: {e}")
