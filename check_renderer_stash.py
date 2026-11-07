import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def render_stash_report_card" in l:
        for j in range(i, min(len(lines), i+60)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
