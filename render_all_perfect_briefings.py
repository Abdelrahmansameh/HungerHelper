import os, sys
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core as core

CANVAS_W = core.CANVAS_W
CANVAS_H = core.CANVAS_H
PANEL_X = core.PANEL_X
PANEL_Y = core.PANEL_Y
PANEL_W = core.PANEL_W
PANEL_H = core.PANEL_H

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ARTIFACT_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")

F_HEADER_TITLE = core.F_HEADER_TITLE
F_HEADER_TAG = core.F_HEADER_TAG
F_CARD_TITLE = core.F_CARD_TITLE
F_SECTION_TITLE = core.F_SECTION_TITLE
F_BODY = core.F_BODY
F_BODY_BOLD = core.F_BODY_BOLD
F_SMALL = core.F_SMALL
F_SMALL_BOLD = core.F_SMALL_BOLD
F_TINY = core.F_TINY
F_MAP_LABEL = core.F_MAP_LABEL
F_PIN_NUM = core.F_PIN_NUM

SARLAT_MAP = os.path.join(DOC_DIR, "sarlat-farm.webp")
JACQUES_MAP = os.path.join(DOC_DIR, "jacques-bridge.webp")
SOMBRE_MAP = os.path.join(DOC_DIR, "sombre-forest.webp")

