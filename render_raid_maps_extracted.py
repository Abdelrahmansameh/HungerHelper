import os, base64, io
from PIL import Image, ImageDraw, ImageFont

MAP_DIR = r'C:\Users\PC\Documents\HungerHelper'
OUT_DIR = r'C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee'
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading base map images...")
sarlat = Image.open(os.path.join(MAP_DIR, 'sarlat-farm.webp')).convert('RGBA')
bridge = Image.open(os.path.join(MAP_DIR, 'jacques-bridge.webp')).convert('RGBA')
forest = Image.open(os.path.join(MAP_DIR, 'sombre-forest.webp')).convert('RGBA')

# Font helper
try:
    font_large = ImageFont.truetype("arialbd.ttf", 42)
    font_med = ImageFont.truetype("arialbd.ttf", 30)
    font_small = ImageFont.truetype("arial.ttf", 24)
except Exception:
    font_large = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

def draw_tactical_pin(draw, x, y, label, sublabel=None, color=(245, 158, 11, 255), icon="★"):
    # Pulse rings
    draw.ellipse([x-40, y-40, x+40, y+40], fill=(color[0], color[1], color[2], 60), outline=(color[0], color[1], color[2], 180), width=3)
    draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline=(255, 255, 255, 255), width=4)
    
    # Label box
    text = f"{icon} {label}"
    bbox = draw.textbbox((x, y), text, font=font_med)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    box_x1 = x - tw//2 - 15
    box_y1 = y + 25
    box_x2 = x + tw//2 + 15
    box_y2 = y + 25 + th + (25 if sublabel else 12)
    
    draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill=(15, 23, 42, 235), outline=(color[0], color[1], color[2], 255), width=2)
    draw.text((x - tw//2, box_y1 + 6), text, font=font_med, fill=(255, 255, 255, 255))
    if sublabel:
        s_bbox = draw.textbbox((x, y), sublabel, font=font_small)
        s_tw = s_bbox[2] - s_bbox[0]
        draw.text((x - s_tw//2, box_y1 + th + 10), sublabel, font=font_small, fill=(203, 213, 225, 255))

def draw_header_banner(img, title, map_name, key_info):
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, img.width, 100], fill=(15, 23, 42, 235))
    draw.line([0, 100, img.width, 100], fill=(245, 158, 11, 255), width=3)
    draw.text((30, 20), title, font=font_large, fill=(255, 255, 255, 255))
    draw.text((30, 65), f"Map: {map_name}  |  {key_info}", font=font_small, fill=(203, 213, 225, 255))

# ----------------- RAID 1: Sarlat Farm (Making Dough & Pre-Farm) -----------------
print("Rendering Raid 1 map...")
r1 = sarlat.copy()
d1 = ImageDraw.Draw(r1)
draw_header_banner(r1, "RAID 1: SARLAT FARM", "Sarlat Farm", "Active: Making Dough (20x Flour) · No Keys Needed")
draw_tactical_pin(d1, 2500, 2100, "Sarlat Village Granaries", "Primary: 20x Flour (47.6%) & 15x Charcoal", color=(16, 185, 129, 255), icon="🌾")
draw_tactical_pin(d1, 3756, 3530, "Estate Residences", "Check Wall Cabinets for Epic China Bowl (16.1%)", color=(6, 182, 212, 255), icon="💎")
draw_tactical_pin(d1, 716, 2830, "West Granary", "Backup Flour Sacks (47.6%)", color=(16, 185, 129, 255), icon="🌾")
draw_tactical_pin(d1, 3500, 3800, "Safe Extraction", "Perimeter Gate Extraction", color=(244, 63, 94, 255), icon="🚪")
r1_thumb = r1.resize((1280, 1280), Image.Resampling.LANCZOS)
r1_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid1_map.jpg'), quality=85)

# ----------------- RAID 2: Jacques Bridge (Gavroche & Opium) -----------------
print("Rendering Raid 2 map...")
r2 = bridge.copy()
d2 = ImageDraw.Draw(r2)
draw_header_banner(r2, "RAID 2: JACQUES BRIDGE", "Jacques Bridge", "Active: The Gavroche Family · Check for Silver Key")
draw_tactical_pin(d2, 1479, 313, "Gavroche Family Camp", "Primary Quest Location (Instant Complete)", color=(245, 158, 11, 255), icon="★")
draw_tactical_pin(d2, 1044, 2660, "Jacque's Medicinals", "CRUCIAL: 1x Opium (47.6%) & China Bowl (11.2%)", color=(6, 182, 212, 255), icon="⚗️")
draw_tactical_pin(d2, 2100, 1500, "Key Dungeon", "Silver Key drop spot (18.9% chance)", color=(59, 130, 246, 255), icon="🗝️")
draw_tactical_pin(d2, 3800, 2000, "Bridge East Extraction", "Safe Return to Château", color=(244, 63, 94, 255), icon="🚪")
r2_thumb = r2.resize((1280, 1280), Image.Resampling.LANCZOS)
r2_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid2_map.jpg'), quality=85)

# ----------------- RAID 3: Sarlat Farm (Mapping the Front) -----------------
print("Rendering Raid 3 map...")
r3 = sarlat.copy()
d3 = ImageDraw.Draw(r3)
draw_header_banner(r3, "RAID 3: SARLAT FARM", "Sarlat Farm", "Active: Mapping the Front · Scout Gunline & Map")
draw_tactical_pin(d3, 1086, 1299, "Tactical Map (Outpost)", "Primary: Interact with Tactical Map", color=(245, 158, 11, 255), icon="★")
draw_tactical_pin(d3, 1196, 1315, "Gunline Fortification", "Primary: Scout Gunline Fort perimeter", color=(245, 158, 11, 255), icon="★")
draw_tactical_pin(d3, 3587, 3627, "Artillery Trenches & Graves", "Farm: 20x Saltpetre & 5x Damp Rags (23.8%)", color=(16, 185, 129, 255), icon="📦")
draw_tactical_pin(d3, 500, 1200, "Northwest Extraction", "Extract to Château", color=(244, 63, 94, 255), icon="🚪")
r3_thumb = r3.resize((1280, 1280), Image.Resampling.LANCZOS)
r3_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid3_map.jpg'), quality=85)

# ----------------- RAID 4: Sarlat Farm (Red Votive Candle) -----------------
print("Rendering Raid 4 map...")
r4 = sarlat.copy()
d4 = ImageDraw.Draw(r4)
draw_header_banner(r4, "RAID 4: THE RED CANDLE", "Sarlat Farm", "Active: Pushing Back the Shadows (Candle Spawns Now!)")
draw_tactical_pin(d4, 3034, 2516, "Chapel Of Weeping Virgins", "LOOT: Red Votive Candle on the Altar (100%)", color=(239, 68, 68, 255), icon="🕯️")
draw_tactical_pin(d4, 2754, 2172, "Parsonage Lockboxes", "Last Chance: Opium Pipe in Jewellery Box (13.7%)", color=(6, 182, 212, 255), icon="💎")
draw_tactical_pin(d4, 3800, 2800, "East Churchyard Extraction", "Extract to Château -> Turn In Bribery to Mr Sweet", color=(244, 63, 94, 255), icon="🚪")
r4_thumb = r4.resize((1280, 1280), Image.Resampling.LANCZOS)
r4_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid4_map.jpg'), quality=85)

# ----------------- RAID 5: Sarlat Farm (Mount Sinai Books 1, 2, 3) -----------------
print("Rendering Raid 5 map...")
r5 = sarlat.copy()
d5 = ImageDraw.Draw(r5)
draw_header_banner(r5, "RAID 5: MOUNT SINAI (SARLAT)", "Sarlat Farm", "Active: Down From Mount Sinai · Books 1, 2 & 3")
draw_tactical_pin(d5, 2446, 1550, "Book 1: Census of 1806", "Inside Town Registry Office", color=(245, 158, 11, 255), icon="📖")
draw_tactical_pin(d5, 1259, 1065, "Book 2: Rozier's Agriculture", "Inside the Master Granary Office", color=(245, 158, 11, 255), icon="📖")
draw_tactical_pin(d5, 3048, 2488, "Book 3: Catechisme 1567", "Inside Church Library Annex", color=(245, 158, 11, 255), icon="📖")
draw_tactical_pin(d5, 3800, 1500, "River Extraction", "Extract with 3 Books safely in pouch", color=(244, 63, 94, 255), icon="🚪")
r5_thumb = r5.resize((1280, 1280), Image.Resampling.LANCZOS)
r5_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid5_map.jpg'), quality=85)

# ----------------- RAID 6: Jacques Bridge (Mount Sinai Books 4 & 5) -----------------
print("Rendering Raid 6 map...")
r6 = bridge.copy()
d6 = ImageDraw.Draw(r6)
draw_header_banner(r6, "RAID 6: MOUNT SINAI (BRIDGE)", "Jacques Bridge", "Active: Down From Mount Sinai · MANDATORY: BRING SILVER KEY")
draw_tactical_pin(d6, 1391, 1535, "Book 4: The Spirit of the Laws", "Judge's Quarters (Open Room)", color=(245, 158, 11, 255), icon="📖")
draw_tactical_pin(d6, 2094, 1346, "Book 5: Buffon's Natural History", "REQUIRES SILVER KEY: High Court Archive Door", color=(6, 182, 212, 255), icon="🗝️")
draw_tactical_pin(d6, 3800, 2000, "Bridge East Extraction", "Extract with Books 4 & 5", color=(244, 63, 94, 255), icon="🚪")
r6_thumb = r6.resize((1280, 1280), Image.Resampling.LANCZOS)
r6_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid6_map.jpg'), quality=85)

# ----------------- RAID 7: Sombre Forest (Mount Sinai Books 6 & 7) -----------------
print("Rendering Raid 7 map...")
r7 = forest.copy()
d7 = ImageDraw.Draw(r7)
draw_header_banner(r7, "RAID 7: MOUNT SINAI (FOREST)", "Sombre Forest", "Active: Down From Mount Sinai · MANDATORY: BRING GOLD KEY")
draw_tactical_pin(d7, 2592, 2992, "Book 6: Codex Medicamentarius", "Sanatorium Reception Desk", color=(245, 158, 11, 255), icon="📖")
draw_tactical_pin(d7, 3168, 2405, "Book 7: Rondelet Architecture", "REQUIRES GOLD KEY: Command Bunker Steel Vault", color=(245, 158, 11, 255), icon="🗝️")
draw_tactical_pin(d7, 1000, 3500, "South Road Extraction", "Final Extract! Return all 7 tomes to Eloise!", color=(244, 63, 94, 255), icon="🚪")
r7_thumb = r7.resize((1280, 1280), Image.Resampling.LANCZOS)
r7_thumb.convert('RGB').save(os.path.join(OUT_DIR, 'raid7_map.jpg'), quality=85)

print("All 7 tactical maps rendered successfully!")
