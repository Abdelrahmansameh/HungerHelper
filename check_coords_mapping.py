import sqlite3
from PIL import Image

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

maps = {
    'Sarlat Farm': r'C:\Users\PC\Documents\HungerHelper\sarlat-farm.webp',
    'Jacques Bridge': r'C:\Users\PC\Documents\HungerHelper\jacques-bridge.webp',
    'Sombre Forest': r'C:\Users\PC\Documents\HungerHelper\sombre-forest.webp'
}

for m_name, path in maps.items():
    im = Image.open(path)
    c.execute("SELECT MIN(x), MAX(x), MIN(y), MAX(y), COUNT(*) FROM map_points WHERE map_name = ?", (m_name,))
    min_x, max_x, min_y, max_y, count = c.fetchone()
    print(f"{m_name}:")
    print(f"  Image size: {im.size} (W x H)")
    print(f"  Points: count={count}, X=[{min_x}, {max_x}], Y=[{min_y}, {max_y}]")
