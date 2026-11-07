with open('co_pilot/game_knowledge.py', 'r', encoding='utf-8') as f:
    text = f.read()

text_n = text.replace('\r\n', '\n')

old_part = """    from co_pilot.card_renderer import render_talent_build_card
    card_path = render_talent_build_card(query, is_french)"""

new_part = """    from co_pilot.card_renderer import render_talent_build_cards_both
    p1, p2 = render_talent_build_cards_both()
    card_path = p1"""

old_ret = 'return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}'
new_ret = 'return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path, "image_attachments": [p1, p2]}'

if old_part in text_n and old_ret in text_n:
    text_n = text_n.replace(old_part, new_part)
    text_n = text_n.replace(old_ret, new_ret)
    with open('co_pilot/game_knowledge.py', 'w', encoding='utf-8') as f:
        f.write(text_n)
    print("GAME_KNOWLEDGE_TALENTS_UPDATED")
else:
    print("NOT_FOUND in game_knowledge")
