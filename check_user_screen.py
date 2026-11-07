from PIL import Image
import os

img_p = r"C:/Users/PC/.gemini/antigravity/brain/3867ac2b-acf9-4012-a98a-a6fd52e96d49/.user_uploaded/media_1793831515451_f14e1f96.png"
if os.path.exists(img_p):
    im = Image.open(img_p)
    print("User screenshot size:", im.size, "mode:", im.mode)
