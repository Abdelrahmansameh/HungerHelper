import os

# Check size and availability of latest raid maps
art_dir = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
for i in range(1, 8):
    p = os.path.join(art_dir, f"raid{i}_map.jpg")
    print(f"Raid {i} map exists: {os.path.exists(p)}, size: {os.path.getsize(p) if os.path.exists(p) else 0}")
