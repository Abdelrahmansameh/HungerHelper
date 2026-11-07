with open(r"c:\Users\PC\Documents\HungerHelper\perfect_briefings_core_v5.py", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("ACTIVE-QUEST")
if p != -1:
    print(s[p-100:p+300])
else:
    print("Not found in core, search in generate:")
    with open(r"c:\Users\PC\Documents\HungerHelper\generate_perfect_briefings_v5.py", "r", encoding="utf-8") as f2:
        s2 = f2.read()
    p2 = s2.find("ACTIVE-QUEST")
    print(s2[p2-100:p2+300])
