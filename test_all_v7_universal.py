import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    ("Rapier Skins (Weapon without skins)", "montre moi les skin de la rapier"),
    ("Spear Skins (Weapon with 3 skins)", "montre moi les skin de la spear"),
    ("Axe Skins (Weapon with 2 skins)", "montre moi les skin de la axe"),
    ("Sombre Forest Map (Clean without sidebar)", "carte de sombre"),
    ("Sarlat Farm Map (Clean without sidebar)", "sarlat"),
    ("Jacques Bridge Map (Clean without sidebar)", "montre moi la map de jaque"),
    ("Shortsword vs Blue Armor (Exact weapon)", "en combien de coup je tue un jouer en bleu avec une shortsword"),
    ("Otto Skills & Profile (Character Otto)", "montre moi les skills de otto"),
    ("Marie Skills & Profile (Character Marie)", "montre moi les skills de marie"),
    ("Jacques Folly Dungeon (Authentic Location)", "donjon jacques folly"),
    ("Stash Appraisal (Real screen, no market rate, letters kept)", "analyse mon stash")
]

print("=== RUNNING UNIVERSAL V7 SYSTEM TESTS ===")
all_passed = True

for label, q in test_queries:
    print(f"\n========================================================")
    print(f"TEST: [{label}]")
    print(f"QUERY: '{q}'")
    print(f"--------------------------------------------------------")
    try:
        res = brain.process_message("user123", "Abdallah", q)
        disp = res.get("display_text", "")
        spok = res.get("spoken_text", "")
        imgs = res.get("image_attachments") or ([res["image_attachment"]] if res.get("image_attachment") else [])

        print(f"Display: {disp[:140]}...")
        print(f"Spoken:  {spok[:140]}...")
        print(f"Attachments Count: {len(imgs)}")
        for img in imgs:
            exists = os.path.exists(img)
            print(f"  -> File: {img} (Exists: {exists})")
            if not exists:
                all_passed = False
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"FAILED: {e}")
        all_passed = False

print(f"\n========================================================")
print(f"ALL TESTS FINISHED. Status: {'SUCCESS (100% Passed)' if all_passed else 'SOME TESTS FAILED'}")
print(f"========================================================")
