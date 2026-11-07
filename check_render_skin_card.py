import re

for fname in ["co_pilot/card_renderer.py", "overhaul_all_cards.py"]:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    idx = content.find("def render_skin_card")
    if idx != -1:
        print(f"Found in {fname} at char {idx}:")
        print(content[idx:idx+2500])
