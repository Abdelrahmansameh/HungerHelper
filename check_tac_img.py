with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

count = s.count('id="tactical-img"')
print('id="tactical-img" count:', count)
import re
for m in re.finditer(r'id=["\']tactical-img["\']', s):
    pos = m.start()
    print("Match at pos:", pos, s[pos-40:pos+80])
