import re

with open("co_pilot/companion_intel.py", "r", encoding="utf-8") as f:
    text = f.read()

# Add aliases to ITEM_ALIASES
extra_aliases = """    "lentille de piro": "piro-s-lens",
    "lentille": "piro-s-lens",
    "piro's lens": "piro-s-lens",
    "piros lens": "piro-s-lens",
    "heavy ammo": "heavy-ammunition",
    "heavy ammunition": "heavy-ammunition",
    "munitions lourdes": "heavy-ammunition",
    "munition lourde": "heavy-ammunition",
    "peasant's burden": "peasants-burden",
    "peasant burden": "peasants-burden",
    "fardeau du paysan": "peasants-burden",
    "fardeau": "peasants-burden",
    "club": "club",
    "gourdin": "club",
    "rapier": "rapier",
    "rapiere": "rapier",
    "rapière": "rapier",
    "vepr": "vepr",
    "solstice": "solstice-vepr",
    "loup": "loup-rapier",
    "basilisk": "basilisk-rapier","""

if '"lentille de piro"' not in text:
    text = text.replace('ITEM_ALIASES: Dict[str, str] = {', f'ITEM_ALIASES: Dict[str, str] = {{\n{extra_aliases}')
    print("Added extra item aliases to ITEM_ALIASES!")

with open("co_pilot/companion_intel.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated companion_intel.py successfully!")
