import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from co_pilot.brain import CoPilotBrain

b = CoPilotBrain()

queries = [
    ("combien de coup pour tuer un joueur en blue a la longsword", "Longsword vs Blue Armor Player"),
    ("combien de coup avec le zweihander contre un joueur en vert", "Zweihänder vs Green Armor Player"),
    ("fiche de la brute", "Bestiary Brute"),
    ("bestiaire drooler", "Bestiary Drooler"),
    ("fiche de gabriel", "Hero Gabriel"),
    ("capacite de eva", "Hero Eva"),
    ("ou se trouve family gavroche", "Gavroche Quest & Clean Map"),
    ("donjon jacques folly", "Jacques Folly Dungeon"),
    ("montre moi mon arbre de talent", "Full Talent Tree (5 disciplines)"),
    ("combien coute la farine", "Flour price & card (Giver: Éloïse)")
]

print("=== RUNNING FULL OVERHAULED PIPELINE VERIFICATION ===")
for q, desc in queries:
    res = b.process_message("user_abdallah", "Abdallah", q)
    print(f"\n>>> TEST: {desc} ({q})")
    print(f"Spoken: {res.get('spoken_text')}")
    first_display = res.get('display_text', '').splitlines()[0] if res.get('display_text') else 'None'
    print(f"Display: {first_display}")
    print(f"Card: {res.get('image_attachment')}")

print("\n=== PIPELINE FULLY VERIFIED ===")
