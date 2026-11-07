import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    ("en combien de coup je tue un joueur en vert avec le auster", "Auster vs Joueur en Vert"),
    ("combien de tire au deux pour tuer une personne en armure vert", "Deux vs Joueur en Vert"),
    ("fiche de eva", "Hero Eva"),
    ("capacité de hugo", "Hero Hugo"),
    ("tactical de gabriel", "Hero Gabriel"),
    ("profil de marie", "Hero Marie"),
    ("personnage otto", "Hero Otto"),
    ("sort de serine", "Hero Serine"),
    ("ou se trouve family gavroche", "Quest Family Gavroche"),
    ("combien coute la farine", "Flour price & card")
]

print("=== STARTING FULL VERIFICATION ===")
for q, desc in test_queries:
    res = brain.process_message("user_test_123", "Abdallah", q)
    print(f"\n--- TEST: {desc} ({q}) ---")
    print(f"Spoken: {res.get('spoken_text')}")
    display_first = res.get('display_text', '').splitlines()[0] if res.get('display_text') else 'None'
    print(f"Display title: {display_first}")
    print(f"Image Attachment: {res.get('image_attachment')}")

print("\n=== ALL TESTS COMPLETED ===")
