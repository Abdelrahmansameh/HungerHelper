import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("overhaul_all_cards.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def render_stash_two_images")
idx2 = text.find("def ", idx + 30)
print(text[idx:idx2 if idx2 != -1 else idx + 3500])
