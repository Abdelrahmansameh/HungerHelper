import os
from PIL import Image

os.makedirs("assets/creatures", exist_ok=True)
p = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793853901975_288e60bf.png"
im = Image.open(p)
crop_farmer = im.crop((32, 18, 102, 88))
crop_farmer.save("assets/creatures/dreg_farmer.png")
print("Saved assets/creatures/dreg_farmer.png!")
