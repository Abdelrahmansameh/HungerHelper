import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(250, min(len(lines), 330)):
    print(f"{i+1}: {lines[i].rstrip()}")
