import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "stash" in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
