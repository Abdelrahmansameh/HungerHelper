import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(375, 420):
    print(f"{i+1}: {repr(lines[i])}")
