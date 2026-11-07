import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def appraise_text_inventory" in l:
        for j in range(i, min(len(lines), i+60)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
