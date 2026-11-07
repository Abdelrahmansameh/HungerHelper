import os, sys
from PIL import Image, ImageDraw, ImageFont

MAP_DIR = r'C:\Users\PC\Documents\HungerHelper'
ASSET_DIR = os.path.join(MAP_DIR, 'assets')
ITEM_DIR = os.path.join(ASSET_DIR, 'items')
CONT_DIR = os.path.join(ASSET_DIR, 'containers')
OUT_DIR = r'C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee'
os.makedirs(OUT_DIR, exist_ok=True)

# Base maps (4096 x 4096)
print("Loading base map terrain textures...")
sarlat_raw = Image.open(os.path.join(MAP_DIR, 'sarlat-farm.webp')).convert('RGBA')
bridge_raw = Image.open(os.path.join(MAP_DIR, 'jacques-bridge.webp')).convert('RGBA')
forest_raw = Image.open(os.path.join(MAP_DIR, 'sombre-forest.webp')).convert('RGBA')

# Fonts
font_title = ImageFont.truetype("arialbd.ttf", 36)
font_card_h = ImageFont.truetype("arialbd.ttf", 22)
font_bold = ImageFont.truetype("arialbd.ttf", 20)
font_regular = ImageFont.truetype("arial.ttf", 18)
font_small = ImageFont.truetype("arial.ttf", 16)
font_pin_large = ImageFont.truetype("arialbd.ttf", 22)
font_pin_sub = ImageFont.truetype("arial.ttf", 16)

def load_icon(path, size=(68, 68)):
    if os.path.exists(path):
        try:
            img = Image.open(path).convert('RGBA')
            return img.resize(size, Image.Resampling.LANCZOS)
        except Exception:
            return None
    return None

