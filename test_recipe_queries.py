import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

queries = [
    "metallurgist recipe spear",
    "peasant's burden spear",
    "peasant burden",
    "cook recipe brioche",
    "artificer recipe damascus armour plate"
]

print("=== TESTING ITEM QUERIES ===")
for q in queries:
    res = brain.process_message(user_id="1", username="Abdallah", text=q)
    print(f"\nQuery: '{q}'")
    print("Spoken:", res.get("spoken_text", "")[:100])
    print("Display:", res.get("display_text", "").splitlines()[0] if res.get("display_text") else "NONE")
    print("Attachment:", res.get("image_attachment"))
