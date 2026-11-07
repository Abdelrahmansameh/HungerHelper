with open(r"c:\Users\PC\Documents\HungerHelper\generate_perfect_briefings_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("for cfg in RAIDS_CONFIG:")
if p == -1:
    p = s.find("RAIDS_CONFIG")
    p2 = s.find("for ", p)
    print("Found 'for' at:", p2)
    print(s[p2:p2+1500])
else:
    print(s[p:p+1500])
