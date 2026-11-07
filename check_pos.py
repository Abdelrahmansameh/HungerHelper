with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("const EMBEDDED_MAPS")
print(s[p:p+300])
p2 = s.find("const EMBEDDED_ICONS")
print(s[p2-200:p2+200])
