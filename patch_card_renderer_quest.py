with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

old_qc = '''def render_quest_card(quest_query: str, is_french: bool = True) -> str:
    return render_clean_gavroche_quest_card(is_french)'''

new_qc = '''def render_quest_card(quest_query: str, is_french: bool = False) -> str:
    from universal_v8_engine import render_dynamic_quest_contract_card
    return render_dynamic_quest_contract_card(quest_query, is_french)'''

assert old_qc in text, "render_quest_card not found in card_renderer.py"
text = text.replace(old_qc, new_qc)

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] card_renderer.py updated: render_quest_card is now fully dynamic!")
