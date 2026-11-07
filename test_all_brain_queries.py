# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    ("combien coute la farine", "1. Item / Loot"),
    ("combien coute le family ring", "2. Quest Item"),
    ("fiche arme de la zweihander", "3. Melee Weapon"),
    ("combien coute le auster", "4. Firearm Auster"),
    ("combien coute le deux", "5. Firearm Deux"),
    ("en combien de coup je tue un joueur en vert avec le auster", "6. TTK Auster vs Green"),
    ("combien de coups avec la zweihander pour tuer la brute", "7. TTK Melee vs Brute"),
    ("ou se trouve family gavroche", "8. Location / GPS Map"),
    ("fiche quete the gavroche family", "9. Quest Sheet"),
    ("tactique contre le baveux", "10. Monster / Bestiary Drooler"),
    ("fiche personnage marie", "11. Character Sheet Marie"),
    ("fiche personnage jean", "12. Character Sheet Jean"),
    ("comment explorer jacques folly", "13. Dungeon Sheet Jacques Folly"),
    ("fiche skin robe noire", "14. Cosmetic Skin Sheet"),
    ("meilleur build pour la lance", "15. Talent Build Sheet")
]

for q, label in test_queries:
    res = brain.process_message("test_user", "Abdallah", q)
    has_img = bool(res.get("image_attachment"))
    img_name = res.get("image_attachment", "").split("\\")[-1] if has_img else "None"
    print(f"[{label}] Query: \"{q}\"")
    print(f"  Spoken: {res.get('spoken_text', '')[:70]}...")
    print(f"  Has Image: {has_img} ({img_name})")
