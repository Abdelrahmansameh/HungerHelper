import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    "montre moi les skin de la rapier",
    "montre moi les skins de la rapier",
    "c'est quoi l'ult de marie",
    "c'est quoi le passif de marie",
    "passive de marie",
    "ou je peux trouver le skin de la spear peasant",
    "ou est ce que je peux trouver le skin peasant burden",
    "combien coute heavy ammo",
    "ou est ce que je peux trouver heavy ammo",
    "ou est la quete piro's nest",
    "ou est piro's lens",
    "lentille de piro"
]

print("=== RUNNING TEST SUITE ===")
for q in test_queries:
    res = brain.process_message(user_id="1", username="Abdallah", text=q)
    spk = res.get("spoken_text", "")
    disp = res.get("display_text", "")
    img = res.get("image_attachment", "")
    imgs = res.get("image_attachments", [])
    print(f"\n--- QUERY: '{q}' ---")
    print(f"Spoken: {spk[:80]}")
    print(f"Display title: {disp.splitlines()[0] if disp else 'NONE'}")
    print(f"Attachment: {img}")
    if imgs:
        print(f"Attachments ({len(imgs)}): {imgs}")
