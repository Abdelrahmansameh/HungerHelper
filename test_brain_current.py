import sys
from co_pilot.brain import CoPilotBrain

b = CoPilotBrain()

queries = [
    "montre moi les skin de la rapier",
    "montre moi les skins de la rapier",
    "combien coute heavy ammo",
    "ou est ce que je peux trouver heavy ammo",
    "c'est quoi l'ult de marie",
    "c'est quoi le passif de marie",
    "passive de marie",
    "ou je peux trouver le skin de la spear peasant",
    "peasant burden",
    "peasant's burden spear",
    "metallurgist recipe spear",
    "cook recipe brioche",
    "artificer recipe damascus armour plate"
]

with open("brain_test_output.txt", "w", encoding="utf-8") as out:
    for q in queries:
        out.write("=" * 60 + "\n")
        out.write(f"QUERY: {q}\n")
        try:
            res = b.process_message("user1", "Abdallah", q)
            out.write(f"spoken_text: {res.get('spoken_text')}\n")
            out.write(f"image_attachment: {res.get('image_attachment')}\n")
            out.write(f"image_attachments: {res.get('image_attachments')}\n")
            disp = res.get('display_text', '')
            out.write(f"display_text: {disp[:300]}\n")
        except Exception as e:
            import traceback
            out.write(f"ERROR: {traceback.format_exc()}\n")

print("Finished testing, output written to brain_test_output.txt")
