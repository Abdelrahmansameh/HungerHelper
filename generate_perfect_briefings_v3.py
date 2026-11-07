import os, sys
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v3 as core

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
            {"x": 2368, "y": 1475, "name": "Sarlat Village Granaries", "sub": "High Flour Sack density", "color": (56, 189, 248), "label_x": 1050, "label_y": 500},
            {"x": 1259, "y": 1065, "name": "Master Granary & Farmsteads", "sub": "Flour Sacks & Fireplaces", "color": (56, 189, 248), "label_x": 100, "label_y": 280}
        ],
        "show_all_loot": True,
        "primary_target": {
            "title": "20x Flour",
            "item_img": "flour.png",
            "cont_title": "Flour Sack / Oak Barrel",
            "cont_img": "flour_sack.webp",
            "drop_rate": "47.6%",
            "density": "597 spots on map",
            "desc": "Primary quest requirement for Eloise. Abundant in all farmhouses and granaries across Sarlat."
        },
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check bedroom nightstands & desks for Opium Pipe!"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Check farmhouse & church walls for China Bowl!")
        ],
        "upcoming_targets": [
            ("Pile of Ash", "pile_of_ash.webp", "15x Charcoal (Q4)", "charcoal.png", "52.6%", "85 spots", "Search hearths & fire pits to bank 15x Charcoal early for Q4"),
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 spots", "Workshop corners in Sarlat military battery")
        ],
        "secondary_mob_note": "Secondary mob note: Dreg Military patrols have a 1/112 drop rate for Flour & Saltpetre.",
        "steps": [
            "Check spawn on Sarlat and orient toward Sarlat Village or Western Granaries.",
            "Loot Flour Sacks (47.6%) and Oak Barrels (38.5%) until reaching 20x Flour.",
            "Sweep fireplaces for 15x Charcoal (52.6%) and Bullion Boxes (Gold) for Opium Pipe.",
            "Extract via designated match extraction gate and return to Château."
        ],
        "post_raid": "Hand in 20x Flour to Eloise -> Unlocks Quest 3: The Gavroche Family."
    },
    {
        "id": 2,
        "phase": "RAID 2 OF 7 · RECON & SCOUTING",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: The Gavroche Family",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (16, 185, 129), (255, 255, 255)),
        "objectives": [
            {"x": 1479, "y": 313, "name": "Gavroche Family Camp", "sub": "Lower bridge deck · Instant discovery trigger", "color": (59, 130, 246), "label_x": 750, "label_y": 140}
        ],
        "show_all_loot": True,
        "primary_target": {
            "title": "Gavroche Family Camp",
            "item_img": "charcoal.png",
            "cont_title": "Camp Location (X: 1479, Y: 313)",
            "cont_img": "basket.webp",
            "drop_rate": "100%",
            "density": "Instant Trigger",
            "desc": "Primary quest requirement. Walk directly into the camp perimeter on the lower bridge deck."
        },
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "37 open spots", "Search bridge tollhouse desks and administrative bedrooms"),
            ("Wall Cabinet / Shelf", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "3 open spots", "Carriage House cellar & upstairs room of Underbridge Smithy")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "24 open spots", "Workshop corners along bridge piers"),
            ("Pile of Ash", "pile_of_ash.webp", "15x Charcoal (Q4 backup)", "charcoal.png", "52.6%", "13 spots", "Old stoves & burnt encampment hearths")
        ],
        "secondary_mob_note": "Significant mob drop: Roaming road Brutes & Droolers have a 1/52 (1.9%) Opium drop rate (no dungeon key!).",
        "steps": [
            "Advance along the Jacques Bridge span toward the Gavroche Camp (X: 1479, Y: 313).",
            "Walking into the camp triggers objective completion automatically.",
            "Loot open Bullion Boxes for Opium Pipe and eliminate any road Brutes for Opium.",
            "Head to whichever bridge extraction gate is active on your HUD and extract safely."
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
            {"x": 1086, "y": 1299, "name": "Tactical Map (Command Post)", "sub": "Interact with map on war table", "color": (59, 130, 246), "label_x": 110, "label_y": 560},
            {"x": 1196, "y": 1315, "name": "Gunline Fort (Battery)", "sub": "Scout artillery battery fortifications", "color": (245, 158, 11), "label_x": 110, "label_y": 660}
        ],
        "show_all_loot": True,
        "primary_target": {
            "title": "Tactical Map & Gunline Fort",
            "item_img": "saltpetre.png",
            "cont_title": "Command Post (X: 1086, Y: 1299)",
            "cont_img": "tooling_bin.webp",
            "drop_rate": "100%",
            "density": "2 Scout Points",
            "desc": "Primary quest requirement. Interact with map on war table, then scout adjacent Gunline Fort battery."
        },
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check nightstands in farmhouses & garrison quarters"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "House walls near command post sector")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 open spots", "High density around artillery redoubts & workshops"),
            ("Stone Grave", "stone_grave.webp", "5x Damp Rag (Q6)", "damp_rag.png", "23.8%", "40 open spots", "Churchyard & ditch burials across Sarlat Farm")
        ],
        "secondary_mob_note": "Secondary mob note: Garrisoned Dreg Military mobs have a 1/112 drop chance for Saltpetre & Damp Rags.",
        "steps": [
            "Spawn in Sarlat and orient toward the northwest fortifications (Command Post).",
            "Interact with the Tactical Map at (X: 1086, Y: 1299) and scout Gunline Fort (X: 1196, Y: 1315).",
            "Loot Tooling Bins (18.9% Saltpetre) and Stone Graves (23.8% Damp Rags) in the trenches.",
            "Extract via designated match extraction gate and return to the Château."
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
            {"x": 3048, "y": 2488, "name": "Chapel of Weeping Virgins", "sub": "Red Candle on bench/altar (Active Q8 only!)", "color": (239, 68, 68), "label_x": 800, "label_y": 1050}
        ],
        "show_all_loot": True,
        "primary_target": {
            "title": "Red Votive Candle",
            "item_img": "votive_candle.png",
            "cont_title": "Chapel Altar / Bench",
            "cont_img": "pile_of_ash.webp",
            "drop_rate": "100%",
            "density": "1 unique spot",
            "desc": "Primary quest requirement. Spawns physically on the altar/bench ONLY while Quest 8 is active!"
        },
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "40 open spots", "Check chapel rectory lockboxes if still needed"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Parsonage living quarters on church grounds")
        ],
        "upcoming_targets": [
            ("Stone Grave", "stone_grave.webp", "Damp Rag (Q6 backup)", "damp_rag.png", "23.8%", "40 open spots", "Church graveyard burials right outside the chapel"),
            ("Bribery Check", "opium.png", "Bribery Trio Complete", "china_bowl.png", "Ready", "3 Items", "Ensure China Bowl, Opium Pipe & Opium are in stash")
        ],
        "secondary_mob_note": "Secondary mob note: Graveyard Brute outside church has a 1/226 drop rate for Bribery items.",
        "steps": [
            "Check spawn on Sarlat and orient toward the Chapel of Weeping Virgins (X: 3048, Y: 2488).",
            "Enter the open chapel and take the Red Votive Candle directly from the bench/altar.",
            "Loot nearby rectory lockboxes for Opium Pipe if still needed for Mr Sweet.",
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
            {"x": 2446, "y": 1550, "name": "Book 1: Census of 1806", "sub": "Farmhouse · Ledger desk in 2nd room (OPEN)", "color": (56, 189, 248), "label_x": 1050, "label_y": 560},
            {"x": 1259, "y": 1065, "name": "Book 2: Course in Agriculture", "sub": "Garnier's Windmill · On desk (OPEN)", "color": (56, 189, 248), "label_x": 100, "label_y": 280},
            {"x": 3048, "y": 2488, "name": "Book 3: Catechisme 1567", "sub": "Chapel of Weeping Virgins · On altar (OPEN)", "color": (56, 189, 248), "label_x": 800, "label_y": 1050}
        ],
        "show_all_loot": False,
        "primary_target": {
            "title": "Books 1, 2, 3 (Sarlat Farm)",
            "item_img": "book_census.png",
            "cont_title": "Desks in Windmill, Farmhouse, Chapel",
            "cont_img": "ledger_desk.webp",
            "drop_rate": "100%",
            "density": "3 Open Desks",
            "desc": "Primary quest requirement. All 3 books are in open, unlocked buildings. Zero keys needed!"
        },
        "hardest_targets": [
            ("Book 1: Census 1806", "ledger_desk.webp", "Census of 1806", "book_census.png", "100%", "Farmhouse", "On the ledger desk inside the second room (OPEN)"),
            ("Book 2: Agriculture", "ledger_desk.webp", "Course in Agriculture", "book_rozier.png", "100%", "Garnier's Windmill", "On a desk inside Garnier's Windmill (OPEN)")
        ],
        "upcoming_targets": [
            ("Book 3: Catechisme", "ledger_desk.webp", "Catechisme of 1567", "book_catechisme.png", "100%", "Chapel Virgins", "On the altar inside the open chapel ruins (OPEN)"),
            ("Key Status Check", "flour_sack.webp", "Zero Keys Needed", "votive_candle.png", "Safe", "No Keys Needed", "All books are in open buildings — keep stash safe!")
        ],
        "secondary_mob_note": "Combat note: Only defend yourself as needed. Books do not drop from mobs.",
        "steps": [
            "Check spawn on Sarlat and path toward whichever of the 3 books is closest to you.",
            "Book 1: Collect 'Census of 1806' from Farmhouse second room ledger desk (X: 2446, Y: 1550).",
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
            {"x": 1391, "y": 1535, "name": "Book 4: The Spirit of the Laws", "sub": "Jacques Bridge Tower · Top desk (OPEN)", "color": (59, 130, 246), "label_x": 750, "label_y": 620},
            {"x": 2094, "y": 1346, "name": "Book 5: Buffon Natural History", "sub": "Carriage House · Fireplace board (OPEN)", "color": (59, 130, 246), "label_x": 1050, "label_y": 520}
        ],
        "show_all_loot": False,
        "primary_target": {
            "title": "Books 4 & 5 (Jacques Bridge)",
            "item_img": "book_buffon.png",
            "cont_title": "Bridge Tower & Carriage House",
            "cont_img": "ledger_desk.webp",
            "drop_rate": "100%",
            "density": "2 Open Spots",
            "desc": "Primary quest requirement. Both books are in open structures — NO locked doors or Silver Keys needed!"
        },
        "hardest_targets": [
            ("Book 4: Montesquieu", "ledger_desk.webp", "Spirit of the Laws", "book_montesquieu.png", "100%", "Bridge Tower", "On the top desk inside the Jacques Bridge Tower (OPEN)"),
            ("Book 5: Buffon History", "ledger_desk.webp", "Natural History", "book_buffon.png", "100%", "Carriage House", "On the fireplace board inside the Carriage House (OPEN)")
        ],
        "upcoming_targets": [
            ("Bridge Looting", "tooling_bin.webp", "Saltpetre & Supplies", "saltpetre.png", "High", "Pier Workshops", "Grab extra crafting supplies if needed on way to extract"),
            ("Loadout Status", "basket.webp", "No Key Requirement", "silver_key.png", "Zero Keys", "Open World", "Both books are out in the open — do NOT bring keys!")
        ],
        "secondary_mob_note": "Combat note: Roaming Brutes patrol the main bridge road. Bypass or snipe from distance.",
        "steps": [
            "Deploy onto Jacques Bridge with 0 keys in your inventory.",
            "Book 4: Loot 'The Spirit of the Laws - Montesquieu' from the top desk in the Tower (X: 1391, Y: 1535).",
            "Book 5: Loot 'Natural History - Buffon' from the fireplace board in the Carriage House (X: 2094, Y: 1346).",
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
            {"x": 2592, "y": 2992, "name": "Book 6: Codex Medicamentarius", "sub": "Infirmary Camp · Ledger desk in tent (OPEN)", "color": (59, 130, 246), "label_x": 800, "label_y": 1050},
            {"x": 3168, "y": 2405, "name": "Book 7: Civil Architecture", "sub": "Black Wood Mill · Box by upstairs desk (OPEN)", "color": (59, 130, 246), "label_x": 800, "label_y": 780}
        ],
        "show_all_loot": False,
        "primary_target": {
            "title": "Books 6 & 7 (Sombre Forest)",
            "item_img": "book_rondelet.png",
            "cont_title": "Infirmary Tent & Black Wood Mill",
            "cont_img": "ledger_desk.webp",
            "drop_rate": "100%",
            "density": "2 Open Spots",
            "desc": "Primary quest requirement. Both books are in open structures — NO Gold Keys or vault locks needed!"
        },
        "hardest_targets": [
            ("Book 6: Codex", "ledger_desk.webp", "Codex Medicamentarius", "tallow_balm.png", "100%", "Infirmary Camp", "On a ledger desk inside a tent at the Infirmary Camp (OPEN)"),
            ("Book 7: Civil Architecture", "ledger_desk.webp", "Course in Architecture", "book_rondelet.png", "100%", "Black Wood Mill", "On a wooden box next to the upstairs desk (OPEN)")
        ],
        "upcoming_targets": [
            ("Camp Bandages", "stone_grave.webp", "Field Supplies", "damp_rag.png", "High", "Infirmary Tents", "Search open medical bags if needed"),
            ("Loadout Status", "physician_bag.webp", "No Key Requirement", "gold_key.png", "Zero Keys", "Open World", "Both forest books are in open structures — 0 keys needed!")
        ],
        "secondary_mob_note": "Combat note: Beware of forest prowlers near the mill. Keep sound low.",
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
    draw.rectangle([0, 0, CANVAS_W, 85], fill=(11, 15, 25))
    draw.line([0, 85, CANVAS_W, 85], fill=(51, 65, 85), width=2)
    
    # Title & Phase
    draw.text((25, 14), cfg["phase"], fill=(255, 230, 0), font=F_HEADER_TAG)
    draw.text((25, 38), f"{cfg['quest_name']}  ·  {cfg['map_name']}", fill=(255, 255, 255), font=F_HEADER_TITLE)
    
    # Key Badge (Header Right)
    badge_text, bg_col, text_col = cfg["key_status"]
    bw = int(draw.textlength(badge_text, font=F_HEADER_TAG)) + 36
    bx = CANVAS_W - bw - 25
    draw.rounded_rectangle([bx, 18, bx+bw, 68], radius=8, fill=bg_col, outline=(255, 255, 255), width=2)
    draw.text((bx+18, 30), badge_text, fill=text_col, font=F_HEADER_TAG)
    
    # 2. LEFT MAP PANEL (Expanded to 1590px width!)
    core.render_terrain_map(draw, canvas, cfg["map_img"], cfg["map_name"], cfg["objectives"], show_all_loot=cfg["show_all_loot"])
    
    # 3. RIGHT BRIEFING PANEL (Prioritized & Organized)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=(15, 20, 30), outline=(51, 65, 85), width=2)
    
    cur_y = PANEL_Y + 18
    
    # ==========================================
    # PRIORITY 1: RAID QUEST OBJECTIVE
    # ==========================================
    draw.text((PANEL_X+20, cur_y), "PRIORITY 1: RAID QUEST OBJECTIVE (THIS MATCH)", fill=(255, 230, 0), font=F_SECTION_TITLE)
    cur_y += 28
    
    p = cfg["primary_target"]
    p_box_h = 100
    draw.rounded_rectangle([PANEL_X+20, cur_y, PANEL_X+PANEL_W-20, cur_y+p_box_h], radius=8, fill=(24, 34, 53), outline=(59, 130, 246), width=2)
    
    # Thumbnails
    c_path = os.path.join(CONT_DIR, p["cont_img"])
    core.paste_icon_safe(canvas, c_path, (PANEL_X+32, cur_y+18, 64, 64), bg_color=(15, 23, 42))
    i_path = os.path.join(ITEM_DIR, p["item_img"])
    core.paste_icon_safe(canvas, i_path, (PANEL_X+104, cur_y+18, 64, 64), bg_color=(15, 23, 42))
    
    draw.text((PANEL_X+180, cur_y+12), f"{p['title']}  →  {p['cont_title']}", fill=(255, 255, 255), font=F_BODY_BOLD)
    draw.text((PANEL_X+180, cur_y+38), f"Drop Rate: {p['drop_rate']}  ·  Spots: {p['density']}", fill=(255, 230, 0), font=F_SMALL_BOLD)
    draw.text((PANEL_X+180, cur_y+62), p["desc"], fill=(203, 213, 225), font=F_TINY)
    
    cur_y += p_box_h + 16
    
    # ==========================================
    # PRIORITY 2: HARDEST DROP RATES TO CHECK
    # ==========================================
    draw.text((PANEL_X+20, cur_y), "PRIORITY 2: HARDEST DROP RATES (RARE BRIBERY ITEMS)", fill=(244, 63, 94), font=F_SECTION_TITLE)
    cur_y += 28
    
    for c_title, c_img, i_title, i_img, drop_rate, count, note in cfg["hardest_targets"]:
        card_h = 76
        draw.rounded_rectangle([PANEL_X+20, cur_y, PANEL_X+PANEL_W-20, cur_y+card_h], radius=8, fill=(11, 15, 25), outline=(51, 65, 85), width=1)
        
        c_path = os.path.join(CONT_DIR, c_img)
        core.paste_icon_safe(canvas, c_path, (PANEL_X+30, cur_y+10, 56, 56), bg_color=(20, 28, 42))
        i_path = os.path.join(ITEM_DIR, i_img)
        core.paste_icon_safe(canvas, i_path, (PANEL_X+94, cur_y+10, 56, 56), bg_color=(20, 28, 42))
        
        draw.text((PANEL_X+162, cur_y+10), f"{c_title}  →  {i_title}", fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+162, cur_y+32), f"Drop Rate: {drop_rate}  ·  Spots: {count}", fill=(255, 230, 0), font=F_SMALL_BOLD)
        draw.text((PANEL_X+162, cur_y+52), note, fill=(148, 163, 184), font=F_TINY)
        cur_y += card_h + 10
        
    cur_y += 6
    
    # ==========================================
    # PRIORITY 3: UPCOMING QUEST REQUIREMENTS
    # ==========================================
    draw.text((PANEL_X+20, cur_y), "PRIORITY 3: UPCOMING QUEST ITEMS (PRE-FARMING)", fill=(52, 211, 153), font=F_SECTION_TITLE)
    cur_y += 28
    
    for c_title, c_img, i_title, i_img, drop_rate, count, note in cfg["upcoming_targets"]:
        card_h = 76
        draw.rounded_rectangle([PANEL_X+20, cur_y, PANEL_X+PANEL_W-20, cur_y+card_h], radius=8, fill=(11, 15, 25), outline=(51, 65, 85), width=1)
        
        c_path = os.path.join(CONT_DIR, c_img)
        core.paste_icon_safe(canvas, c_path, (PANEL_X+30, cur_y+10, 56, 56), bg_color=(20, 28, 42))
        i_path = os.path.join(ITEM_DIR, i_img)
        core.paste_icon_safe(canvas, i_path, (PANEL_X+94, cur_y+10, 56, 56), bg_color=(20, 28, 42))
        
        draw.text((PANEL_X+162, cur_y+10), f"{c_title}  →  {i_title}", fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+162, cur_y+32), f"Drop Rate: {drop_rate}  ·  Spots: {count}", fill=(52, 211, 153), font=F_SMALL_BOLD)
        draw.text((PANEL_X+162, cur_y+52), note, fill=(148, 163, 184), font=F_TINY)
        cur_y += card_h + 10

    # Secondary mob note if present
    if cfg.get("secondary_mob_note"):
        draw.text((PANEL_X+24, cur_y), cfg["secondary_mob_note"], fill=(148, 163, 184), font=F_TINY)
        cur_y += 22

    cur_y += 8
    
    # ==========================================
    # SPAWN-INDEPENDENT EXECUTION STEPS
    # ==========================================
    draw.text((PANEL_X+20, cur_y), "SPAWN-INDEPENDENT EXECUTION STEPS", fill=(255, 230, 0), font=F_SECTION_TITLE)
    cur_y += 28
    
    for idx, step in enumerate(cfg["steps"]):
        draw.ellipse([PANEL_X+24, cur_y+2, PANEL_X+46, cur_y+24], fill=(59, 130, 246), outline=(255, 255, 255), width=1)
        draw.text((PANEL_X+30, cur_y+4), str(idx+1), fill=(255, 255, 255), font=F_SMALL_BOLD)
        draw.text((PANEL_X+56, cur_y+3), step, fill=(226, 232, 240), font=F_SMALL)
        cur_y += 32
        
    cur_y += 10
    
    # ==========================================
    # POST-RAID ACTION & HAND-IN PROTOCOL
    # ==========================================
    draw.rounded_rectangle([PANEL_X+20, cur_y, PANEL_X+PANEL_W-20, PANEL_Y+PANEL_H-20], radius=8, fill=(6, 78, 59, 160), outline=(16, 185, 129), width=2)
    draw.text((PANEL_X+34, cur_y+14), "POST-RAID ACTION & HAND-IN PROTOCOL", fill=(110, 231, 183), font=F_BODY_BOLD)
    draw.text((PANEL_X+34, cur_y+40), cfg["post_raid"], fill=(255, 255, 255), font=F_BODY_BOLD)

    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

print("Generating all 7 prioritized panoramic briefings...")
for cfg in RAIDS_CONFIG:
    render_briefing(cfg)
print("All 7 briefings generated successfully!")
