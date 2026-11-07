# -*- coding: utf-8 -*-
with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add import core if missing
if "import perfect_briefings_core_v25 as core" not in text:
    text = "import perfect_briefings_core_v25 as core\n" + text

# 2. Add words to creature keywords check
old_c_check = 'and any(w in lowered for w in ["pv", "vie", "degat", "dégât", "battre", "tuer", "vaincre", "comment", "c\'est quoi", "stats", "faiblesse", "loot", "drop", "info", "boss", "qui est", "quels sont"])'
old_c_check_raw = 'and any(w in lowered for w in ["pv", "vie", "degat", "dgt", "battre", "tuer", "vaincre", "comment", "c\'est quoi", "stats", "faiblesse", "loot", "drop", "info", "boss", "qui est", "quels sont"])'

new_c_check = 'and (any(w in lowered for w in ["pv", "vie", "degat", "dégât", "battre", "tuer", "vaincre", "comment", "c\'est quoi", "stats", "faiblesse", "loot", "drop", "info", "boss", "qui est", "quels sont", "tactique", "fiche", "astuce", "conseil", "stratégie", "strategie"]) or "baveux" in lowered or "drooler" in lowered or "brute" in lowered or "pitchskin" in lowered)'

if old_c_check in text:
    text = text.replace(old_c_check, new_c_check, 1)
elif old_c_check_raw in text:
    text = text.replace(old_c_check_raw, new_c_check, 1)
else:
    # Use regex
    import re
    text = re.sub(r'and any\(w in lowered for w in \["pv".*?\]\)', new_c_check, text, count=1)

# 3. Fix line 1007 core.ITEM_IMGS
text = text.replace('icon_name=f"{it[\'slug\']}.png" if f"{it[\'slug\']}.png" in core.ITEM_IMGS else None',
                    'icon_name=f"{it[\'slug\']}.png"')

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] brain.py creature & core references fixed.")
