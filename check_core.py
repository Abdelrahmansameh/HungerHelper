with open(r"c:\Users\PC\Documents\HungerHelper\perfect_briefings_core_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("def render_terrain_map(")
print(s[p:p+2000])
