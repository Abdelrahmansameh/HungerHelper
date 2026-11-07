import json

with open('user_talents_summary.json', 'r', encoding='utf-8') as f:
    trees = json.load(f)

for tree in trees:
    print(f"=== {tree['name']} ({tree['points']} pts) ===")
    for t in tree['talents']:
        desc = t['desc']
        rank = t['rank']
        max_r = t['max']
        print(f"[{t['tier']}] {t['name']} ({rank}/{max_r}) -> {desc}")
