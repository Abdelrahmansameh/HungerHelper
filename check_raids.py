with open(r"c:\Users\PC\Documents\HungerHelper\generate_perfect_briefings_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = re.findall(r"'raid_num':\s*(\d+),[\s\S]*?'header_title':\s*([^\n]+)", s)
for m in matches:
    print(m)
