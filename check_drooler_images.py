from PIL import Image
import os

im1 = Image.open("assets/bestiary/drooler_full.webp")
print("drooler_full.webp size:", im1.size, "mode:", im1.mode)

im2 = Image.open("assets/bestiary/drooler_face.webp")
print("drooler_face.webp size:", im2.size, "mode:", im2.mode)

im3 = Image.open("assets/items/drooler_jaw.png")
print("drooler_jaw.png size:", im3.size, "mode:", im3.mode)
