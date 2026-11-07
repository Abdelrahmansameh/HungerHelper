with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("function selectRaid(idx)")
end = s.find("function toggleActiveQuestComplete")
lines = s[p:end].split("\n")
for i, l in enumerate(lines):
    safe_l = l.encode('ascii', 'replace').decode('ascii')
    print(f"{i}: {safe_l[:100]}")
