import json

with open("data/full_companion_skins.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

print(f"Total skins in full_companion_skins.json: {len(skins)}")
targets = set()
for k, v in skins.items():
    targets.add(v.get("target", "None"))
    if "rapier" in k.lower() or "rapier" in str(v).lower() or "vepr" in k.lower() or "vepr" in str(v).lower():
        print(f"Match: key={k}, name={v.get('name')}, target={v.get('target')}")

print("\nAll targets in skins DB:", sorted(list(targets)))
