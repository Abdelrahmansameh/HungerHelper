import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def analyze_inventory_screenshot" in l:
        for j in range(i, min(len(lines), i+90)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