def draw_tactical_pin(draw, x, y, label, sublabel=None, color=(245, 158, 11), num="1"):
    # Target glow rings
    draw.ellipse([x-26, y-26, x+26, y+26], fill=(color[0], color[1], color[2], 50), outline=(color[0], color[1], color[2], 180), width=2)
    draw.ellipse([x-13, y-13, x+13, y+13], fill=color, outline=(255, 255, 255), width=3)
    
    # Pin number
    bbox_n = draw.textbbox((x, y), str(num), font=font_bold)
    nw = bbox_n[2] - bbox_n[0]
    nh = bbox_n[3] - bbox_n[1]
    draw.text((x - nw//2, y - nh//2 - 2), str(num), font=font_bold, fill=(10, 13, 20))

    # Badge box
    text = f"{label}"
    bbox = draw.textbbox((x, y), text, font=font_pin_large)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    box_w = max(tw + 24, 210)
    box_h = th + (24 if sublabel else 14)
    bx1 = x - box_w//2
    by1 = y + 18
    bx2 = x + box_w//2
    by2 = by1 + box_h
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=8, fill=(15, 23, 42, 240), outline=(color[0], color[1], color[2], 255), width=2)
    draw.text((x - tw//2, by1 + 5), text, font=font_pin_large, fill=(255, 255, 255))
    if sublabel:
        s_bbox = draw.textbbox((x, y), sublabel, font=font_pin_sub)
        s_tw = s_bbox[2] - s_bbox[0]
        draw.text((x - s_tw//2, by1 + th + 7), sublabel, font=font_pin_sub, fill=(203, 213, 225))

def build_visual_infographic(base_map, raid_num, title, map_name, quest_name, key_badge, key_color, pins, route_lines, mission_steps, target_items, target_containers, mob_note, post_raid_steps, crop_box=(100, 100, 4000, 4000)):
    canvas = Image.new('RGB', (2400, 1400), (10, 13, 20))
    
    # 1. Full-Map Terrain (Left width 1320, height 1260)
    map_crop = base_map.crop(crop_box)
    map_w, map_h = 1320, 1260
    map_fitted = map_crop.resize((map_w, map_h), Image.Resampling.LANCZOS)
    canvas.paste(map_fitted, (20, 120))
    
    d = ImageDraw.Draw(canvas, 'RGBA')
    d.rectangle([20, 120, 20+map_w, 120+map_h], outline=(51, 65, 85), width=2)
    
    cb_x1, cb_y1, cb_x2, cb_y2 = crop_box
    scale_x = map_w / (cb_x2 - cb_x1)
    scale_y = map_h / (cb_y2 - cb_y1)
    
    def to_canvas(cx, cy):
        return (int(20 + (cx - cb_x1) * scale_x), int(120 + (cy - cb_y1) * scale_y))
    
    # Inter-objective lines connecting targets only
    if route_lines and len(route_lines) > 1:
        for i in range(len(route_lines)-1):
            p1 = to_canvas(route_lines[i][0], route_lines[i][1])
            p2 = to_canvas(route_lines[i+1][0], route_lines[i+1][1])
            d.line([p1, p2], fill=(245, 158, 11, 210), width=4)
    
    # Pins
    for pin in pins:
        px, py = to_canvas(pin['x'], pin['y'])
        draw_tactical_pin(d, px, py, pin['label'], pin.get('sublabel'), pin.get('color', (245, 158, 11)), pin.get('num', '★'))
    
    # 2. Header Bar
    d.rectangle([0, 0, 2400, 105], fill=(15, 23, 42))
    d.line([0, 105, 2400, 105], fill=(245, 158, 11), width=3)
    header_title = f"RAID {raid_num} · {title.upper()}"
    d.text((30, 15), header_title, font=font_title, fill=(255, 255, 255))
    d.text((32, 62), f"REGION: {map_name.upper()}   |   STORY QUEST: {quest_name.upper()}   |   RANDOM SPAWNS & EXITS", font=font_card_h, fill=(203, 213, 225))
    
    # Key Badge (Large and high-contrast)
    kb_w = d.textbbox((0, 0), key_badge, font=font_card_h)[2] + 40
    kb_x = 2360 - kb_w
    d.rounded_rectangle([kb_x, 22, 2360, 82], radius=8, fill=(key_color[0], key_color[1], key_color[2], 40), outline=key_color, width=2)
    d.text((kb_x + 20, 37), key_badge, font=font_card_h, fill=key_color)
    
    # 3. Right Visual Dashboard (Width 1010px: x = 1370 to 2380)
    cur_x = 1370
    cur_w = 1010
    cur_y = 120
    
    # --- Card 1: Mission Objectives (Spacious & Clean) ---
    card_h1 = 150
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+card_h1], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+36], radius=10, fill=(24, 32, 50))
    d.rectangle([cur_x, cur_y+24, cur_x+cur_w, cur_y+36], fill=(24, 32, 50))
    d.line([cur_x, cur_y+36, cur_x+cur_w, cur_y+36], fill=(245, 158, 11), width=2)
    d.text((cur_x+14, cur_y+7), "🎯  MISSION DIRECTIVE & ROUTE (ANY SPAWN POINT)", font=font_card_h, fill=(245, 158, 11))
    
    step_y = cur_y + 46
    for idx, (action, detail) in enumerate(mission_steps, 1):
        d.text((cur_x+16, step_y), f"{idx}. {action}", font=font_bold, fill=(255, 255, 255))
        d.text((cur_x+32, step_y+22), detail, font=font_regular, fill=(203, 213, 225))
        step_y += 34
    
    cur_y += card_h1 + 14
    
    # --- Card 2: Target Items (WITH REAL IMAGES) ---
    item_row_h = 74
    total_items_h = 42 + len(target_items) * (item_row_h + 8) + 6
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+total_items_h], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+36], radius=10, fill=(24, 32, 50))
    d.rectangle([cur_x, cur_y+24, cur_x+cur_w, cur_y+36], fill=(24, 32, 50))
    d.line([cur_x, cur_y+36, cur_x+cur_w, cur_y+36], fill=(6, 182, 212), width=2)
    d.text((cur_x+14, cur_y+7), "💎  TARGET ITEMS TO COLLECT IN THIS RAID", font=font_card_h, fill=(6, 182, 212))
    
    it_y = cur_y + 44
    for it in target_items:
        # Item row card
        d.rounded_rectangle([cur_x+12, it_y, cur_x+cur_w-12, it_y+item_row_h], radius=8, fill=(13, 17, 26), outline=(30, 41, 59), width=1)
        # Paste real item icon
        icon = load_icon(it['icon_path'], (64, 64))
        if icon:
            canvas.paste(icon, (cur_x+18, it_y+5), icon)
        
        # Name and Quantity
        d.text((cur_x+92, it_y+10), it['name'], font=font_bold, fill=(255, 255, 255))
        d.text((cur_x+cur_w-180, it_y+10), it['count'], font=font_bold, fill=(245, 158, 11))
        # Purpose description
        d.text((cur_x+92, it_y+38), it['desc'], font=font_small, fill=(148, 163, 184))
        it_y += item_row_h + 8
        
    cur_y += total_items_h + 14
    
    # --- Card 3: Target Containers (WITH REAL IMAGES) ---
    cont_row_h = 74
    total_conts_h = 42 + len(target_containers) * (cont_row_h + 8) + 6
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+total_conts_h], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+36], radius=10, fill=(24, 32, 50))
    d.rectangle([cur_x, cur_y+24, cur_x+cur_w, cur_y+36], fill=(24, 32, 50))
    d.line([cur_x, cur_y+36, cur_x+cur_w, cur_y+36], fill=(16, 185, 129), width=2)
    d.text((cur_x+14, cur_y+7), "🧰  HIGH-DENSITY CONTAINERS (EXACT CHANCES)", font=font_card_h, fill=(16, 185, 129))
    
    c_y = cur_y + 44
    for ct in target_containers:
        d.rounded_rectangle([cur_x+12, c_y, cur_x+cur_w-12, c_y+cont_row_h], radius=8, fill=(13, 17, 26), outline=(30, 41, 59), width=1)
        icon = load_icon(ct['icon_path'], (64, 64))
        if icon:
            canvas.paste(icon, (cur_x+18, c_y+5), icon)
            
        d.text((cur_x+92, c_y+10), ct['name'], font=font_bold, fill=(255, 255, 255))
        d.text((cur_x+cur_w-180, c_y+10), ct['chance'], font=font_bold, fill=(16, 185, 129))
        d.text((cur_x+92, c_y+38), ct['note'], font=font_small, fill=(148, 163, 184))
        c_y += cont_row_h + 8
        
    cur_y += total_conts_h + 14
    
    # --- Card 4: Mob Target (Concise 1-2 lines, NO KEY FARMING) ---
    if mob_note:
        card_h_mob = 76
        d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+card_h_mob], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
        d.text((cur_x+14, cur_y+12), f"⚔️  HIGH-YIELD MOB TARGET:  {mob_note[0]}", font=font_bold, fill=(244, 63, 94))
        d.text((cur_x+14, cur_y+42), mob_note[1], font=font_regular, fill=(203, 213, 225))
        cur_y += card_h_mob + 14
        
    # --- Card 5: Post-Raid Hand-In ---
    card_h_post = 115
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+card_h_post], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
    d.rounded_rectangle([cur_x, cur_y, cur_x+cur_w, cur_y+32], radius=10, fill=(24, 32, 50))
    d.rectangle([cur_x, cur_y+20, cur_x+cur_w, cur_y+32], fill=(24, 32, 50))
    d.line([cur_x, cur_y+32, cur_x+cur_w, cur_y+32], fill=(245, 158, 11), width=2)
    d.text((cur_x+14, cur_y+6), "⚡  MATCH EXTRACTION & POST-RAID HAND-IN SEQUENCE", font=font_card_h, fill=(245, 158, 11))
    
    post_y = cur_y + 42
    for p_line in post_raid_steps:
        d.text((cur_x+14, post_y), p_line[0], font=font_bold, fill=(255, 255, 255))
        d.text((cur_x+30, post_y+20), p_line[1], font=font_regular, fill=(203, 213, 225))
        post_y += 36
        
    return canvas

