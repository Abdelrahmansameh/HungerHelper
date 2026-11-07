import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def find_item_icon")
print(text[idx:idx+1800])
