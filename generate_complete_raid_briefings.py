import os, sys
from PIL import Image, ImageDraw, ImageFont

MAP_DIR = r'C:\Users\PC\Documents\HungerHelper'
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
font_bold = ImageFont.truetype("arialbd.ttf", 18)
font_regular = ImageFont.truetype("arial.ttf", 17)
font_small = ImageFont.truetype("arial.ttf", 15)
font_pin_large = ImageFont.truetype("arialbd.ttf", 24)
font_pin_sub = ImageFont.truetype("arial.ttf", 18)

def draw_tactical_pin(draw, x, y, label, sublabel=None, color=(245, 158, 11), num="1"):
    # Target glow rings
    draw.ellipse([x-30, y-30, x+30, y+30], fill=(color[0], color[1], color[2], 50), outline=(color[0], color[1], color[2], 180), width=2)
    draw.ellipse([x-15, y-15, x+15, y+15], fill=color, outline=(255, 255, 255), width=3)
    
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
    
    box_w = max(tw + 24, 200)
    box_h = th + (26 if sublabel else 14)
    bx1 = x - box_w//2
    by1 = y + 20
    bx2 = x + box_w//2
    by2 = by1 + box_h
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=8, fill=(15, 23, 42, 240), outline=(color[0], color[1], color[2], 255), width=2)
    draw.text((x - tw//2, by1 + 6), text, font=font_pin_large, fill=(255, 255, 255))
    if sublabel:
        s_bbox = draw.textbbox((x, y), sublabel, font=font_pin_sub)
        s_tw = s_bbox[2] - s_bbox[0]
        draw.text((x - s_tw//2, by1 + th + 8), sublabel, font=font_pin_sub, fill=(203, 213, 225))

def draw_hud_card(draw, x, y, w, h, icon, title, lines, accent_color=(245, 158, 11)):
    # Panel background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=(18, 24, 38), outline=(38, 47, 65), width=1)
    # Header bar
    draw.rounded_rectangle([x, y, x+w, y+36], radius=10, fill=(24, 32, 50))
    draw.rectangle([x, y+24, x+w, y+36], fill=(24, 32, 50))
    draw.line([x, y+36, x+w, y+36], fill=accent_color, width=2)
    
    # Title
    draw.text((x+12, y+7), f"{icon}  {title}", font=font_card_h, fill=accent_color)
    
    # Content lines
    cur_y = y + 44
    for line in lines:
        if isinstance(line, tuple):
            prefix, text, subtext = line
            draw.text((x+14, cur_y), prefix, font=font_bold, fill=(255, 255, 255))
            pw = draw.textbbox((0, 0), prefix, font=font_bold)[2]
            draw.text((x+16+pw, cur_y), text, font=font_regular, fill=(226, 232, 240))
            if subtext:
                cur_y += 20
                draw.text((x+28, cur_y), subtext, font=font_small, fill=(148, 163, 184))
            cur_y += 24
        else:
            draw.text((x+14, cur_y), str(line), font=font_regular, fill=(203, 213, 225))
            cur_y += 22

def build_briefing_image(base_map, raid_num, title, map_name, quest_name, key_badge, key_color, pins, route_lines, cards, crop_box=None):
    canvas = Image.new('RGB', (2400, 1400), (10, 13, 20))
    
    # Map Crop & Fit
    map_layer = base_map.copy()
    if crop_box:
        map_crop = map_layer.crop(crop_box)
    else:
        map_crop = map_layer
    
    map_w, map_h = 1540, 1260
    map_fitted = map_crop.resize((map_w, map_h), Image.Resampling.LANCZOS)
    canvas.paste(map_fitted, (20, 120))
    
    d = ImageDraw.Draw(canvas, 'RGBA')
    d.rectangle([20, 120, 20+map_w, 120+map_h], outline=(51, 65, 85), width=2)
    
    scale_x = map_w / (crop_box[2] - crop_box[0] if crop_box else 4096)
    scale_y = map_h / (crop_box[3] - crop_box[1] if crop_box else 4096)
    offset_x = crop_box[0] if crop_box else 0
    offset_y = crop_box[1] if crop_box else 0
    
    def to_canvas(cx, cy):
        return (int(20 + (cx - offset_x) * scale_x), int(120 + (cy - offset_y) * scale_y))
    
    # Route lines
    if route_lines and len(route_lines) > 1:
        for i in range(len(route_lines)-1):
            p1 = to_canvas(route_lines[i][0], route_lines[i][1])
            p2 = to_canvas(route_lines[i+1][0], route_lines[i+1][1])
            d.line([p1, p2], fill=(245, 158, 11, 200), width=4)
    
    # Pins
    for pin in pins:
        px, py = to_canvas(pin['x'], pin['y'])
        draw_tactical_pin(d, px, py, pin['label'], pin.get('sublabel'), pin.get('color', (245, 158, 11)), pin.get('num', '★'))
    
    # Header Bar
    d.rectangle([0, 0, 2400, 105], fill=(15, 23, 42))
    d.line([0, 105, 2400, 105], fill=(245, 158, 11), width=3)
    header_title = f"RAID {raid_num} · {title.upper()}"
    d.text((30, 15), header_title, font=font_title, fill=(255, 255, 255))
    d.text((32, 62), f"DEPLOY MAP: {map_name.upper()}   |   STORY QUEST: {quest_name.upper()}", font=font_card_h, fill=(203, 213, 225))
    
    # Key Badge
    kb_w = d.textbbox((0, 0), key_badge, font=font_card_h)[2] + 40
    kb_x = 2360 - kb_w
    d.rounded_rectangle([kb_x, 24, 2360, 80], radius=8, fill=(key_color[0], key_color[1], key_color[2], 40), outline=key_color, width=2)
    d.text((kb_x + 20, 38), key_badge, font=font_card_h, fill=key_color)
    
    # Right Briefing Sidebar (Width 800px: x = 1580 to 2380)
    card_x = 1580
    card_w = 800
    card_y = 120
    
    for c in cards:
        draw_hud_card(d, card_x, card_y, card_w, c['h'], c['icon'], c['title'], c['lines'], c.get('color', (245, 158, 11)))
        card_y += c['h'] + 14
        
    return canvas

# ================= RAID 1: Sarlat Farm (Making Dough) =================
print("Rendering Raid 1 infographic...")
pins_1 = [
    {'x': 1800, 'y': 3400, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'South Perimeter', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 2500, 'y': 2100, 'label': 'SARLAT VILLAGE GRANARIES', 'sublabel': 'Primary: 20x Flour & Ash Piles', 'color': (16, 185, 129), 'num': '1'},
    {'x': 3756, 'y': 3530, 'label': 'ESTATE BRICK RESIDENCES', 'sublabel': 'China Bowl & 81 Table Spawns', 'color': (6, 182, 212), 'num': '2'},
    {'x': 3500, 'y': 3800, 'label': 'PERIMETER GATE EXTRACTION', 'sublabel': 'Safe Return to Château', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_1 = [(1800, 3400), (2500, 2100), (3756, 3530), (3500, 3800)]
cards_1 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Flour Sacks & Barrels: ", "Collect 20x Flour in Sarlat Village farmhouses.", "Finish in a single run: 597 flour sacks and 758 barrels on map."),
            ("2. Hearth Pre-Farm: ", "Loot all fireplaces for 15x Charcoal (Pile of Ash 52.6%).", "Hold in stash for instant turn-in on Quest 4!"),
            ("3. Bribery Pre-Farm: ", "Check estate wall cabinets and dressers for 1x China Bowl.", "16.1% in cabinets; 13 fixed loose table spawns on Sarlat.")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'HIGH-DENSITY CONTAINERS (EXACT ODDS)', 'color': (16, 185, 129),
        'lines': [
            ("Flour Sack: ", "47.6% (1 in 2.1) Flour", "597 spots on Sarlat. Highest odds food container."),
            ("Oak Barrel: ", "38.5% (1 in 2.6) Flour & Saltpetre", "758 spots on map. Huge density along roads & barns."),
            ("Pile of Ash: ", "52.6% (1 in 1.9) Charcoal", "85 hearth/stove spots. Guarantees 15x Charcoal in 1 raid."),
            ("Wall Cabinet: ", "16.1% (1 in 6.2) China Bowl", "7 global spots inside brick estate houses (bribery item).")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Dreg Military / Voltigeur: ", "1/112 Flour, Saltpetre, Damp Rag, Balm", "Patrols road checkpoints and village entrances."),
            ("Iron Shambler & Shambler: ", "1/72 (1.39%) Charcoal Drop", "Roams country lanes. Iron Shamblers have highest Charcoal odds!"),
            ("Bloat: ", "1/92 (1.09%) Charcoal Drop", "Roaming swollen corpses near farm ditches.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Silver Key (81 Fixed Table Spots): ", "1/52 (1.92%) Loose Spawn", "Placed on desks, nightstands & shelves across Sarlat Farm!"),
            ("Gold Key (81 Fixed Table Spots): ", "1/262 (0.38%) Loose Spawn", "Can spawn directly on same 81 tables in farmhouses."),
            ("China Bowl (13 Fixed House Spots): ", "1/344 (0.29%) Loose Spawn", "Direct table pickups inside village living rooms.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT', 'color': (168, 85, 247),
        'lines': [
            ("KEY LOADOUT: ", "BRING ZERO KEYS ON THIS RAID!", "Keep Silver & Gold keys safe in stash so you cannot lose them."),
            ("Louis (Stashmaster): ", "Check Silver Key (12s 60c) & Gold Key (25s 60c).", "Louis has 17.7% Silver / 8.8% Gold restock chance after every raid!"),
            ("Octave de Villiers: ", "Buy Burlap Haversack / Damp Knapsack.", "Upgrades your inventory carry capacity for pre-farm loot.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID TURN-IN SEQUENCE', 'color': (245, 158, 11),
        'lines': [
            ("Extract via Perimeter Gate: ", "Return to Château Outer Ramparts.", "Ensure 20x Flour and pre-farmed items are in your bag."),
            ("Hand in Quest 2 (Making Dough): ", "Give 20x Flour to Eloise.", "Unlocks Quest 3: The Gavroche Family!"),
            ("Stash Management: ", "Deposit 15x Charcoal & China Bowl into Stash.", "Do NOT carry them into Raid 2!")
        ]
    }
]
img1 = build_briefing_image(sarlat_raw, 1, "Sarlat Farm · Village Recon", "Sarlat Farm", "Making Dough", "[BRING NO KEYS · KEEP SAFE IN STASH]", (16, 185, 129), pins_1, route_1, cards_1, crop_box=(400, 1500, 4000, 4050))
img1.save(os.path.join(OUT_DIR, 'raid1_map.jpg'), quality=90)

# ================= RAID 2: Jacques Bridge (Gavroche Family) =================
print("Rendering Raid 2 infographic...")
pins_2 = [
    {'x': 500, 'y': 1800, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'West Bridge Span', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 1479, 'y': 313, 'label': 'GAVROCHE FAMILY CAMP', 'sublabel': 'Primary: Instant Quest Trigger', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1044, 'y': 2660, 'label': "JACQUE'S MEDICINALS", 'sublabel': 'CRUCIAL: 1x Opium (47.6%) & Bowl', 'color': (6, 182, 212), 'num': '2'},
    {'x': 2100, 'y': 1500, 'label': 'ADMINISTRATIVE BLOCK', 'sublabel': 'Ledger Desks: 34.5% Silver Key', 'color': (168, 85, 247), 'num': '3'},
    {'x': 3800, 'y': 2000, 'label': 'EAST BRIDGE GATE EXTRACTION', 'sublabel': 'Safe Return to Château', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_2 = [(500, 1800), (1479, 313), (1044, 2660), (2100, 1500), (3800, 2000)]
cards_2 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Gavroche Camp: ", "Walk into camp at X: 1479, Y: 313.", "Discovery triggers instant Quest 3 completion!"),
            ("2. Jacque's Medicinals: ", "Loot clinic container at X: 1044, Y: 2660.", "47.6% Opium & 11.2% China Bowl/Opium Pipe (Bribery item)."),
            ("3. Elite Mob Hunting: ", "Kill Brutes on road for Opium (1/52) & Silver Key (1/69).", "High-Class Dregs in tollhouses also drop Opium at 1/85!")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'HIGH-DENSITY CONTAINERS (EXACT ODDS)', 'color': (16, 185, 129),
        'lines': [
            ("Jacque's Medicinals: ", "47.6% Opium · 11.2% China Bowl & Pipe", "Unique container! Single best spot in game for Bribery items."),
            ("Bullion / Jewellery Box: ", "13.7% (1 in 7.3) Opium Pipe", "119 spots combined across residential bridge rooms."),
            ("Ledger Desk / Cabinet: ", "34.5% (1 in 2.9) Silver Key", "73 spots in bridge offices. Best non-vendor Silver Key odds!"),
            ("Old Cabinet / Bucket: ", "15.4% / 14.3% Damp Rag", "Fallback containers in bridge tenement rooms.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Brute & Drooler (Heavy Mobs): ", "1/52 (1.92%) Opium · 1/69 (1.45%) Silver Key", "Top target! Also drops China Bowl & Pipe at 1/226 each."),
            ("High-Class Dreg: ", "1/85 (1.18%) Opium · 1/420 China Bowl", "Inside tollhouses and administrative quarters."),
            ("Shambler & Bloat: ", "1/72 Shambler · 1/92 Bloat Charcoal", "Roaming under bridge arches.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Silver Cutlery & Valuables: ", "Check tollhouse and office desks.", "High silver coin value for buying Louis's keys."),
            ("Tollhouse Loose Desks: ", "Can spawn loose keys and medical vials.", "Inspect all office surfaces on lower and upper bridge deck.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT', 'color': (168, 85, 247),
        'lines': [
            ("KEY LOADOUT: ", "ZERO KEYS REQUIRED TO COMPLETE QUEST!", "If Louis sold Silver Key (12s 60c), keep it in safe stash."),
            ("Piro (Physician): ", "Buy 1-2 Robust Antidotes.", "Jacques Bridge has dangerous chemical gas zones!"),
            ("Reynauld: ", "Top up Heavy & Medium ammunition.", "Essential for taking down Brutes and Droolers.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID CHAIN (DOUBLE TURN-IN)', 'color': (245, 158, 11),
        'lines': [
            ("Extract via East Gate: ", "Return to Château Outer Ramparts.", "Ensure Opium & Bribery items are securely stored."),
            ("Hand in Quest 3 (The Gavroche Family): ", "Turn in camp report to Eloise.", "Quest 3 Completed!"),
            ("INSTANT TURN-IN Quest 4 (Last Embers): ", "Give pre-farmed 15x Charcoal to Eloise!", "Quest 4 Completed instantly! Unlocks Quest 5: Mapping Front!")
        ]
    }
]
img2 = build_briefing_image(bridge_raw, 2, "Jacques Bridge · Gavroche & Medicinals", "Jacques Bridge", "The Gavroche Family", "[ZERO KEYS MANDATORY · CHECK SILVER KEY]", (6, 182, 212), pins_2, route_2, cards_2, crop_box=(200, 100, 4000, 3600))
img2.save(os.path.join(OUT_DIR, 'raid2_map.jpg'), quality=90)

# ================= RAID 3: Sarlat Farm (Mapping the Front) =================
print("Rendering Raid 3 infographic...")
pins_3 = [
    {'x': 600, 'y': 3200, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'Southwest Approach', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 1086, 'y': 1299, 'label': 'TACTICAL MAP OUTPOST', 'sublabel': 'Primary: Interact with Map', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1196, 'y': 1315, 'label': 'GUNLINE FORTIFICATION', 'sublabel': 'Primary: Scout Fort Perimeter', 'color': (245, 158, 11), 'num': '2'},
    {'x': 3587, 'y': 3627, 'label': 'ARTILLERY TRENCHES & GRAVES', 'sublabel': 'Pre-Farm: 20x Saltpetre & Rags', 'color': (16, 185, 129), 'num': '3'},
    {'x': 500, 'y': 1200, 'label': 'NORTHWEST EXTRACTION', 'sublabel': 'Return to Château', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_3 = [(600, 3200), (1086, 1299), (1196, 1315), (3587, 3627), (500, 1200)]
cards_3 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Tactical Map: ", "Interact with military map on desk at X: 1086, Y: 1299.", "Completes first scout objective."),
            ("2. Gunline Fort: ", "Approach the artillery gunline fortifications (X: 1196, Y: 1315).", "Scouting perimeter triggers Quest 5 completion!"),
            ("3. Trench Pre-Farm Q6: ", "Loot 20x Saltpetre, 5x Damp Rags, 10x Tallow Balm.", "Enables immediate instant turn-in of Quest 6 after extracting!")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'HIGH-DENSITY CONTAINERS (EXACT ODDS)', 'color': (16, 185, 129),
        'lines': [
            ("Tooling Bin: ", "18.9% (1 in 5.3) Saltpetre", "41 spots inside artillery trenches and bunker workshops."),
            ("Stone Grave: ", "23.8% (1 in 4.2) Damp Rag", "40 spots in churchyard & battlefield ditch burials."),
            ("Basket / Jacket: ", "13.3% / 11.5% Damp Rag", "237 fallback containers along the front lines."),
            ("Physician Bag / Medical Chest: ", "6.7% (1 in 15) Tallow Balm", "98 spots across field medical tents and hospital annexes.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Dreg Military (Trench Defenders): ", "1/112 Saltpetre · 1/112 Balm · 1/112 Rag", "Abundant around Gunline Fort. Kill every soldier on sight!"),
            ("Waif (Scavenger): ", "1/112 Damp Rag · 1/112 Saltpetre", "Lurking inside bomb craters and mud trenches."),
            ("Iron Shambler: ", "1/72 Charcoal", "Stalking road margins.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Silver Key (81 Fixed Table Spots): ", "1/52 (1.92%) Loose Spawn", "Check command bunker tables next to the Tactical Map!"),
            ("Gold Key (81 Fixed Table Spots): ", "1/262 (0.38%) Loose Spawn", "Same 81 fixed spots. Always inspect desks before leaving."),
            ("China Bowl (13 Spots): ", "1/344 Loose Spawn", "Check ruined farmhouses.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT', 'color': (168, 85, 247),
        'lines': [
            ("KEY LOADOUT: ", "BRING ZERO KEYS ON THIS RAID!", "Keep Silver & Gold keys safely stored in your Château stash."),
            ("Piro (Physician): ", "Buy starter bandages and ampoules.", "Trench warfare has frequent bleeding damage."),
            ("Louis: ", "Check vendor shop for Silver Key & Gold Key.", "Buy immediately if available so you are set for Raids 6 & 7.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID CHAIN (TRIPLE TURN-IN)', 'color': (245, 158, 11),
        'lines': [
            ("Extract via Northwest Gate: ", "Return to Château Outer Ramparts.", "Ensure 20x Saltpetre, 5x Rags, 10x Balm in inventory."),
            ("Hand in Quest 5 (Mapping the Front): ", "Turn in scouting report to Eloise.", "Quest 5 Complete!"),
            ("INSTANT TURN-IN Quest 6 & 7: ", "Turn in 20x Saltpetre/5x Rag/10x Balm to Eloise (Q6) -> Speak to Mr Sweet (Q7)!", "Quest 6 & 7 Completed without deploying! Unlocks Quest 8!")
        ]
    }
]
img3 = build_briefing_image(sarlat_raw, 3, "Sarlat Farm · Gunline & Trench Recon", "Sarlat Farm", "Mapping the Front", "[BRING NO KEYS · KEEP SAFE IN STASH]", (16, 185, 129), pins_3, route_3, cards_3, crop_box=(400, 800, 3900, 3900))
img3.save(os.path.join(OUT_DIR, 'raid3_map.jpg'), quality=90)

# ================= RAID 4: Sarlat Farm (The Red Candle) =================
print("Rendering Raid 4 infographic...")
pins_4 = [
    {'x': 2000, 'y': 3700, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'South Woods Trail', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 3034, 'y': 2516, 'label': 'CHAPEL OF WEEPING VIRGINS', 'sublabel': 'LOOT: Red Votive Candle on Altar', 'color': (239, 68, 68), 'num': '1'},
    {'x': 2754, 'y': 2172, 'label': 'PARSONAGE LOCKBOXES', 'sublabel': 'Last Chance: Opium Pipe (13.7%) & Bowl', 'color': (6, 182, 212), 'num': '2'},
    {'x': 3300, 'y': 2800, 'label': 'GRAVEYARD PERIMETER', 'sublabel': 'Kill Brute: 1/69 Silver Key', 'color': (244, 63, 94), 'num': '3'},
    {'x': 3800, 'y': 2800, 'label': 'EAST CHURCHYARD EXTRACTION', 'sublabel': 'Extract to Château', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_4 = [(2000, 3700), (3034, 2516), (2754, 2172), (3300, 2800), (3800, 2800)]
cards_4 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Chapel Altar: ", "Infiltrate Chapel ruins (X: 3034, Y: 2516) & loot Red Votive Candle.", "Spawns physically ONLY now that Quest 8 is active!"),
            ("2. Finalize Bribery Items: ", "Ensure you have 1x China Bowl, 1x Opium Pipe, 1x Opium.", "Search parsonage wall cabinets and bullion strongboxes."),
            ("3. Graveyard Brute Kill: ", "Eliminate the Brute outside chapel for Silver Key (1/69).", "Great fallback if Louis has not sold Silver Key yet.")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'HIGH-DENSITY CONTAINERS (EXACT ODDS)', 'color': (16, 185, 129),
        'lines': [
            ("Chapel Altar: ", "100% Guaranteed Red Votive Candle", "Spawns directly on the church altar during active Quest 8!"),
            ("Parsonage Wall Cabinet: ", "16.1% (1 in 6.2) China Bowl", "Inside church living quarters (last chance before Mount Sinai)."),
            ("Bullion / Jewellery Box: ", "13.7% (1 in 7.3) Opium Pipe", "Check rectory lockboxes for Mr Sweet's Bribery pipe."),
            ("Stone Grave: ", "23.8% Damp Rag", "Cemetery graves surrounding the chapel.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Graveyard Brute: ", "1/69 (1.45%) Silver Key · 1/226 China Bowl / Pipe", "Patrols around the chapel tombs. High-yield kill!"),
            ("Dreg Military: ", "1/112 Damp Rag · 1/112 Tallow Balm", "Guarding the stone cemetery boundary walls."),
            ("Shamblers & Bloats: ", "1/72 & 1/92 Charcoal", "Wandering in the misty churchyard.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Parsonage Table: ", "1/344 Loose China Bowl Spawn", "Inspect the parsonage dining table and dresser."),
            ("Chapel Lectern / Benches: ", "Can spawn loose Silver Key (1/52).", "Scan church benches while grabbing the altar candle.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT', 'color': (168, 85, 247),
        'lines': [
            ("KEY LOADOUT: ", "KEEP ALL KEYS SAFE IN STASH!", "Do not risk Silver or Gold key until Mount Sinai."),
            ("Louis: ", "Silver Key (12s 60c) & Gold Key (25s 60c).", "Make sure you own 1x Silver Key for Raid 6 and 1x Gold Key for Raid 7!"),
            ("Mr Sweet: ", "Check that you have Bribery items ready.", "1x China Bowl, 1x Opium Pipe, 1x Opium.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID CHAIN (UNLOCK MOUNT SINAI)', 'color': (245, 158, 11),
        'lines': [
            ("Extract via Churchyard Gate: ", "Return safely to Château Outer Ramparts.", "Ensure Red Votive Candle is in inventory."),
            ("Hand in Quest 8: ", "Give Red Votive Candle to Eloise.", "Quest 8 Complete!"),
            ("INSTANT TURN-IN A Touch of Bribery: ", "Hand in China Bowl, Opium Pipe, Opium to Mr Sweet!", "Bribery Complete! Unlocks Quest 9: Down From Mount Sinai!")
        ]
    }
]
img4 = build_briefing_image(sarlat_raw, 4, "Sarlat Farm · The Chapel Altar", "Sarlat Farm", "Pushing Back the Shadows", "[ACTIVE QUEST ONLY · CANDLE AT ALTAR]", (239, 68, 68), pins_4, route_4, cards_4, crop_box=(1800, 1500, 4000, 3900))
img4.save(os.path.join(OUT_DIR, 'raid4_map.jpg'), quality=90)

# ================= RAID 5: Sarlat Farm (Mount Sinai Part 1) =================
print("Rendering Raid 5 infographic...")
pins_5 = [
    {'x': 1800, 'y': 3300, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'South River Trail', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 2446, 'y': 1550, 'label': 'BOOK 1: CENSUS OF 1806', 'sublabel': 'Town Registry Office (Open Room)', 'color': (245, 158, 11), 'num': '1'},
    {'x': 1259, 'y': 1065, 'label': "BOOK 2: ROZIER'S AGRICULTURE", 'sublabel': 'Master Granary Ledger (Open Room)', 'color': (245, 158, 11), 'num': '2'},
    {'x': 3048, 'y': 2488, 'label': 'BOOK 3: CATECHISME 1567', 'sublabel': 'Church Library Lectern (Open Room)', 'color': (245, 158, 11), 'num': '3'},
    {'x': 3800, 'y': 1500, 'label': 'RIVER EXTRACTION', 'sublabel': 'Extract with 3 Books in Pouch', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_5 = [(1800, 3300), (2446, 1550), (1259, 1065), (3048, 2488), (3800, 1500)]
cards_5 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Book 1 (Census of 1806): ", "Town Registry Office desk at X: 2446, Y: 1550.", "Sitting on open town clerk table."),
            ("2. Book 2 (Rozier's Agriculture): ", "Master Granary ledger desk at X: 1259, Y: 1065.", "Inside the large central granary office."),
            ("3. Book 3 (Catechisme of 1567): ", "Church Library Annex lectern at X: 3048, Y: 2488.", "Inside the stone library room adjacent to church.")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'KEYED ACCESS & CONTAINER RULES', 'color': (16, 185, 129),
        'lines': [
            ("ZERO KEYS NEEDED ON SARLAT: ", "All 3 books are in 100% open accessible rooms!", "Do not waste keys. No lockpicks required."),
            ("Quest 9 Active Requirement: ", "These 3 historical tomes only spawn now!", "Will not exist if Quest 9 is not yet active."),
            ("Secure Pouch Storage: ", "Store all 3 books inside your secure pouch.", "Guarantees books are not lost if killed."),
            ("General Loot Barrels: ", "758 barrels on map if you need extra food/ammo.", "Speed is priority: grab books and extract.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Iron Shambler & Shambler: ", "1/72 (1.39%) Charcoal Drop", "Roams country roads near granary and registry."),
            ("Dreg Military: ", "1/112 Ammo & Medical supplies", "Guards village crossroads and perimeter."),
            ("Bloat: ", "1/92 Charcoal Drop", "Swollen corpses in drainage ditches.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Registry & Granary Desks: ", "81 fixed table spots for Silver Key (1/52) & Gold Key (1/262).", "Check the exact desks where Book 1 and Book 2 sit!"),
            ("Church Annex Shelves: ", "Scan bookshelves for silver candleholders and coins.", "Valuable loot while picking up Book 3.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT', 'color': (168, 85, 247),
        'lines': [
            ("KEY LOADOUT WARNING: ", "DO NOT BRING SILVER OR GOLD KEY!", "Keep both keys safe in your Château stash so you cannot drop them."),
            ("Octave de Villiers: ", "Equip Burlap Haversack / Damp Knapsack.", "Ensures 3 book slots take minimal main bag room."),
            ("Verify Keys in Stash: ", "Check that 1x Silver Key is ready for Raid 6.", "If missing, buy from Louis (12s 60c).")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID CHAIN', 'color': (245, 158, 11),
        'lines': [
            ("Extract via River Crossing: ", "Return to Château Outer Ramparts.", "Ensure Books 1, 2, and 3 are intact."),
            ("Stash 3 Books: ", "Deposit Books 1, 2, 3 into your Château Stash.", "Do NOT carry them into Raid 6!"),
            ("PREPARE FOR RAID 6: ", "MOVE 1x SILVER KEY FROM STASH INTO SECURE POUCH!", "Mandatory requirement for unlocking Book 5 on Jacques Bridge!")
        ]
    }
]
img5 = build_briefing_image(sarlat_raw, 5, "Sarlat Farm · Mount Sinai (Books 1, 2, 3)", "Sarlat Farm", "Down From Mount Sinai", "[NO KEYS NEEDED · KEEP KEYS IN STASH]", (16, 185, 129), pins_5, route_5, cards_5, crop_box=(800, 800, 4000, 3500))
img5.save(os.path.join(OUT_DIR, 'raid5_map.jpg'), quality=90)

# ================= RAID 6: Jacques Bridge (Mount Sinai Part 2) =================
print("Rendering Raid 6 infographic...")
pins_6 = [
    {'x': 1000, 'y': 1600, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'West Span Approach', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 1391, 'y': 1535, 'label': 'BOOK 4: THE SPIRIT OF THE LAWS', 'sublabel': "Judge's Quarters Bench (Open Room)", 'color': (245, 158, 11), 'num': '1'},
    {'x': 2094, 'y': 1346, 'label': "BOOK 5: BUFFON'S NATURAL HISTORY", 'sublabel': 'REQUIRES SILVER KEY: High Court Door', 'color': (6, 182, 212), 'num': '2'},
    {'x': 3800, 'y': 2000, 'label': 'EAST BRIDGE GATE EXTRACTION', 'sublabel': 'Extract with Books 4 & 5', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_6 = [(1000, 1600), (1391, 1535), (2094, 1346), (3800, 2000)]
cards_6 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Book 4 (Montesquieu): ", "Judge's Quarters bench at X: 1391, Y: 1535.", "Inside open municipal administrative quarters."),
            ("2. Book 5 (Buffon): ", "High Court Archives at X: 2094, Y: 1346.", "LOCKED DOOR: Requires 1x SILVER KEY to unlock and loot!"),
            ("3. East Bridge Gate: ", "Extract with Books 4 & 5 stored in your secure pouch.", "Return safely to Château Outer Ramparts.")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'KEYED ACCESS & CONTAINER RULES', 'color': (6, 182, 212),
        'lines': [
            ("MANDATORY SILVER KEY DOOR: ", "High Court Archive Door (X: 2094, Y: 1346)", "Cannot be opened without Silver Key! Consumes/uses key."),
            ("Book 4 Open Access: ", "The Spirit of the Laws is in an open courtroom.", "No key needed for Book 4."),
            ("High Court Lockers: ", "Inside archive contains rare silver cutlery & jewelry.", "Search cabinets after retrieving Book 5."),
            ("Pouch Security: ", "Keep Silver Key in pouch until at the door.", "Keep books in pouch after looting.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("High Court Brute & Drooler: ", "1/69 (1.45%) Silver Key · 1/52 Opium", "Guards court perimeter. Emergency fallback if Silver Key lost!"),
            ("High-Class Dreg: ", "1/85 Opium · 1/420 China Bowl", "Inside municipal corridors and judge's chambers."),
            ("Voltigeur: ", "1/282 Heavy ammunition & components", "Sniping from upper bridge balconies.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Judge's Court Benches: ", "Can spawn silver candlesticks and loose silver.", "Grab while picking up Book 4."),
            ("High Court Archive Tables: ", "Behind locked door: check all desk surfaces.", "High silver coin yields.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT (CRUCIAL)', 'color': (168, 85, 247),
        'lines': [
            ("LOADOUT CHECK: ", "BRING 1x SILVER KEY IN YOUR POUCH!", "Do NOT deploy without verifying Silver Key is in your inventory!"),
            ("Louis: ", "If missing Silver Key, buy from Louis (12s 60c).", "Louis has 17.7% stock chance. Check shop before queuing."),
            ("KEEP GOLD KEY IN STASH: ", "Do NOT bring Gold Key into Raid 6!", "Keep Gold Key safe in stash for Raid 7.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'POST-RAID CHAIN', 'color': (245, 158, 11),
        'lines': [
            ("Extract via East Gate: ", "Return to Château Outer Ramparts.", "Ensure Books 4 and 5 are in your secure pouch."),
            ("Stash Books: ", "Deposit Books 4 & 5 into Château Stash.", "You now possess 5 of 7 historical books!"),
            ("PREPARE FOR RAID 7: ", "MOVE 1x GOLD KEY FROM STASH INTO SECURE POUCH!", "Mandatory requirement for unlocking Book 7 in Sombre Forest!")
        ]
    }
]
img6 = build_briefing_image(bridge_raw, 6, "Jacques Bridge · Mount Sinai (Books 4 & 5)", "Jacques Bridge", "Down From Mount Sinai", "[MANDATORY: BRING SILVER KEY IN POUCH]", (6, 182, 212), pins_6, route_6, cards_6, crop_box=(800, 200, 3900, 2500))
img6.save(os.path.join(OUT_DIR, 'raid6_map.jpg'), quality=90)

# ================= RAID 7: Sombre Forest (Mount Sinai Part 3) =================
print("Rendering Raid 7 infographic...")
pins_7 = [
    {'x': 1800, 'y': 1800, 'label': 'DEPLOYMENT ZONE', 'sublabel': 'North Woods Trail', 'color': (59, 130, 246), 'num': 'START'},
    {'x': 2592, 'y': 2992, 'label': 'BOOK 6: CODEX MEDICAMENTARIUS', 'sublabel': 'Sanatorium Desk (Open Room)', 'color': (245, 158, 11), 'num': '1'},
    {'x': 3168, 'y': 2405, 'label': 'BOOK 7: RONDELET ARCHITECTURE', 'sublabel': 'REQUIRES GOLD KEY: Bunker Steel Vault', 'color': (245, 158, 11), 'num': '2'},
    {'x': 1000, 'y': 3500, 'label': 'SOUTH FOREST EXTRACTION', 'sublabel': 'Final Extract! Return to Château', 'color': (244, 63, 94), 'num': 'EXTRACT'}
]
route_7 = [(1800, 1800), (2592, 2992), (3168, 2405), (1000, 3500)]
cards_7 = [
    {
        'h': 160, 'icon': '🎯', 'title': 'MISSION OBJECTIVES & ROUTE', 'color': (245, 158, 11),
        'lines': [
            ("1. Book 6 (Codex Medicamentarius): ", "Sanatorium reception desk at X: 2592, Y: 2992.", "Inside open abandoned hospital reception hall."),
            ("2. Book 7 (Rondelet Architecture): ", "Fortified Command Bunker at X: 3168, Y: 2405.", "LOCKED STEEL VAULT: Requires 1x GOLD KEY to unlock and loot!"),
            ("3. Final Extraction: ", "Extract via South Forest Road with all remaining books.", "Final deployment of Eloise's questline!")
        ]
    },
    {
        'h': 215, 'icon': '📦', 'title': 'KEYED ACCESS & CONTAINER RULES', 'color': (245, 158, 11),
        'lines': [
            ("MANDATORY GOLD KEY STEEL VAULT: ", "Command Bunker Vault Door (X: 3168, Y: 2405)", "Cannot be opened without Gold Key! Consumes/uses key."),
            ("Book 6 Open Access: ", "Codex Medicamentarius is on an open desk.", "No key needed for Book 6 in Sanatorium."),
            ("Bunker Vault Chests: ", "Contains top-tier military weaponry and bullion.", "Loot all crates after retrieving Book 7."),
            ("Pouch Security: ", "Keep Gold Key in pouch until at the vault door.", "Place Book 7 in pouch immediately.")
        ]
    },
    {
        'h': 195, 'icon': '⚔️', 'title': 'CREATURE MOB TARGETS (KILL ON SIGHT)', 'color': (244, 63, 94),
        'lines': [
            ("Bunker Brute & Drooler: ", "1/452 Gold Key · 1/69 Silver Key", "Fortified outside the command bunker entrance."),
            ("Pale Lady & Pitchskin: ", "1/2,691 Gold Key · 1/1,346 Pipe & Bowl", "Stalking the sawmill and sanatorium woods."),
            ("Iron Shambler: ", "1/72 Charcoal · 1/2,834 Gold Key", "Roaming along forest perimeter fences.")
        ]
    },
    {
        'h': 180, 'icon': '🔍', 'title': 'LOOSE WORLD LOOT (NO CONTAINERS NEEDED)', 'color': (6, 182, 212),
        'lines': [
            ("Sanatorium Mortuary Desks: ", "Inspect desks and mortuary tables for medical supplies.", "Check reception tables around Book 6."),
            ("Bunker Bunk Tables: ", "Inside Gold Key bunker: check all table surfaces.", "High military scrap and coin yields.")
        ]
    },
    {
        'h': 210, 'icon': '🗝️', 'title': 'HUB MERCHANTS & PRE-RAID LOADOUT (CRUCIAL)', 'color': (168, 85, 247),
        'lines': [
            ("LOADOUT CHECK: ", "BRING 1x GOLD KEY IN YOUR POUCH!", "Do NOT deploy without verifying Gold Key is in your inventory!"),
            ("Louis: ", "If missing Gold Key, buy from Louis (25s 60c).", "Louis has 8.8% Gold Key restock chance. Must have for Raid 7!"),
            ("Piro: ", "Buy extra bloodbags and antidotes.", "Sombre Forest has dangerous lurking beasts.")
        ]
    },
    {
        'h': 190, 'icon': '⚡', 'title': 'STORYLINE FINALE & CAULDRON UNLOCK', 'color': (16, 185, 129),
        'lines': [
            ("Extract via South Road: ", "Return safely to Château Outer Ramparts.", "Ensure Books 6 & 7 are securely in your pouch."),
            ("Hand in Quest 9 (Mount Sinai): ", "Hand in all 7 Historical Books to Eloise!", "Quest 9 Complete! +1,000 Rep, Weapons, Coins!"),
            ("CROSS THE THRESHOLD (Quest 10): ", "Walk to the great bridge barricade & speak to Prelate Castiel!", "Barricade opened! FULL PERMANENT ACCESS INTO THE CAULDRON!")
        ]
    }
]
img7 = build_briefing_image(forest_raw, 7, "Sombre Forest · Mount Sinai (Books 6 & 7)", "Sombre Forest", "Down From Mount Sinai", "[MANDATORY: BRING GOLD KEY IN POUCH]", (245, 158, 11), pins_7, route_7, cards_7, crop_box=(800, 1500, 3900, 3800))
img7.save(os.path.join(OUT_DIR, 'raid7_map.jpg'), quality=90)

print("All 7 ultra-detailed tactical raid infographics successfully generated!")