RAIDS_CONFIG = [
    {
        "id": 1,
        "phase": "RAID 1 OF 7 · INTRODUCTORY GATHERING",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 2: Making Dough",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 2368, "y": 1475, "name": "Sarlat Village Granaries", "sub": "High Flour Sack density", "color": (56, 189, 248), "label_x": 920, "label_y": 500},
            {"x": 1259, "y": 1065, "name": "Master Granary & Farmsteads", "sub": "Flour Sacks & Fireplaces", "color": (56, 189, 248), "label_x": 100, "label_y": 300}
        ],
        "show_all_loot": True,
        "pre_loot_alert": "PRIORITY PRE-LOOTING: Check all Bullion Boxes (gold stars) for Opium Pipe and Wall Cabinets (pink diamonds) for China Bowl while collecting Flour! You need them for Mr Sweet's Bribery quest later.",
        "containers": [
            ("Flour Sack", "flour_sack.webp", "Flour (Q2)", "flour.png", "47.6%", "597 spots", "Primary food container across all farmhouses"),
            ("Pile of Ash", "pile_of_ash.webp", "Charcoal (Q4)", "charcoal.png", "52.6%", "85 spots", "Search hearths & fireplaces for 15x Charcoal"),
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check bedroom nightstands & desks for Opium Pipe!"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Check farmhouse & church walls for China Bowl!")
        ],
        "steps": [
            "Check spawn position on map and orient toward Sarlat Village or Western Granaries.",
            "Loot Flour Sacks (47.6%) and Oak Barrels (38.5%) until reaching 20x Flour.",
            "Loot all hearths and fire pits for Pile of Ash (52.6%) to secure 15x Charcoal early for Q4.",
            "Search marked Bullion Boxes (Gold) for Opium Pipe and Wall Cabinets (Pink) for China Bowl.",
            "Navigate to whichever extraction gate your match HUD designates and extract to Château."
        ],
        "post_raid": "Hand in 20x Flour to Eloise -> Unlocks Quest 3: The Gavroche Family."
    },
    {
        "id": 2,
        "phase": "RAID 2 OF 7 · RECON & MOB DROPS",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: The Gavroche Family",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 1479, "y": 313, "name": "Gavroche Family Camp", "sub": "Lower bridge deck · Instant discovery trigger", "color": (59, 130, 246), "label_x": 650, "label_y": 140}
        ],
        "show_all_loot": True,
        "pre_loot_alert": "DOUBLE TURN-IN ALERT: If you collected 15x Charcoal during Raid 1, you can hand in Quest 3 AND Quest 4 (Cold Hearth) immediately after this raid with ZERO extra deployments!",
        "containers": [
            ("Roaming Brute / Drooler", "basket.webp", "Opium (Bribery)", "opium.png", "1/52 (1.9%)", "Road patrols", "Kill open-world heavy mobs on bridge for Opium (No dungeon key!)"),
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "37 open spots", "Search bridge tollhouse desks and administrative bedrooms"),
            ("Wall Cabinet / Shelf", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "3 open spots", "Carriage House cellar & upstairs room of Underbridge Smithy"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "24 open spots", "Workshop corners along open bridge piers")
        ],
        "steps": [
            "Check spawn on Jacques Bridge span and advance toward the Gavroche Camp (X: 1479, Y: 313).",
            "Camp triggers completion instantly upon walking into the area.",
            "Eliminate road Brutes & Droolers on the bridge deck for Opium (1/52 drop rate).",
            "Check bridge tollhouse desks and Bullion Boxes for Opium Pipe if still needed.",
            "Head to whichever bridge extraction point is open on your match timer and extract safely."
        ],
        "post_raid": "DOUBLE TURN-IN: Hand in Q3 to Eloise -> Immediately turn in 15x Charcoal to complete Q4!"
    },
    {
        "id": 3,
        "phase": "RAID 3 OF 7 · MILITARY RECON & TRENCHES",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 5: Mapping the Front",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 1086, "y": 1299, "name": "Tactical Map (Command Post)", "sub": "Interact with map on war table", "color": (59, 130, 246), "label_x": 110, "label_y": 540},
            {"x": 1196, "y": 1315, "name": "Gunline Fort (Battery)", "sub": "Scout artillery battery fortifications", "color": (245, 158, 11), "label_x": 110, "label_y": 640}
        ],
        "show_all_loot": True,
        "pre_loot_alert": "TRIPLE TURN-IN READY: In the trenches around the fort, gather the 20x Saltpetre and 5x Damp Rags needed for Quest 6 (Bare Necessities) to enable a triple turn-in after this raid!",
        "containers": [
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 open spots", "High density around artillery redoubts & workshops"),
            ("Stone Grave", "stone_grave.webp", "Damp Rag (Q6)", "damp_rag.png", "23.8%", "40 open spots", "Churchyard & ditch burials across Sarlat Farm"),
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check nightstands in farmhouses & garrison quarters"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "House walls near command post sector")
        ],
        "steps": [
            "Spawn in Sarlat and orient toward the northwest fortifications (Command Post).",
            "Interact with the Tactical Map on the military table at (X: 1086, Y: 1299).",
            "Scout the adjacent Gunline Fort artillery trenches at (X: 1196, Y: 1315).",
            "Raid Tooling Bins (18.9% Saltpetre) and Stone Graves (23.8% Damp Rags) in the trenches.",
            "Extract via designated match extraction and return to the Château."
        ],
        "post_raid": "TRIPLE TURN-IN: Hand in Q5 -> Hand in Q6 (Bare Necessities) -> Speak to Mr Sweet (Q7)!"
    },
    {
        "id": 4,
        "phase": "RAID 4 OF 7 · THE CHAPEL ALTAR",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8: Pushing Back the Shadows",
        "key_status": ("ACTIVE-QUEST SPAWN (0 KEYS REQUIRED)", (88, 28, 135), (255, 255, 255)),
        "objectives": [
            {"x": 3048, "y": 2488, "name": "Chapel of Weeping Virgins", "sub": "Red Candle on bench/altar (Active Q8 only!)", "color": (239, 68, 68), "label_x": 750, "label_y": 1050}
        ],
        "show_all_loot": True,
        "pre_loot_alert": "QUEST-ONLY SPAWN: The Red Votive Candle physically spawns on the altar/bench ONLY while Quest 8 is active in your quest log. Also ensure your 3 Bribery items (Bowl, Pipe, Opium) are in stash!",
        "containers": [
            ("Chapel Altar / Bench", "pile_of_ash.webp", "Red Votive Candle", "votive_candle.png", "100%", "1 unique spot", "Spawns ONLY while Quest 8 is active!"),
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check chapel rectory lockboxes if still needed"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Parsonage living quarters on church grounds"),
            ("Stone Grave", "stone_grave.webp", "Damp Rag (Q6 backup)", "damp_rag.png", "23.8%", "40 open spots", "Church graveyard burials right outside the chapel")
        ],
        "steps": [
            "Check spawn on Sarlat and orient toward the southeastern Chapel ruins (X: 3048, Y: 2488).",
            "Enter the chapel interior and take the Red Votive Candle from the bench/altar.",
            "Check rectory lockboxes for Opium Pipe and Wall Cabinets for China Bowl if missing.",
            "Deposit the candle safely into your secure pouch.",
            "Navigate to your active extraction gate and return to the Château."
        ],
        "post_raid": "Hand in Candle to Eloise (Q8) -> Hand in 3 Bribery Items to Mr Sweet -> Unlocks Quest 9!"
    },
    {
        "id": 5,
        "phase": "RAID 5 OF 7 · MOUNT SINAI (SARLAT BOOKS 1-3)",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Books 1, 2, 3)",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 2446, "y": 1550, "name": "Book 1: Census of 1806", "sub": "Farmhouse · Ledger desk in 2nd room (OPEN)", "color": (56, 189, 248), "label_x": 920, "label_y": 560},
            {"x": 1259, "y": 1065, "name": "Book 2: Course in Agriculture", "sub": "Garnier's Windmill · On desk (OPEN)", "color": (56, 189, 248), "label_x": 90, "label_y": 280},
            {"x": 3048, "y": 2488, "name": "Book 3: Catechisme 1567", "sub": "Chapel of Weeping Virgins · On altar (OPEN)", "color": (56, 189, 248), "label_x": 750, "label_y": 1050}
        ],
        "show_all_loot": False,
        "pre_loot_alert": "100% VERIFIED: ZERO KEYS NEEDED! All 3 books on Sarlat Farm are located in open, unlocked buildings. Keep your inventory empty of keys to eliminate risk upon death.",
        "containers": [
            ("Book 1: Census 1806", "ledger_desk.webp", "Census of 1806", "book_census.png", "100%", "Farmhouse", "On the ledger desk inside the second room (OPEN)"),
            ("Book 2: Agriculture", "ledger_desk.webp", "Course in Agriculture", "book_rozier.png", "100%", "Garnier's Windmill", "On a desk inside Garnier's Windmill (OPEN)"),
            ("Book 3: Catechisme", "ledger_desk.webp", "Catechisme of 1567", "book_catechisme.png", "100%", "Chapel Virgins", "On the altar inside the open chapel ruins (OPEN)"),
            ("Key Status Check", "flour_sack.webp", "Zero Keys Needed", "votive_candle.png", "Safe", "No Keys Required", "All 3 books are in open structures — keep stash safe!")
        ],
        "steps": [
            "Check spawn on Sarlat and path toward whichever of the 3 books is closest to you.",
            "Book 1: Collect 'Census of 1806' from Farmhouse ledger desk (X: 2446, Y: 1550).",
            "Book 2: Collect 'Course in Agriculture - Rozier' from Garnier's Windmill desk (X: 1259, Y: 1065).",
            "Book 3: Collect 'Catechisme of Christian Doctrine' from Chapel altar (X: 3048, Y: 2488).",
            "Extract with all 3 books safely stored in your secure pouch and return to Château."
        ],
        "post_raid": "Deposit Books 1-3 into stash -> Head to Jacques Bridge for Books 4 & 5 (0 keys needed)."
    },
    {
        "id": 6,
        "phase": "RAID 6 OF 7 · MOUNT SINAI (BRIDGE BOOKS 4 & 5)",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Books 4 & 5)",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 1391, "y": 1535, "name": "Book 4: The Spirit of the Laws", "sub": "Jacques Bridge Tower · Top desk (OPEN)", "color": (59, 130, 246), "label_x": 620, "label_y": 620},
            {"x": 2094, "y": 1346, "name": "Book 5: Buffon Natural History", "sub": "Carriage House · Fireplace board (OPEN)", "color": (59, 130, 246), "label_x": 880, "label_y": 520}
        ],
        "show_all_loot": False,
        "pre_loot_alert": "100% VERIFIED: ZERO KEYS NEEDED! Book 5 is located in the Carriage House on the fireplace board — NOT behind any locked doors! Zero keys are required.",
        "containers": [
            ("Book 4: Montesquieu", "ledger_desk.webp", "Spirit of the Laws", "book_montesquieu.png", "100%", "Bridge Tower", "On the top desk inside the Jacques Bridge Tower (OPEN)"),
            ("Book 5: Buffon History", "ledger_desk.webp", "Natural History", "book_buffon.png", "100%", "Carriage House", "On the fireplace board inside the Carriage House (OPEN)"),
            ("Open Road Notice", "basket.webp", "No Locked Doors", "silver_key.png", "Zero Keys", "Open World", "Both books are out in the open — do NOT bring keys!"),
            ("Bridge Looting", "tooling_bin.webp", "Saltpetre & Supplies", "saltpetre.png", "High", "Pier Workshops", "Grab extra supplies if needed on way to extract")
        ],
        "steps": [
            "Deploy onto Jacques Bridge with an empty key pouch (0 keys needed!).",
            "Book 4: Loot 'The Spirit of the Laws - Montesquieu' from the top desk in the Tower (X: 1391, Y: 1535).",
            "Book 5: Loot 'Natural History - Buffon' from the fireplace board in the Carriage House (X: 2094, Y: 1346).",
            "Deposit both books safely into your secure pouch.",
            "Head to the nearest open extraction gate and extract safely to the Château."
        ],
        "post_raid": "Deposit Books 4 & 5 into stash -> Head to Sombre Forest for Books 6 & 7 (0 keys needed)."
    },
    {
        "id": 7,
        "phase": "RAID 7 OF 7 · MOUNT SINAI (FOREST BOOKS 6 & 7)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Books 6 & 7)",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 2592, "y": 2992, "name": "Book 6: Codex Medicamentarius", "sub": "Infirmary Camp · Ledger desk in tent (OPEN)", "color": (59, 130, 246), "label_x": 750, "label_y": 1050},
            {"x": 3168, "y": 2405, "name": "Book 7: Civil Architecture", "sub": "Black Wood Mill · Box by upstairs desk (OPEN)", "color": (59, 130, 246), "label_x": 750, "label_y": 780}
        ],
        "show_all_loot": False,
        "pre_loot_alert": "100% VERIFIED: ZERO KEYS NEEDED! Book 7 is located in the Black Wood Mill on a box next to the upstairs ledger desk — NOT in a locked vault! Zero keys required.",
        "containers": [
            ("Book 6: Codex", "ledger_desk.webp", "Codex Medicamentarius", "tallow_balm.png", "100%", "Infirmary Camp", "On a ledger desk inside a tent at the Infirmary Camp (OPEN)"),
            ("Book 7: Civil Architecture", "ledger_desk.webp", "Course in Architecture", "book_rondelet.png", "100%", "Black Wood Mill", "On a wooden box next to the upstairs desk (OPEN)"),
            ("Open Forest Notice", "physician_bag.webp", "No Key Requirement", "gold_key.png", "Zero Keys", "Open World", "Both forest books are in open structures — 0 keys needed!"),
            ("Camp Bandages", "stone_grave.webp", "Field Supplies", "damp_rag.png", "High", "Infirmary Tents", "Search open medical bags if needed")
        ],
        "steps": [
            "Deploy into Sombre Forest with 0 keys in inventory (keep pouch open for books).",
            "Book 6: Loot 'Codex Medicamentarius' from ledger desk inside the Infirmary tent (X: 2592, Y: 2992).",
            "Book 7: Loot 'Course in Civil Architecture - Rondelet' from box by upstairs desk in Black Wood Mill (X: 3168, Y: 2405).",
            "Extract via whichever gate is currently active on your match HUD and return to Château.",
            "Deliver all 7 books to Eloise to complete Quest 9!"
        ],
        "post_raid": "FINAL TURN-IN: Hand in all 7 books to Eloise -> Speak to Prelate Castiel -> Cauldron Unlocked!"
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (15, 23, 42))
    draw = ImageDraw.Draw(canvas)
    
    # 1. TOP HEADER BAR
    draw.rectangle([0, 0, CANVAS_W, 90], fill=(11, 15, 25))
    draw.line([0, 90, CANVAS_W, 90], fill=(51, 65, 85), width=2)
    
    # Title & Phase
    draw.text((30, 16), cfg["phase"], fill=(255, 230, 0), font=F_HEADER_TAG)
    draw.text((30, 42), f"{cfg['quest_name']}  ·  {cfg['map_name']}", fill=(255, 255, 255), font=F_HEADER_TITLE)
    
    # Key Badge (Header Right)
    badge_text, bg_col, text_col = cfg["key_status"]
    bw = int(draw.textlength(badge_text, font=F_HEADER_TAG)) + 40
    bx = CANVAS_W - bw - 30
    draw.rounded_rectangle([bx, 20, bx+bw, 70], radius=8, fill=bg_col, outline=(255, 255, 255), width=2)
    draw.text((bx+20, 32), badge_text, fill=text_col, font=F_HEADER_TAG)
    
    # 2. LEFT MAP PANEL
    core.render_terrain_map(draw, canvas, cfg["map_img"], cfg["map_name"], cfg["objectives"], show_all_loot=cfg["show_all_loot"])
    
    # 3. RIGHT BRIEFING PANEL
    core.draw_round_rect(draw, [PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], fill=(15, 20, 30), outline=(51, 65, 85), width=2, radius=12)
    
    cur_y = PANEL_Y + 24
    
    # Section A: Pre-Looting Alert Box
    alert_box_h = 105
    draw.rounded_rectangle([PANEL_X+24, cur_y, PANEL_X+PANEL_W-24, cur_y+alert_box_h], radius=8, fill=(30, 27, 75, 220), outline=(129, 140, 248), width=2)
    draw.text((PANEL_X+40, cur_y+14), "TACTICAL PRE-LOOTING & PROGRESSION FOCUS", fill=(199, 210, 254), font=F_BODY_BOLD)
    
    # Wrap alert text
    alert_text = cfg["pre_loot_alert"]
    words = alert_text.split()
    lines, cur_line = [], ""
    for w in words:
        if len(cur_line + " " + w) < 85:
            cur_line = (cur_line + " " + w).strip()
        else:
            lines.append(cur_line); cur_line = w
    if cur_line: lines.append(cur_line)
    
    for i, line in enumerate(lines[:2]):
        draw.text((PANEL_X+40, cur_y+44 + i*24), line, fill=(224, 231, 255), font=F_SMALL)
        
    cur_y += alert_box_h + 24
    
    # Section B: Primary Target Cards (Top Drop Rate Containers)
    draw.text((PANEL_X+24, cur_y), "PRIORITY HIGH-DROP OPEN WORLD TARGETS (ZERO DUNGEON CLUTTER)", fill=(255, 230, 0), font=F_SECTION_TITLE)
    cur_y += 34
    
    for c_title, c_img, i_title, i_img, drop_rate, count, note in cfg["containers"]:
        card_h = 86
        draw.rounded_rectangle([PANEL_X+24, cur_y, PANEL_X+PANEL_W-24, cur_y+card_h], radius=8, fill=(11, 15, 25), outline=(51, 65, 85), width=1)
        
        # Container thumbnail (64x64)
        c_path = os.path.join(CONT_DIR, c_img)
        core.paste_icon_safe(canvas, c_path, (PANEL_X+36, cur_y+11, 64, 64), bg_color=(20, 28, 42))
        
        # Item thumbnail (64x64)
        i_path = os.path.join(ITEM_DIR, i_img)
        core.paste_icon_safe(canvas, i_path, (PANEL_X+112, cur_y+11, 64, 64), bg_color=(20, 28, 42))
        
        # Titles & Text
        draw.text((PANEL_X+190, cur_y+14), f"{c_title}  →  {i_title}", fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+190, cur_y+42), f"Drop Rate: {drop_rate}  ·  Spots: {count}", fill=(255, 230, 0), font=F_SMALL_BOLD)
        draw.text((PANEL_X+190, cur_y+63), note, fill=(148, 163, 184), font=F_TINY)
        
        # Drop Rate Pill on the right
        pill_w = 95
        pill_x = PANEL_X + PANEL_W - 24 - pill_w - 14
        draw.rounded_rectangle([pill_x, cur_y+24, pill_x+pill_w, cur_y+62], radius=6, fill=(245, 158, 11, 40), outline=(245, 158, 11), width=1)
        draw.text((pill_x+10, cur_y+34), drop_rate, fill=(253, 230, 138), font=F_BODY_BOLD)
        
        cur_y += card_h + 14

    cur_y += 10
    
    # Section C: Deployment & Navigation Steps (Spawn Independent)
    draw.text((PANEL_X+24, cur_y), "SPAWN-INDEPENDENT EXECUTION STEPS", fill=(255, 230, 0), font=F_SECTION_TITLE)
    cur_y += 32
    
    for idx, step in enumerate(cfg["steps"]):
        draw.ellipse([PANEL_X+28, cur_y+2, PANEL_X+52, cur_y+26], fill=(59, 130, 246), outline=(255, 255, 255), width=1)
        draw.text((PANEL_X+35, cur_y+5), str(idx+1), fill=(255, 255, 255), font=F_SMALL_BOLD)
        
        draw.text((PANEL_X+64, cur_y+4), step, fill=(226, 232, 240), font=F_BODY)
        cur_y += 38
        
    cur_y += 12
    
    # Section D: Post-Raid Stash & Hand-In Protocol
    draw.rounded_rectangle([PANEL_X+24, cur_y, PANEL_X+PANEL_W-24, PANEL_Y+PANEL_H-24], radius=8, fill=(6, 78, 59, 140), outline=(16, 185, 129), width=2)
    draw.text((PANEL_X+40, cur_y+16), "POST-RAID ACTION & HAND-IN PROTOCOL", fill=(110, 231, 183), font=F_BODY_BOLD)
    draw.text((PANEL_X+40, cur_y+46), cfg["post_raid"], fill=(255, 255, 255), font=F_BODY_BOLD)

    # Save output
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

print("Starting generation of all 7 unblocked high-visibility infographics...")
for cfg in RAIDS_CONFIG:
    render_briefing(cfg)
print("All 7 briefings generated!")
