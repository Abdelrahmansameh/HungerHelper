from PIL import Image
import os

p = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\raid6_map.jpg"
im = Image.open(p)
print("raid6_map.jpg size:", im.size)

# Crop the top-left area where the title is written (e.g. 50, 50, 600, 200)
crop1 = im.crop((50, 50, 650, 200))
crop1.save(r"C:\Users\PC\Documents\HungerHelper\raid6_title_crop.png")
print("Saved raid6_title_crop.png")
