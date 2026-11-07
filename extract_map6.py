import re, base64

with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

m = re.search(r'6:\s*"data:image/jpeg;base64,([^"]+)"', s)
if m:
    b64 = m.group(1)
    with open(r"C:\Users\PC\Documents\HungerHelper\extracted_map6.jpg", "wb") as f_out:
        f_out.write(base64.b64decode(b64))
    print("Saved extracted_map6.jpg! Size:", len(b64))
else:
    print("Map 6 not found!")
