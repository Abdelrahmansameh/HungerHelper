from PIL import Image
import os

# Inspect Skin_Club_01a.webp
skin_p = "assets/skins/Skin_Club_01a.webp"
im = Image.open(skin_p).convert("RGBA")
print("Skin Club 01a size:", im.size)

# The club is on a dark brown background. Let's find the bounding box and remove the dark background
# Bounding box of non-dark pixels:
pixels = im.load()
w, h = im.size
min_x, min_y, max_x, max_y = w, h, 0, 0

# The club has distinct bone/wood colors (r > 60, g > 40, b > 30 and difference from dark bg)
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # Dark brown background is roughly (15-25, 10-18, 8-15)
        if r > 45 or g > 35 or b > 25:
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y

print(f"Detected Club bounding box: ({min_x}, {min_y}, {max_x}, {max_y})")

# Let's crop the club
cropped = im.crop((min_x - 10, min_y - 10, max_x + 10, max_y + 10))
print("Cropped size:", cropped.size)

# Create clean transparent PNG
club_rgba = Image.new("RGBA", cropped.size, (0, 0, 0, 0))
c_pixels = cropped.load()
cw, ch = cropped.size

for y in range(ch):
    for x in range(cw):
        r, g, b, a = c_pixels[x, y]
        # Distance from background color (20, 15, 12)
        brightness = (r + g + b) / 3.0
        if brightness > 40:
            # Smooth alpha transition for anti-aliasing
            alpha = min(255, int((brightness - 35) * 10))
            club_rgba.putpixel((x, y), (r, g, b, alpha))

club_rgba.save("assets/items/T_UI_Item_Club.png")
print("Saved clean transparent club icon to assets/items/T_UI_Item_Club.png!")
