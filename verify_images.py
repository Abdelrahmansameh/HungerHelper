from PIL import Image

for i in range(1, 8):
    p = f"C:/Users/PC/.gemini/antigravity/brain/d8f00a68-a5af-4b09-aa15-7c0d58ac69ee/raid{i}_map.jpg"
    im = Image.open(p)
    print(f"Raid {i} map: {im.size}, mode: {im.mode}")
