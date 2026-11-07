import os
from PIL import Image

ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    im = Image.open(p)
    # Check top header text area or sample
    # Let's crop (30, 32, 500, 65)
    crop = im.crop((30, 32, 500, 65))
    crop.save(r"C:\Users\PC\Documents\HungerHelper" + f"\\header_{i}.png")
    print(f"Header {i} saved")
