from PIL import Image
import os

p = "assets/items/T_UI_Item_MoistPouch.png"
if os.path.exists(p):
    im = Image.open(p)
    print(f"Moist Pouch icon loaded successfully: size={im.size}, mode={im.mode}")
else:
    print("Moist Pouch file does not exist!")

sp = "assets/skins/Skin_Longboy_01a.webp"
if os.path.exists(sp):
    sim = Image.open(sp)
    print(f"Skin Longboy 01a loaded successfully: size={sim.size}, mode={sim.mode}")
else:
    print("Skin file does not exist!")
