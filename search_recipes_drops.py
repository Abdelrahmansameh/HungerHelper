import json, os, glob

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Keys in all_tracker_data:', d.keys())

# Check containers / drops / recipes
recipes = d.get('recipes', [])
print('Total recipes:', len(recipes))
for r in recipes[:15]:
    print(r)

# Check items with skin or recipe
items = d.get('items', [])
print('Total items:', len(items))
for it in items:
    name = str(it.get('name', '')).lower()
    if 'peasant' in name or 'skin' in name or 'recipe' in name or 'schema' in name:
        print('Item match:', it)
