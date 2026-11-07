with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

p = s.find("id: 0,")
print(s[p:p+1200].encode('ascii', 'replace').decode('ascii'))
