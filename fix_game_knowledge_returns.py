p = "co_pilot/game_knowledge.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Restore line 125
bad_block = """            card_img = None
    try:
        from co_pilot.card_renderer import render_item_card
        card_img = render_item_card(item_en)
    except Exception:
        pass
    res_dict = {"spoken_text": spoken, "display_text": display}
    if card_img:
        res_dict["image_attachment"] = card_img
    return res_dict"""

good_block = """            return {"spoken_text": spoken, "display_text": display}"""

assert bad_block in text, "bad_block not found"
text = text.replace(bad_block, good_block, 1)

# 2. Add card attachment to answer_squad_item_needs_query
target_needs = """        display = (
            f"🎒 **SAFE POUCH & QUEST PRIORITY : {item_en.upper()}**\\n\\n"
            f"• ✅ **Verdict :** **KEEP IN SAFE POUCH!**\\n"
            f"• 📜 **Quest :** **{quest_name}** ({giver})\\n"
            f"• 📦 **Required :** **{quantity}**\\n"
            f"• 📍 **Location :** {location_hint}"
        )
    return {"spoken_text": spoken, "display_text": display}"""

replacement_needs = """        display = (
            f"🎒 **SAFE POUCH & QUEST PRIORITY : {item_en.upper()}**\\n\\n"
            f"• ✅ **Verdict :** **KEEP IN SAFE POUCH!**\\n"
            f"• 📜 **Quest :** **{quest_name}** ({giver})\\n"
            f"• 📦 **Required :** **{quantity}**\\n"
            f"• 📍 **Location :** {location_hint}"
        )
    card_img = None
    try:
        from co_pilot.card_renderer import render_item_card
        card_img = render_item_card(item_en)
    except Exception:
        pass
    res_dict = {"spoken_text": spoken, "display_text": display}
    if card_img:
        res_dict["image_attachment"] = card_img
    return res_dict"""

assert target_needs in text, "target_needs not found"
text = text.replace(target_needs, replacement_needs, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Properly updated game_knowledge.py!")
