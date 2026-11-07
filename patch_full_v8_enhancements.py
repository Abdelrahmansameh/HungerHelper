# -*- coding: utf-8 -*-
import re

# 1. Patch co_pilot/card_renderer.py for Item Card Header text overlap
with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    cr_text = f.read()

# Replace header creation in render_item_card
old_cr_header = '''    canvas, draw = create_base_canvas(f"FICHE OBJET : {name_fr.upper()} ({name_en.upper()})", tag="INVENTAIRE & BUTIN")'''
new_cr_header = '''    if not is_french or name_fr.strip().lower() == name_en.strip().lower():
        title_str = f"ITEM PROFILE : {name_en.upper()}"
        tag_str = "INVENTORY & LOOT"
    else:
        title_str = f"FICHE OBJET : {name_fr.upper()}"
        tag_str = "INVENTAIRE & BUTIN"
    canvas, draw = create_base_canvas(title_str, tag=tag_str)'''

assert old_cr_header in cr_text, "Item card header not found in card_renderer.py"
cr_text = cr_text.replace(old_cr_header, new_cr_header)

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(cr_text)

print("[OK] card_renderer.py item card header patched.")
