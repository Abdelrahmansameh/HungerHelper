import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

print("Length of card_renderer.py:", len(text))
print("find_item_icon index:", text.find("def find_item_icon"))
print("render_item_card index:", text.find("def render_item_card"))
print("render_skin_card index:", text.find("def render_skin_card"))
