import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
for m in re.finditer(r'gavroche', text, re.I):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 200)
    print(text[start:end])
    print("="*40)
