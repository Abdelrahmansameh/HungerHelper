from PIL import Image

# Check if raid1 and raid6 images are different
im1 = Image.open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\raid1_map.jpg")
im6 = Image.open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\raid6_map.jpg")

# Compare pixel samples
diff = sum(abs(a - b) for a, b in zip(im1.getpixel((100, 100)), im6.getpixel((100, 100))))
print("Pixel diff at (100, 100):", diff)

# Save thumbnail of raid6
im6.resize((480, 280)).save(r"C:\Users\PC\Documents\HungerHelper\raid6_thumb.png")
print("Saved raid6_thumb.png")