# ================= RAID 1: Sarlat Farm (Making Dough) =================
print("Rendering Visual Raid 1...")
pins_1 = [
    {'x': 2500, 'y': 2100, 'label': 'SARLAT VILLAGE (FOOD HUB)', 'sublabel': '597 Flour Sacks · 758 Oak Barrels', 'color': (16, 185, 129), 'num': '1'},
    {'x': 1259, 'y': 1065, 'label': 'WEST GRANARIES & BARNS', 'sublabel': 'Backup Flour Sacks (47.6%) & Ash Hearths', 'color': (16, 185, 129), 'num': '2'},
    {'x': 3756, 'y': 3530, 'label': 'ESTATE BRICK RESIDENCES', 'sublabel': 'Wall Cabinets (16.1% China Bowl) & Desks', 'color': (6, 182, 212), 'num': '3'},
    {'x': 3048, 'y': 2488, 'label': 'CHURCH ASH HEARTHS', 'sublabel': 'Hearths: 15x Charcoal (Pile of Ash 52.6%)', 'color': (245, 158, 11), 'num': '4'}
]
items_1 = [
    {'name': 'Flour', 'count': '20x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'flour.png'), 'desc': 'Primary Story Quest 2 requirement. Complete in 1 raid.'},
    {'name': 'Charcoal (Pre-Farm)', 'count': '15x STASH', 'icon_path': os.path.join(ITEM_DIR, 'charcoal.png'), 'desc': 'Pre-farm for instant turn-in on Quest 4! Do not sell.'},
    {'name': 'China Bowl (Pre-Farm)', 'count': '1x STASH', 'icon_path': os.path.join(ITEM_DIR, 'china_bowl.png'), 'desc': 'Rare Bribery item for Mr Sweet. Search brick estate cabinets & tables.'}
]
conts_1 = [
    {'name': 'Flour Sack', 'chance': '47.6% (1 in 2.1)', 'icon_path': os.path.join(CONT_DIR, 'flour_sack.webp'), 'note': '597 spots across Sarlat farmhouses and granaries.'},
    {'name': 'Oak Barrel', 'chance': '38.5% (1 in 2.6)', 'icon_path': os.path.join(CONT_DIR, 'oak_barrel.webp'), 'note': '758 spots on map. High density along country roads & barns.'},
    {'name': 'Pile of Ash', 'chance': '52.6% (1 in 1.9)', 'icon_path': os.path.join(CONT_DIR, 'pile_of_ash.webp'), 'note': '85 spots. Search all fireplaces and hearths for 15x Charcoal.'},
    {'name': 'Wall Cabinet', 'chance': '16.1% (1 in 6.2)', 'icon_path': os.path.join(CONT_DIR, 'wall_cabinet.webp'), 'note': 'Inside brick houses. Priority container for China Bowl.'}
]
mob_1 = ("Iron Shambler & Dreg Military", "Iron Shamblers drop Charcoal at 1/72 (1.39%); Dreg Militaries drop Flour at 1/112.")
steps_1 = [
    ("Orient toward nearest granary or Sarlat Village: ", "Loot Flour Sacks and Barrels until you hit 20x Flour."),
    ("Sweep all fireplaces for 15x Charcoal: ", "Check estate wall cabinets and dressers for the rare China Bowl.")
]
post_1 = [
    ("Extract through your active match exit gate: ", "Return safely to Château Outer Ramparts."),
    ("Hand in 20x Flour to Eloise: ", "Quest 2 complete -> Unlocks Quest 3! Deposit Charcoal & China Bowl into stash.")
]

img1 = build_visual_infographic(sarlat_raw, 1, "Sarlat Farm · Making Dough", "Sarlat Farm", "Making Dough", "KEYS: NONE NEEDED (KEEP IN STASH)", (16, 185, 129), pins_1, [], steps_1, items_1, conts_1, mob_1, post_1)
img1.save(os.path.join(OUT_DIR, 'raid1_map.jpg'), quality=92)

# ================= RAID 2: Jacques Bridge (Gavroche Family) =================
print("Rendering Visual Raid 2...")
pins_2 = [
    {'x': 1479, 'y': 313, 'label': 'GAVROCHE FAMILY CAMP (QUEST 3)', 'sublabel': 'Lower deck span · Step into camp to complete', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1044, 'y': 2660, 'label': "JACQUE'S MEDICINALS (BRIBERY HUB)", 'sublabel': 'Unique Clinic Box: 47.6% Opium & 11.2% China Bowl/Pipe', 'color': (6, 182, 212), 'num': '2'},
    {'x': 2100, 'y': 1500, 'label': 'ADMINISTRATIVE BLOCK', 'sublabel': 'Bullion Boxes: 13.7% Opium Pipe', 'color': (168, 85, 247), 'num': '3'},
    {'x': 2600, 'y': 1800, 'label': 'ROADWAY BRUTE PATROL', 'sublabel': 'Kill Brutes: 1/52 Opium drop (Highest in game!)', 'color': (244, 63, 94), 'num': '4'}
]
items_2 = [
    {'name': 'Gavroche Camp Report', 'count': 'VISIT CAMP', 'icon_path': os.path.join(ITEM_DIR, 'flour.png'), 'desc': 'Primary Story Quest 3. Auto-triggers upon reaching camp footprint.'},
    {'name': 'Opium (Bribery Pre-Farm)', 'count': '1x STASH', 'icon_path': os.path.join(ITEM_DIR, 'opium.png'), 'desc': 'Required for Mr Sweet. Loot Jacque’s Medicinals or kill Brutes (1/52).'},
    {'name': 'Opium Pipe (Bribery Pre-Farm)', 'count': '1x STASH', 'icon_path': os.path.join(ITEM_DIR, 'opium_pipe.png'), 'desc': 'Required for Mr Sweet. Loot Bullion Boxes (13.7%) or bridge desks.'}
]
conts_2 = [
    {'name': "Jacque's Medicinals", 'chance': '47.6% Opium · 11.2% Pipe/Bowl', 'icon_path': os.path.join(CONT_DIR, 'jacques_medicinals.webp'), 'note': 'Unique clinic container! Single best spot in the game for Bribery items.'},
    {'name': 'Bullion Box', 'chance': '13.7% (1 in 7.3) Opium Pipe', 'icon_path': os.path.join(CONT_DIR, 'bullion_box.webp'), 'note': '119 spots in residential and office bedrooms along bridge.'},
    {'name': 'Ledger Desk', 'chance': 'Valuable Silver Cutlery & Coins', 'icon_path': os.path.join(CONT_DIR, 'ledger_desk.webp'), 'note': '73 spots in bridge offices. Search for coin currency.'}
]
mob_2 = ("Brute & Drooler (Heavy Mobs)", "1/52 (1.92%) Opium · 1/226 Opium Pipe & China Bowl · Top priority mob kill!")
steps_2 = [
    ("Advance to Gavroche Camp (X: 1479, Y: 313): ", "Walking into camp triggers Quest 3 completion automatically."),
    ("Loot Jacque's Medicinals container & hunt Brutes: ", "Secure 1x Opium and 1x Opium Pipe for Mr Sweet's Bribery quest.")
]
post_2 = [
    ("Extract via whichever bridge gate is open: ", "Return to Château Outer Ramparts."),
    ("DOUBLE TURN-IN at Château: ", "Hand in Q3 (Gavroche) -> INSTANT TURN-IN Q4 (15x Charcoal)! Unlocks Quest 5!")
]

img2 = build_visual_infographic(bridge_raw, 2, "Jacques Bridge · Gavroche & Opium", "Jacques Bridge", "The Gavroche Family", "KEYS: NONE NEEDED (KEEP IN STASH)", (16, 185, 129), pins_2, [], steps_2, items_2, conts_2, mob_2, post_2)
img2.save(os.path.join(OUT_DIR, 'raid2_map.jpg'), quality=92)

# ================= RAID 3: Sarlat Farm (Mapping the Front) =================
print("Rendering Visual Raid 3...")
pins_3 = [
    {'x': 1086, 'y': 1299, 'label': 'TACTICAL MAP OUTPOST', 'sublabel': 'Primary 1: Interact with Tactical Map', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1196, 'y': 1315, 'label': 'GUNLINE FORTIFICATION', 'sublabel': 'Primary 2: Scout Fort Perimeter (Completes Q5)', 'color': (245, 158, 11), 'num': '2'},
    {'x': 3587, 'y': 3627, 'label': 'ARTILLERY TRENCHES (SALTPETRE)', 'sublabel': '41 Tooling Bins: 18.9% Saltpetre', 'color': (16, 185, 129), 'num': '3'},
    {'x': 3048, 'y': 2488, 'label': 'CHURCHYARD GRAVES (DAMP RAGS)', 'sublabel': '40 Stone Graves: 23.8% Damp Rag', 'color': (16, 185, 129), 'num': '4'}
]
route_3 = [(1086, 1299), (1196, 1315)]
items_3 = [
    {'name': 'Saltpetre (Pre-Farm Q6)', 'count': '20x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'saltpetre.png'), 'desc': 'Loot Tooling Bins (18.9%) in trenches or kill Dreg Militaries (1/112).'},
    {'name': 'Damp Rag (Pre-Farm Q6)', 'count': '5x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'damp_rag.png'), 'desc': 'Loot Stone Graves (23.8%) in churchyard or Baskets (13.3%).'},
    {'name': 'Tallow Balm (Pre-Farm Q6)', 'count': '10x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'tallow_balm.png'), 'desc': 'Loot Physician Bags / Medical Chests (6.7%) in field tents.'}
]
conts_3 = [
    {'name': 'Tooling Bin', 'chance': '18.9% (1 in 5.3) Saltpetre', 'icon_path': os.path.join(CONT_DIR, 'tooling_bin.webp'), 'note': '41 spots inside artillery trenches and bunker workshops.'},
    {'name': 'Stone Grave', 'chance': '23.8% (1 in 4.2) Damp Rag', 'icon_path': os.path.join(CONT_DIR, 'stone_grave.webp'), 'note': '40 spots in churchyard & battlefield ditch burials.'},
    {'name': 'Physician Bag', 'chance': '6.7% (1 in 15) Tallow Balm', 'icon_path': os.path.join(CONT_DIR, 'physician_bag.webp'), 'note': '98 spots across field medical tents and hospital annexes.'}
]
mob_3 = ("Dreg Military (Trench Defenders)", "1/112 Saltpetre · 1/112 Tallow Balm · 1/112 Damp Rag · Abundant in trenches!")
steps_3 = [
    ("Navigate to Northwest Outpost (X: 1086, Y: 1299): ", "Interact with Tactical Map & scout Gunline Fort (completes Q5)."),
    ("Sweep trenches & graves for Q6 Pre-Farm items: ", "Gather 20x Saltpetre, 5x Damp Rags, and 10x Tallow Balm.")
]
post_3 = [
    ("Extract through your active match exit gate: ", "Return to Château Outer Ramparts."),
    ("TRIPLE TURN-IN at Château: ", "Hand in Q5 -> INSTANT TURN-IN Q6 (Saltpetre/Rag/Balm) -> Talk to Mr Sweet (Q7 complete)!")
]

img3 = build_visual_infographic(sarlat_raw, 3, "Sarlat Farm · Gunline & Pre-Farm", "Sarlat Farm", "Mapping the Front", "KEYS: NONE NEEDED (KEEP IN STASH)", (16, 185, 129), pins_3, route_3, steps_3, items_3, conts_3, mob_3, post_3)
img3.save(os.path.join(OUT_DIR, 'raid3_map.jpg'), quality=92)

# ================= RAID 4: Sarlat Farm (The Red Candle) =================
print("Rendering Visual Raid 4...")
pins_4 = [
    {'x': 3034, 'y': 2516, 'label': 'CHAPEL OF WEEPING VIRGINS', 'sublabel': 'PRIMARY: Red Votive Candle on Altar (100%)', 'color': (239, 68, 68), 'num': '1'},
    {'x': 2754, 'y': 2172, 'label': 'PARSONAGE RECTORY', 'sublabel': 'Wall Cabinets (16.1% China Bowl) & Bullion Boxes', 'color': (6, 182, 212), 'num': '2'},
    {'x': 3300, 'y': 2800, 'label': 'GRAVEYARD CEMETERY', 'sublabel': 'Graveyard Brute: China Bowl & Opium Pipe drop (1/226)', 'color': (244, 63, 94), 'num': '3'}
]
items_4 = [
    {'name': 'Red Votive Candle', 'count': '1x ALTAR', 'icon_path': os.path.join(ITEM_DIR, 'votive_candle.png'), 'desc': 'Primary Story Quest 8. Spawns physically on chapel altar ONLY during active Q8!'},
    {'name': 'China Bowl (Bribery Final)', 'count': '1x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'china_bowl.png'), 'desc': 'Check parsonage wall cabinets & tables if you still need it for Mr Sweet.'},
    {'name': 'Opium Pipe (Bribery Final)', 'count': '1x NEEDED', 'icon_path': os.path.join(ITEM_DIR, 'opium_pipe.png'), 'desc': 'Check rectory bullion lockboxes if you still need it for Mr Sweet.'}
]
conts_4 = [
    {'name': 'Chapel Altar', 'chance': '100% Guaranteed Spawn', 'icon_path': os.path.join(CONT_DIR, 'stone_grave.webp'), 'note': 'Loot candle directly off church altar inside Chapel ruins.'},
    {'name': 'Wall Cabinet', 'chance': '16.1% (1 in 6.2) China Bowl', 'icon_path': os.path.join(CONT_DIR, 'wall_cabinet.webp'), 'note': 'Inside church rectory quarters. Final chance before Mount Sinai.'},
    {'name': 'Bullion Box', 'chance': '13.7% (1 in 7.3) Opium Pipe', 'icon_path': os.path.join(CONT_DIR, 'bullion_box.webp'), 'note': 'Inside church quarters lockbox. Final chance before Mount Sinai.'}
]
mob_4 = ("Graveyard Brute", "1/226 China Bowl & Opium Pipe fallback · Roams directly outside the Chapel.")
steps_4 = [
    ("Navigate directly to Chapel ruins (X: 3034, Y: 2516): ", "Infiltrate church interior and take Red Votive Candle from altar."),
    ("Ensure 1x China Bowl, 1x Pipe, 1x Opium are ready: ", "Check parsonage lockboxes if missing any Bribery items.")
]
post_4 = [
    ("Extract via your active match exit gate: ", "Return to Château Outer Ramparts."),
    ("UNLOCK MOUNT SINAI (DOUBLE TURN-IN): ", "Hand in Candle to Eloise (Q8 complete) -> Turn in Bribery items to Mr Sweet -> Unlocks Quest 9!")
]

img4 = build_visual_infographic(sarlat_raw, 4, "Sarlat Farm · The Red Candle", "Sarlat Farm", "Pushing Back the Shadows", "KEYS: NONE NEEDED (KEEP IN STASH)", (16, 185, 129), pins_4, [], steps_4, items_4, conts_4, mob_4, post_4)
img4.save(os.path.join(OUT_DIR, 'raid4_map.jpg'), quality=92)

# ================= RAID 5: Sarlat Farm (Mount Sinai Part 1) =================
print("Rendering Visual Raid 5...")
pins_5 = [
    {'x': 2446, 'y': 1550, 'label': 'BOOK 1: CENSUS OF 1806', 'sublabel': 'Town Registry Office (Open Room · Desk)', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1259, 'y': 1065, 'label': "BOOK 2: ROZIER'S AGRICULTURE", 'sublabel': 'Master Granary (Open Room · Ledger Desk)', 'color': (245, 158, 11), 'num': '2'},
    {'x': 3048, 'y': 2488, 'label': 'BOOK 3: CATECHISME 1567', 'sublabel': 'Church Library Annex (Open Room · Lectern)', 'color': (245, 158, 11), 'num': '3'}
]
route_5 = [(1259, 1065), (2446, 1550), (3048, 2488)]
items_5 = [
    {'name': 'Census of 1806', 'count': 'BOOK 1 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_census.png'), 'desc': 'Town Registry Office (X: 2446, Y: 1550). Sitting on open clerk desk.'},
    {'name': "Rozier's Agriculture", 'count': 'BOOK 2 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_rozier.png'), 'desc': 'Master Granary (X: 1259, Y: 1065). Sitting on open ledger desk.'},
    {'name': 'Catechisme of 1567', 'count': 'BOOK 3 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_catechisme.png'), 'desc': 'Church Library Annex (X: 3048, Y: 2488). Sitting on open stone lectern.'}
]
conts_5 = [
    {'name': 'Open Desks & Lecterns', 'chance': '100% Guaranteed Physical Spawn', 'icon_path': os.path.join(CONT_DIR, 'ledger_desk.webp'), 'note': 'ZERO KEYS NEEDED on Sarlat Farm! All 3 books are in 100% open rooms.'},
    {'name': 'Secure Pouch Storage', 'chance': 'Store All 3 Books in Pouch', 'icon_path': os.path.join(CONT_DIR, 'strongbox.webp'), 'note': 'Guarantees books are not dropped or lost if eliminated.'}
]
mob_5 = ("Iron Shambler & Village Dregs", "Roam roads between granary & church · Kill for extra ammunition.")
steps_5 = [
    ("Loot Books 1, 2, and 3 in whichever order is closest: ", "Town Registry -> Master Granary -> Church Library Annex."),
    ("Store all 3 books inside your secure pouch: ", "All 3 rooms are open: do not bring Silver or Gold keys on this raid!")
]
post_5 = [
    ("Extract via your active match exit gate: ", "Return safely to Château Outer Ramparts."),
    ("DEPOSIT 3 BOOKS IN STASH & EQUIP SILVER KEY: ", "Move Books 1-3 to Stash -> Put 1x Silver Key in pouch for Raid 6!")
]

img5 = build_visual_infographic(sarlat_raw, 5, "Sarlat Farm · Mount Sinai (Books 1, 2, 3)", "Sarlat Farm", "Down From Mount Sinai", "KEYS: NONE NEEDED (KEEP IN STASH)", (16, 185, 129), pins_5, route_5, steps_5, items_5, conts_5, mob_5, post_5)
img5.save(os.path.join(OUT_DIR, 'raid5_map.jpg'), quality=92)

# ================= RAID 6: Jacques Bridge (Mount Sinai Part 2) =================
print("Rendering Visual Raid 6...")
pins_6 = [
    {'x': 1391, 'y': 1535, 'label': 'BOOK 4: THE SPIRIT OF THE LAWS', 'sublabel': "Judge's Quarters (Open Room · Bench)", 'color': (245, 158, 11), 'num': '1'},
    {'x': 2094, 'y': 1346, 'label': "BOOK 5: BUFFON'S NATURAL HISTORY", 'sublabel': 'REQUIRES SILVER KEY: High Court Archive Door', 'color': (6, 182, 212), 'num': '2'}
]
route_6 = [(1391, 1535), (2094, 1346)]
items_6 = [
    {'name': 'The Spirit of the Laws', 'count': 'BOOK 4 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_montesquieu.png'), 'desc': "Judge's Quarters (X: 1391, Y: 1535). Open courtroom room — no key needed."},
    {'name': 'Buffon’s Natural History', 'count': 'BOOK 5 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_buffon.png'), 'desc': 'High Court Archives (X: 2094, Y: 1346). LOCKED BEHIND SILVER KEY DOOR!'},
    {'name': 'Silver Key (Loadout)', 'count': 'BRING IN POUCH', 'icon_path': os.path.join(ITEM_DIR, 'silver_key.png'), 'desc': 'Bought from Louis at Château (12s 60c). Consumes key to open Book 5 door.'}
]
conts_6 = [
    {'name': 'Silver Key Archive Door', 'chance': 'MANDATORY: Requires Silver Key', 'icon_path': os.path.join(CONT_DIR, 'wall_cabinet.webp'), 'note': 'High Court Archives (X: 2094, Y: 1346). Door cannot be opened without key!'},
    {'name': "Judge's Quarters Bench", 'chance': '100% Guaranteed Physical Spawn', 'icon_path': os.path.join(CONT_DIR, 'ledger_desk.webp'), 'note': 'Open courtroom bench holding Book 4 (The Spirit of the Laws).'}
]
mob_6 = ("High Court Drooler & Dregs", "Defend court entrance · Clear before unlocking the Silver Key door.")
steps_6 = [
    ("VERIFY LOADOUT BEFORE QUEUEING: ", "Place 1x Silver Key (from Louis) into your secure pouch!"),
    ("Loot Book 4 in Judge's Quarters -> Unlock Archive for Book 5: ", "Open High Court Archive door with Silver Key and retrieve Book 5.")
]
post_6 = [
    ("Extract via your active match exit gate: ", "Return safely to Château Outer Ramparts."),
    ("DEPOSIT BOOKS 4 & 5 IN STASH & EQUIP GOLD KEY: ", "Move Books 4 & 5 to Stash -> Put 1x Gold Key in pouch for Raid 7!")
]

