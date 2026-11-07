import os

BRAIN_PATH = "co_pilot/brain.py"

with open(BRAIN_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = '''        is_pure_map_query = (
            any(w in lowered for w in ["map", "carte", "plan"]) and
            not any(w in lowered for w in [
                "poi", "point", "trouver", "drop", "coffre", "container", "clef", "clé", "key",
                "creature", "créature", "baveux", "brute", "drooler", "farm", "route", "speedrun",
                "guide", "tactique", "stratégie", "strat", "skin", "arme", "weapon", "degat"
            ])
        ) or any(w in lowered for w in ["carte sans indication", "map sans indication", "blank map", "pure map", "carte de base"])'''

replacement = '''        is_exact_map_name = lowered.strip() in [
            "sarlat", "sarlat farm", "ferme de sarlat",
            "sombre", "sombre forest", "foret sombre", "forêt sombre",
            "jacques", "jacques bridge", "pont jacques",
            "chateau", "le chateau", "le château", "the chateau"
        ]
        is_pure_map_query = (
            any(w in lowered for w in ["map", "carte", "plan"]) and
            not any(w in lowered for w in [
                "poi", "point", "trouver", "drop", "coffre", "container", "clef", "clé", "key",
                "creature", "créature", "baveux", "brute", "drooler", "farm", "route", "speedrun",
                "guide", "tactique", "stratégie", "strat", "skin", "arme", "weapon", "degat"
            ])
        ) or any(w in lowered for w in ["carte sans indication", "map sans indication", "blank map", "pure map", "carte de base"]) or is_exact_map_name'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open(BRAIN_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched brain.py with is_exact_map_name successfully.")
else:
    print("Target not found.")
