import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(205, min(len(lines), 280)):
    print(f"{i+1}: {lines[i].rstrip()}")