img6 = build_visual_infographic(bridge_raw, 6, "Jacques Bridge · Mount Sinai (Books 4 & 5)", "Jacques Bridge", "Down From Mount Sinai", "KEY REQUIRED: BRING SILVER KEY IN POUCH", (6, 182, 212), pins_6, route_6, steps_6, items_6, conts_6, mob_6, post_6)
img6.save(os.path.join(OUT_DIR, 'raid6_map.jpg'), quality=92)

# ================= RAID 7: Sombre Forest (Mount Sinai Part 3) =================
print("Rendering Visual Raid 7...")
pins_7 = [
    {'x': 2592, 'y': 2992, 'label': 'BOOK 6: CODEX MEDICAMENTARIUS', 'sublabel': 'Sanatorium Reception Desk (Open Room · No Key)', 'color': (245, 158, 11), 'num': '1'},
    {'x': 3168, 'y': 2405, 'label': 'BOOK 7: RONDELET ARCHITECTURE', 'sublabel': 'REQUIRES GOLD KEY: Command Bunker Steel Vault', 'color': (245, 158, 11), 'num': '2'}
]
route_7 = [(2592, 2992), (3168, 2405)]
items_7 = [
    {'name': 'Codex Medicamentarius', 'count': 'BOOK 6 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_mortuary.png'), 'desc': 'Sanatorium Reception Desk (X: 2592, Y: 2992). Open hospital hall — no key needed.'},
    {'name': 'Civil Architecture (Rondelet)', 'count': 'BOOK 7 OF 7', 'icon_path': os.path.join(ITEM_DIR, 'book_rondelet.png'), 'desc': 'Command Bunker Vault (X: 3168, Y: 2405). LOCKED BEHIND GOLD KEY VAULT!'},
    {'name': 'Gold Key (Loadout)', 'count': 'BRING IN POUCH', 'icon_path': os.path.join(ITEM_DIR, 'gold_key.png'), 'desc': 'Bought from Louis at Château (25s 60c). Consumes key to open steel vault door.'}
]
conts_7 = [
    {'name': 'Gold Key Steel Vault Door', 'chance': 'MANDATORY: Requires Gold Key', 'icon_path': os.path.join(CONT_DIR, 'strongbox.webp'), 'note': 'Fortified Command Bunker (X: 3168, Y: 2405). Cannot be opened without Gold Key!'},
    {'name': 'Sanatorium Desk', 'chance': '100% Guaranteed Physical Spawn', 'icon_path': os.path.join(CONT_DIR, 'ledger_desk.webp'), 'note': 'Open reception desk holding Book 6 (Codex Medicamentarius).'}
]
mob_7 = ("Bunker Brute & Pale Lady", "Patrol command bunker woods · Eliminate before unlocking the Gold Key vault.")
steps_7 = [
    ("VERIFY LOADOUT BEFORE QUEUEING: ", "Place 1x Gold Key (from Louis) into your secure pouch!"),
    ("Loot Book 6 in Sanatorium -> Unlock Bunker Vault for Book 7: ", "Open Command Bunker Steel Vault with Gold Key and take final book.")
]
post_7 = [
    ("Extract via your active match exit gate: ", "Final deployment complete! Return to Château Outer Ramparts."),
    ("HAND IN ALL 7 BOOKS & UNLOCK THE CAULDRON: ", "Hand in all 7 books to Eloise (Q9 complete) -> Speak to Prelate Castiel -> Cauldron Unlocked!")
]

img7 = build_visual_infographic(forest_raw, 7, "Sombre Forest · Mount Sinai (Books 6 & 7)", "Sombre Forest", "Down From Mount Sinai", "KEY REQUIRED: BRING GOLD KEY IN POUCH", (245, 158, 11), pins_7, route_7, steps_7, items_7, conts_7, mob_7, post_7)
img7.save(os.path.join(OUT_DIR, 'raid7_map.jpg'), quality=92)

print("All 7 ultra-visual infographics with real item & container icons generated successfully!")
