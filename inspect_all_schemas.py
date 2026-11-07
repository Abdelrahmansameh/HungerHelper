import json

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    items = json.load(f)

schemas = {k: v for k, v in items.items() if v.get("c") == "schema"}
print(f"Total schemas: {len(schemas)}")

skins_schemas = {}
recipes_schemas = {}

for k, v in schemas.items():
    if "recipe" in k:
        recipes_schemas[k] = v
    else:
        skins_schemas[k] = v

print(f"Recipe schemas: {len(recipes_schemas)}")
print(f"Skin / Cosmetic / Weapon schemas: {len(skins_schemas)}")

print("\n--- SAMPLE SKIN/WEAPON SCHEMAS ---")
for k, v in list(skins_schemas.items())[:20]:
    print(f"  {k} -> {v['t']} (rarity: {v['r']}, value: {v['v']}c)")

print("\n--- SAMPLE RECIPES ---")
for k, v in list(recipes_schemas.items())[:20]:
    print(f"  {k} -> {v['t']} (rarity: {v['r']}, value: {v['v']}c)")
