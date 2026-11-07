import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    ("Spear Skins", "montre moi les skin de la spear"),
    ("Jacques Bridge Map", "montre moi la map de jaque"),
    ("Jacques Bridge Map JB", "montre moi la map JB"),
    ("Sarlat Farm Map", "montre moi sarlat"),
    ("Dungeon Jacques Folly", "donjon jacques folly"),
    ("Longsword vs Blue Armor", "combien de coup pour tuer un joueur en blue a la longsword"),
    ("Talent Build", "arbre de talent"),
    ("Character Marie", "personnage marie"),
    ("Stash Analysis", "analyse mon stash")
]

print("=== TESTING ALL V6 QUERIES ===")
for label, q in test_queries:
    print(f"\n--- Testing: [{label}] Query: '{q}' ---")
    try:
        res = brain.process_message("user123", "Abdallah", q)
        spoken = res.get("spoken_text", "")
        display = res.get("display_text", "")
        img = res.get("image_attachment", "")
        imgs = res.get("image_attachments", [])

        print(f"Display: {display[:120]}...")
        print(f"Spoken: {spoken[:120]}...")
        if imgs:
            print(f"Image Attachments ({len(imgs)}):")
            for im in imgs:
                exists = os.path.exists(im)
                print(f"  - {im} (exists: {exists})")
        elif img:
            exists = os.path.exists(img)
            print(f"Single Image: {img} (exists: {exists})")
        else:
            print("No image attached!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")

print("\n=== ALL TESTS FINISHED ===")
