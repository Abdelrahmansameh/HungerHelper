import os
from co_pilot.brain import CoPilotBrain

b = CoPilotBrain()

test_queries = [
    ("c'est quoi the hunger", True),
    ("who is mr sweet", False),
    ("histoire du chateau", True),
    ("qui sont les dregs", True),
    ("lore de marie", True),
    ("what is the lore of hunger", False)
]

for q, fr in test_queries:
    res = b.process_message("t1", "Abdallah", q)
    sp = res.get("spoken_text", "")
    disp = res.get("display_text", "")
    img = res.get("image_attachment", "")
    sp_ascii = sp.encode("ascii", errors="replace").decode("ascii")
    disp_first = disp.splitlines()[0].encode("ascii", errors="replace").decode("ascii") if disp else ""
    print(f"\n>>> QUERY: {q}")
    print(f"  Spoken: {sp_ascii[:80]}")
    print(f"  Display: {disp_first}")
    print(f"  Image: {os.path.basename(img) if img else 'None'}")
    assert sp and disp and img, f"Failed for {q}"

print("\nALL LORE QUERIES PASSED PERFECTLY!")
