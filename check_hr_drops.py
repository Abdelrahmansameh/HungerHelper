import sys, json
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('data/high_rate_drops.json', encoding='utf-8'))
print(f"Total entries in high_rate_drops.json: {len(data)}")

# Sample entries
for k in list(data.keys())[:10]:
    v = data[k]
    print(f"KEY: {k} | Title: {v.get('title')} | Cat: {v.get('category')} | Resale: {v.get('sell_display')}")
    if v.get('mob_drops'):
        print(f"  Mob Drops: {v['mob_drops']}")
    if v.get('placed_drops'):
        print(f"  Placed Drops: {v['placed_drops']}")
    if v.get('vendor_buys'):
        print(f"  Vendor Buys: {v['vendor_buys']}")
