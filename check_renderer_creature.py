import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def render_creature_card")
if idx != -1:
    print(text[idx:idx+1200])
else:
    print("Not found in card_renderer.py!")
