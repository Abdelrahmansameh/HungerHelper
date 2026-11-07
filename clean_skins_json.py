import json, re

with open('data/full_companion_skins.json', 'r', encoding='utf-8') as f:
    skins = json.load(f)

cleaned_count = 0
for k, v in skins.items():
    # Clean fee
    raw_fee = str(v.get('fee', ''))
    digits = ''.join(c for c in raw_fee if c.isdigit())
    if digits:
        v['resale_copper'] = int(digits)
        v['fee_clean'] = f"{digits} Copper"
    else:
        v['resale_copper'] = 18
        v['fee_clean'] = "18 Copper"
    v['fee'] = f"Schema · {v['fee_clean']}"

    # Clean lore
    lore = v.get('lore', '')
    lore = lore.replace('', '"').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    # strip redundant outer quotes
    lore = lore.strip().strip('"')
    v['lore'] = lore

with open('data/full_companion_skins.json', 'w', encoding='utf-8') as f:
    json.dump(skins, f, indent=2, ensure_ascii=False)

print(f"Cleaned all {len(skins)} skins in data/full_companion_skins.json!")
