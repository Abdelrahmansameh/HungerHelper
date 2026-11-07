from PIL import Image

p = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793853874701_f2615fae.png"
im = Image.open(p)
# Clean crop: remove purple border at y=285
# The box is centered around (75, 75, 215, 215)
crop1 = im.crop((74, 74, 218, 218))
crop1.save("assets/items/T_UI_Item_Schema.png")
print("Saved clean assets/items/T_UI_Item_Schema.png!")
