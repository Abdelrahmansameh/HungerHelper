with open('co_pilot/brain.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = """        tal_res = answer_talent_advice_query(clean_text, is_french)
        if tal_res:
            card_path = render_talent_build_card(clean_text, is_french)
            tal_res["image_attachment"] = card_path
            return tal_res"""

new_block = """        tal_res = answer_talent_advice_query(clean_text, is_french)
        if tal_res:
            from co_pilot.card_renderer import render_talent_build_cards_both
            p1, p2 = render_talent_build_cards_both(username, 100)
            tal_res["image_attachment"] = p1
            tal_res["image_attachments"] = [p1, p2]
            return tal_res"""

text_n = text.replace('\r\n', '\n')
old_n = old_block.replace('\r\n', '\n')
if old_n in text_n:
    text_n = text_n.replace(old_n, new_block)
    with open('co_pilot/brain.py', 'w', encoding='utf-8') as f:
        f.write(text_n)
    print('BRAIN_UPDATED')
else:
    print('NOT_FOUND')
