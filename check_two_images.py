import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("overhaul_all_cards.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def render_stash_two_images" in l:
        for j in range(i, min(len(lines), i+80)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
