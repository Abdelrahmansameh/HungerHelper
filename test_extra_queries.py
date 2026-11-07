import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    "carte de sombre",
    "carte de sombre sans rien",
    "carte de sarlat",
    "carte de jacques bridge",
    "club",
    "marengo",
    "montre moi mon arbre de talent"
]

print("=== RUNNING EXTRA TESTS ===")
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
