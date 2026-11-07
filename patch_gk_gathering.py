import os

GK_PATH = "co_pilot/game_knowledge.py"

with open(GK_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = '''    # Cosmetic skins and blueprints are handled by the dedicated skin crafting engine!
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "outfit", "apparence", "peasant burden", "bacchus", "loup", "basilisk", "solstice"]):
        return None'''

replacement = '''    # Cosmetic skins and blueprints are handled by the dedicated skin crafting engine!
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "outfit", "apparence", "peasant burden", "bacchus", "loup", "basilisk", "solstice"]):
        return None

    # Gathering nodes are handled by the dedicated gathering engine!
    if any(w in lowered for w in [
        "garlic", "lavender", "clove", "rosemary", "cinnamon", "yarrow", "fungi", "saffron",
        "poppy", "peppercorn", "twine", "screws", "gunpowder", "striker", "lever arm", "lodestone",
        "whale oil", "quicksilver", "burlap", "lead ore", "copper ore", "linen", "cotton", "iron ore",
        "silver ore", "gold ore", "silk"
    ]):
        return None'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open(GK_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched game_knowledge.py successfully.")
else:
    print("Target not found.")
