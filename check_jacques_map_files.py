from PIL import Image
import os

for p in ["data/maps/jacques_bridge_hq.jpg", "assets/jacques_bridge.png", "data/maps/jacques_bridge.png", "assets/maps/jacques_bridge.png"]:
    if os.path.exists(p):
        im = Image.open(p)
        print(f"Path: {p}, size={im.size}, mode={im.mode}")
