import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "is_skin_query" in line:
        for j in range(max(0, i-5), min(len(lines), i+45)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
