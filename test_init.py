with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("init()")
if p != -1:
    print("init() found:")
    print(s[p-50:p+1000])
else:
    print("init() not found, search window.onload or DOMContentLoaded:")
    for kw in ["window.onload", "DOMContentLoaded", "selectRaid("]:
        pos = s.find(kw)
        if pos != -1:
            print(f"{kw} found at {pos}:")
            print(s[pos:pos+300])
