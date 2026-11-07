with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

target = 'for w in weapons:\n        if w["slug"] in lowered or w["name_en"].lower() in lowered or w["name_fr"].lower() in lowered:\n            card_path = render_weapon_card(w["slug"], is_french)'

replacement = 'for w_row in weapons:\n        w = dict(w_row)\n        if w["slug"] in lowered or w["name_en"].lower() in lowered or w["name_fr"].lower() in lowered:\n            card_path = render_weapon_card(w["slug"], is_french)'

assert target in text, "target not found"
text = text.replace(target, replacement, 1)

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Replaced successfully.")
