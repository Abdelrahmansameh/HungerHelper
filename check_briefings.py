with open(r"c:\Users\PC\Documents\HungerHelper\generate_perfect_briefings_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = re.findall(r'def generate_raid(\d+)_briefing', s)
print("Briefing functions:", matches)

# Check titles
for i in range(1, 8):
    p = s.find(f"generate_raid{i}_briefing")
    if p != -1:
        print(f"Raid {i}:")
        print(s[p:p+300])
