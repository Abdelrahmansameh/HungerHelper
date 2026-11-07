import os
from PIL import Image

ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    if os.path.exists(p):
        im = Image.open(p)
        print(f"Raid {i} map size: {im.size}, file size: {os.path.getsize(p)}")
    else:
        print(f"Raid {i} map MISSING!")
