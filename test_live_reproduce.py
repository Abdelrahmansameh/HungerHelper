import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

queries = [
    "montre moi la map de jaque",
    "montre moi la map JB",
    "combien coute heavy ammo",
    "ou est ce que je peux trouver heavy ammo",
    "c'est quoi l'ult de marie",
    "c'est quoi le passif de marie",
    "ou je peux trouver le skin de la spear peasant",
    "ou est ce que je peux trouver le skin peasant burden",
    "montre moi les skin de la rapier"
]

for q in queries:
    res = brain.process_message("123", "Abdallah", q)
    print("=" * 60)
    print("QUERY:", q)
    print("  spoken_text:", res.get("spoken_text"))
    print("  display_text:", res.get("display_text"))
    print("  image_attachment:", res.get("image_attachment"))
    if "attachments" in res:
        print("  attachments:", res.get("attachments"))
