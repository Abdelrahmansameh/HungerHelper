import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("overhaul_all_cards.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def render_clean_gavroche_quest_card")
print(text[idx+2400:idx+3800])
