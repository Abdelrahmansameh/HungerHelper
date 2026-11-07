with open(r"c:\Users\PC\Documents\HungerHelper\generate_perfect_briefings_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("RAIDS_CONFIG = [")
print(s[p:p+2500])
