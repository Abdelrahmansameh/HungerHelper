from PIL import Image
import os

p = "jacques-bridge.webp"
if os.path.exists(p):
    im = Image.open(p)
    print(f"jacques-bridge.webp size={im.size}, mode={im.mode}")
