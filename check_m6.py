from PIL import Image

im = Image.open(r"C:\Users\PC\Documents\HungerHelper\extracted_map6.jpg")
print("Size:", im.size)
crop = im.crop((20, 10, 600, 65))
crop.save(r"C:\Users\PC\Documents\HungerHelper\map6_header.png")
print("Saved map6_header.png")
