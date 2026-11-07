import json

with open('data/full_companion_skins.json', 'r', encoding='utf-8') as f:
    skins = json.load(f)

for k, v in skins.items():
    lore = v.get('lore', '')
    # Remove excessive quotes caused by string replacement
    lore = lore.replace('"', '').replace('“', '').replace('”', '').replace('\ufffd', '')
    # Restore clean string
    v['lore'] = lore.strip()
    
    # Fix fee string
    digits = ''.join(c for c in str(v.get('fee', '')) if c.isdigit())
    copp = int(digits) if digits else 18
    v['resale_copper'] = copp
    v['fee_clean'] = f"{copp} Copper"
    v['fee'] = f"Schema · {copp} Copper"

with open('data/full_companion_skins.json', 'w', encoding='utf-8') as f:
    json.dump(skins, f, indent=2, ensure_ascii=False)

print("Lore and fee cleaned cleanly!")
