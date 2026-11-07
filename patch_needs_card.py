p = "co_pilot/game_knowledge.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = """    return {"spoken_text": spoken, "display_text": display}"""

replacement = """    card_img = None
    try:
        from co_pilot.card_renderer import render_item_card
        card_img = render_item_card(item_en)
    except Exception:
        pass
    res_dict = {"spoken_text": spoken, "display_text": display}
    if card_img:
        res_dict["image_attachment"] = card_img
    return res_dict"""

assert target in text, "target not found"
text = text.replace(target, replacement, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Added card attachment to answer_squad_item_needs_query successfully!")
