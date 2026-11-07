import json
import re

with open('mastery_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'window\.HUNGER_MASTERY\s*=\s*(\[.*?\]);', html, re.DOTALL)
if not m:
    print("Could not find window.HUNGER_MASTERY")
    exit(1)

data = json.loads(m.group(1))
with open('mastery_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Extracted {len(data)} trees:")
for tree in data:
    node_count = sum(len(t['nodes']) for t in tree['tiers'])
    print(f"- {tree['name']} (slug: {tree['slug']}): {len(tree['tiers'])} tiers, {node_count} nodes")
