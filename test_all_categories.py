import sys
from co_pilot.brain import CoPilotBrain

b = CoPilotBrain()

test_queries = [
    # 1. Weapons & Firearms
    ("stats de la spear", "Weapons"),
    ("degats du club", "Weapons"),
    ("degats de marengo", "Firearms"),
    ("combien vaut le deux", "Firearms"),
    # 2. Skins & Cosmetics
    ("montre moi les skins de la rapier", "Skins"),
    ("peasant burden", "Skins"),
    ("ou je peux trouver le skin de la spear peasant", "Skins"),
    # 3. Recipes
    ("metallurgist recipe spear", "Recipes"),
    ("cook recipe brioche", "Recipes"),
    ("artificer recipe damascus armour plate", "Recipes"),
    # 4. Bags
    ("combien de slots a coldstream pack", "Bags"),
    ("ludwig's drumcase", "Bags"),
    # 5. Items (700 items)
    ("combien coute heavy ammo", "Items"),
    ("ou est ce que je peux trouver heavy ammo", "Items"),
    ("farine", "Items"),
    # 6. Hero Abilities
    ("c'est quoi l'ult de marie", "Heroes"),
    ("passive de marie", "Heroes"),
    ("ult de hugo", "Heroes"),
    # 7. Creatures / Bestiary
    ("stats de la brute", "Bestiary"),
    ("combien de pv a la pale lady", "Bestiary"),
    # 8. Traps & Status Effects
    ("explosive trap", "Traps"),
    ("c'est quoi light bleed", "Effects"),
    # 9. Gathering
    ("ou trouver garlic bulb", "Gathering"),
    # 10. Quests & Locations
    ("piro's lens", "Quests"),
    ("carte sans indication sombre", "Maps")
]

results = []
for q, cat in test_queries:
    try:
        res = b.process_message("user1", "Abdallah", q)
        sp = res.get("spoken_text", "")
        disp = res.get("display_text", "")
        img = res.get("image_attachment", "")
        imgs = res.get("image_attachments", [])
        status = "PASS" if sp or disp else "FAIL"
        results.append((q, cat, status, sp[:80], str(img or imgs)[:60]))
    except Exception as e:
        results.append((q, cat, f"FAIL: {e}", "", ""))

with open("category_test_results.txt", "w", encoding="utf-8") as out:
    for q, cat, status, sp, img in results:
        out.write(f"[{status}] ({cat}) '{q}' -> Spoken: '{sp}' | Img: {img}\n")

print(f"Tested {len(test_queries)} queries across all 10 categories!")
