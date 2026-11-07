with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

for kw in ["ROUTE WALKTHROUGH", "HIGH-DENSITY LOOT TARGETS", "CREATURE & LOOSE WORLD LOOT", "FAST-TRACK STASH CHECKLIST", "WHAT YOU NEED TO FOCUS ON"]:
    pos = s.find(kw)
    print(f"{kw}: pos {pos}")
    if pos != -1:
        print(s[pos-100:pos+400].encode('ascii', 'replace').decode('ascii'))
        print("="*40)
