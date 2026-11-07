import os, sys, io
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v7 as core
import loot_engine_v6 as loot

CANVAS_W = core.CANVAS_W
CANVAS_H = core.CANVAS_H
MAP_X = core.MAP_X
MAP_Y = core.MAP_Y
MAP_W = core.MAP_W
MAP_H = core.MAP_H
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
F_SECTION_TITLE = core.F_SECTION_TITLE
F_CARD_TITLE = core.F_CARD_TITLE
F_BODY_BOLD = core.F_BODY_BOLD
F_BODY = core.F_BODY
F_SMALL_BOLD = core.F_SMALL_BOLD
F_SMALL = core.F_SMALL
F_TINY = core.F_TINY
F_BADGE = core.F_BADGE

SARLAT_MAP = os.path.join(DOC_DIR, "sarlat-farm.webp")
JACQUES_MAP = os.path.join(DOC_DIR, "jacques-bridge.webp")
SOMBRE_MAP = os.path.join(DOC_DIR, "sombre-forest.webp")

def to_map_coord(x, y):
    mx = MAP_X + int((x / 4096.0) * MAP_W)
    my = MAP_Y + int((y / 4096.0) * MAP_H)
    return mx, my

RAIDS_CONFIG = [
    # RAID 1: Sarlat Farm (Making Dough)
    {
        "id": 1,
        "phase": "RAID 1 OF 7  —  INTRODUCTORY GATHERING",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 2: Making Dough",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Flour Sack", "flour_sack.webp", "Flour (Q2)", "flour.png", "47.6%", "Primary Objective"),
            ("Bullion Box", "bullion_box.webp", "Opium Pipe", "opium_pipe.png", "13.7%", "Hardest Drop (Gold)"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl", "china_bowl.png", "16.1%", "Hardest Drop (Gold)"),
            ("Pile of Ash", "pile_of_ash.webp", "Charcoal (Q4)", "charcoal.png", "52.6%", "Upcoming Stash (Q4)"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Upcoming Stash (Q6)")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 240, 'target_x': 520, 'target_y': 420,
                'color': (0, 229, 255),
                'title': "Master Granary Complex",
                'count_text': "18x Flour Sacks (20x Flour Goal)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'flour_sack.webp',
                'item_img': 'flour.png',
                'sub_text': "Loot 1st & 2nd floors + exterior barrels"
            },
            {
                'box_x': 1100, 'box_y': 380, 'target_x': 960, 'target_y': 550,
                'color': (0, 229, 255),
                'title': "Sarlat Village Granaries",
                'count_text': "14x Flour Sacks & Oak Barrels",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'flour_sack.webp',
                'item_img': 'flour.png',
                'sub_text': "Village farmhouses & granary lofts"
            },
            {
                'box_x': 500, 'box_y': 860, 'target_x': 710, 'target_y': 780,
                'color': (255, 234, 0),
                'title': "Farmhouse Bullion & Ash",
                'count_text': "12x Bullion Boxes · 15x Ash Piles",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'bullion_box.webp',
                'item_img': 'opium_pipe.png',
                'sub_text': "Bank 15x Charcoal & sweep for Opium Pipe"
            }
        ],
        # Differentiated Priority 1 Quests (Single in Raid 1)
        "priority_1_list": [
            {
                "tag": "PRIORITY 1: RAID OBJECTIVE (THIS MATCH)",
                "title": "Quest 2: Gather 20x Flour",
                "cont_title": "Flour Sack / Oak Barrel",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "32 spots in granaries",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. Abundant in all farmhouses & granaries across Sarlat."
            }
        ],
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "12 open spots", "Check bedroom nightstands & desks for Opium Pipe!"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Check farmhouse & church walls for China Bowl!")
        ],
        "upcoming_targets": [
            ("Pile of Ash", "pile_of_ash.webp", "15x Charcoal (Q4)", "charcoal.png", "52.6%", "15 spots", "Search hearths & fire pits to bank 15x Charcoal early for Q4"),
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 spots", "Workshop corners in Sarlat military battery")
        ],
        "steps": [
            "Orient toward Master Granary (West) or Sarlat Village (East).",
            "Loot Flour Sacks (47.6%) and Oak Barrels (38.5%) until reaching 20x Flour.",
            "Sweep fireplaces for 15x Charcoal (52.6%) and Bullion Boxes (Gold) for Opium Pipe.",
            "Extract via designated match extraction gate and return to Château."
        ],
        "post_raid": "Hand in 20x Flour to Eloise -> Unlocks Quest 3: The Gavroche Family.",
        "roadmap": [
            {"quest": "Quest 2 & 4: Bakery & Fuel", "items": [("20x Flour", "flour.png"), ("15x Charcoal", "charcoal.png")]},
            {"quest": "Bribery: Mr Sweet Smuggling", "items": [("1x China Bowl", "china_bowl.png"), ("1x Opium Pipe", "opium_pipe.png"), ("1x Opium", "opium.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8 & 9: Finale & Books", "items": [("1x Red Votive Candle", "votive_candle.png"), ("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 2: Jacques Bridge (Differentiated Multiple Turn-Ins: Gavroche Camp + Flour Finish)
    {
        "id": 2,
        "phase": "RAID 2 OF 7  —  EXPEDITION SCOUT & FLOUR FINISH",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: Gavroche Camp  &  Quest 2: Flour Finish",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Gavroche Camp", "master_chest.webp", "Camp Trigger (Q3)", "flour.png", "100%", "Quest 3 Turn-in"),
            ("Flour Sack", "flour_sack.webp", "Flour (Q2)", "flour.png", "47.6%", "Quest 2 Finish"),
            ("Bullion Box", "bullion_box.webp", "Opium Pipe", "opium_pipe.png", "13.7%", "Hardest Drop (Gold)"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Upcoming Stash (Q6)"),
            ("Pile of Ash", "pile_of_ash.webp", "Charcoal (Q4)", "charcoal.png", "52.6%", "Upcoming Stash (Q4)")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 220, 'target_x': 590, 'target_y': 380,
                'color': (0, 229, 255),
                'title': "Gavroche Family Camp",
                'count_text': "Camp Perimeter (X: 1479, Y: 313)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'master_chest.webp',
                'item_img': 'flour.png',
                'sub_text': "Walk directly into perimeter on lower deck"
            },
            {
                'box_x': 1050, 'box_y': 440, 'target_x': 830, 'target_y': 620,
                'color': (0, 229, 255),
                'title': "Bridge Tower Granary Lofts",
                'count_text': "8x Flour Sacks (Finish 20x Goal)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'flour_sack.webp',
                'item_img': 'flour.png',
                'sub_text': "Check top levels of North Bridge towers"
            },
            {
                'box_x': 450, 'box_y': 780, 'target_x': 820, 'target_y': 690,
                'color': (255, 234, 0),
                'title': "Fortress Guardhouse Bullion",
                'count_text': "4x Bullion Boxes · 8x Tool Bins",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'bullion_box.webp',
                'item_img': 'saltpetre.png',
                'sub_text': "Guardhouse desks & workshop tooling bins"
            }
        ],
        # DIFFERENTIATED MULTIPLE QUEST PRIORITIES!
        "priority_1_list": [
            {
                "tag": "PRIORITY 1A: QUEST TURN-IN (QUEST 3 — THE GAVROCHE FAMILY)",
                "title": "Scout Gavroche Family Camp",
                "cont_title": "Camp Perimeter (Lower Deck)",
                "cont_img": "master_chest.webp",
                "item_img": "flour.png",
                "drop_rate": "100%",
                "density": "Instant Trigger (X: 1479, Y: 313)",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Walk directly into the camp perimeter on the lower bridge deck to complete Quest 3."
            },
            {
                "tag": "PRIORITY 1B: QUEST GATHERING (QUEST 2 — FLOUR COMPLETION)",
                "title": "Gather Remaining 20x Flour",
                "cont_title": "Bridge Tower Sacks & Barrels",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "12 spots in bridge towers",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Finish any remaining Flour from Bridge tower storerooms to ready the hand-in."
            }
        ],
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "8 open spots", "Guardhouse desks on Jacques Bridge road"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "3 open spots", "Tower living quarters and tollhouse offices")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "8 spots", "Workshop corners in fortress guardhouse"),
            ("Pile of Ash", "pile_of_ash.webp", "15x Charcoal (Q4)", "charcoal.png", "52.6%", "10 spots", "Carriage house and guardhouse fireplaces")
        ],
        "steps": [
            "Check bridge spawn and navigate to Gavroche Family Camp (X: 1479, Y: 313) to trigger Quest 3.",
            "Loot Bridge tower storerooms to complete 20x Flour.",
            "Sweep Fortress Guardhouse Bullion Boxes for Opium Pipe and Tooling Bins for Saltpetre.",
            "Extract safely via open bridge extraction gate."
        ],
        "post_raid": "Return to Chateau -> Hand in Quest 3 to Eloise -> Unlocks Quest 4: Fuel for the Fire.",
        "roadmap": [
            {"quest": "Quest 2 & 4: Bakery & Fuel", "items": [("20x Flour", "flour.png"), ("15x Charcoal", "charcoal.png")]},
            {"quest": "Bribery: Mr Sweet Smuggling", "items": [("1x China Bowl", "china_bowl.png"), ("1x Opium Pipe", "opium_pipe.png"), ("1x Opium", "opium.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8 & 9: Finale & Books", "items": [("1x Red Votive Candle", "votive_candle.png"), ("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 3: Sarlat Farm (Fuel for Fire & Bribery Sweep)
    {
        "id": 3,
        "phase": "RAID 3 OF 7  —  FUEL HARVEST & BRIBERY SWEEP",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 4: Fuel for the Fire",
        "key_status": ("KEYS: NONE NEEDED (0 KEYS REQUIRED)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Pile of Ash", "pile_of_ash.webp", "15x Charcoal (Q4)", "charcoal.png", "52.6%", "Primary Objective"),
            ("Bullion Box", "bullion_box.webp", "Opium Pipe", "opium_pipe.png", "13.7%", "Hardest Drop (Gold)"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl", "china_bowl.png", "16.1%", "Hardest Drop (Gold)"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Upcoming Stash (Q6)")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 240, 'target_x': 520, 'target_y': 420,
                'color': (0, 229, 255),
                'title': "Master Granary Fireplaces",
                'count_text': "6x Ash Piles (15x Charcoal Goal)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'pile_of_ash.webp',
                'item_img': 'charcoal.png',
                'sub_text': "Sweep living quarters hearths & woodstoves"
            },
            {
                'box_x': 1050, 'box_y': 440, 'target_x': 960, 'target_y': 590,
                'color': (255, 234, 0),
                'title': "Sarlat Village Bullion & Ash",
                'count_text': "8x Bullion Boxes · 9x Ash Piles",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'bullion_box.webp',
                'item_img': 'opium_pipe.png',
                'sub_text': "Opium Pipe sweep + Wall Cabinets"
            }
        ],
        "priority_1_list": [
            {
                "tag": "PRIORITY 1: RAID OBJECTIVE (THIS MATCH)",
                "title": "Quest 4: Gather 15x Charcoal",
                "cont_title": "Pile of Ash / Fireplace",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png",
                "drop_rate": "52.6%",
                "density": "15 open spots",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. Found in hearths and stoves in every Sarlat farmhouse."
            }
        ],
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "12 open spots", "Check bedroom nightstands & desks for Opium Pipe!"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Check farmhouse & church walls for China Bowl!")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 spots", "Workshop corners in Sarlat military battery"),
            ("Flour Sack", "flour_sack.webp", "Damp Rags (Q6)", "damp_rag.png", "32.4%", "30 spots", "Grab Damp Rags for Quest 6")
        ],
        "steps": [
            "Sweep Master Granary hearths or Village kitchens for 15x Charcoal (52.6%).",
            "Actively check every Bullion Box for the rare Opium Pipe (13.7%).",
            "Inspect wall cabinets for the China Bowl (16.1%).",
            "Extract safely and return to Château."
        ],
        "post_raid": "Hand in 15x Charcoal to Eloise -> Unlocks Quest 5: Safe Conduct.",
        # Quest 2 (Flour) is REMOVED!
        "roadmap": [
            {"quest": "Quest 4: Fuel for Fire (Active)", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Bribery: Mr Sweet Smuggling", "items": [("1x China Bowl", "china_bowl.png"), ("1x Opium Pipe", "opium_pipe.png"), ("1x Opium", "opium.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8 & 9: Finale & Books", "items": [("1x Red Votive Candle", "votive_candle.png"), ("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Sarlat Farm (Differentiated Multiple Turn-Ins: Red Candle + Bribery to Mr Sweet)
    {
        "id": 4,
        "phase": "RAID 4 OF 7  —  SHADOWS SANCTUARY & BRIBERY FINISH",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8: Red Candle  &  Bribery Turn-In",
        "key_status": ("QUEST OBJECTIVE (0 KEYS REQUIRED)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Chapel Altar", "chapel_altar.webp", "Red Candle (Q8)", "votive_candle.png", "100%", "Quest 8 Objective"),
            ("Mr Sweet Hub", "master_chest.webp", "Bribery Hand-in", "china_bowl.png", "100%", "Bribery Turn-In"),
            ("Bullion Box", "bullion_box.webp", "Opium Pipe", "opium_pipe.png", "13.7%", "Hardest Drop (Gold)"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Upcoming Stash (Q6)")
        ],
        "callouts": [
            {
                'box_x': 900, 'box_y': 780, 'target_x': 1230, 'target_y': 870,
                'color': (0, 229, 255),
                'title': "Chapel of Weeping Virgins",
                'count_text': "1x Red Votive Candle (Active Q8)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'chapel_altar.webp',
                'item_img': 'votive_candle.png',
                'sub_text': "Located on front bench/altar table (OPEN)"
            },
            {
                'box_x': 500, 'box_y': 520, 'target_x': 700, 'target_y': 750,
                'color': (255, 234, 0),
                'title': "Farmstead Bribery Finish",
                'count_text': "Opium Pipe & China Bowl Sweep",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'bullion_box.webp',
                'item_img': 'china_bowl.png',
                'sub_text': "Check Wall Cabinets & nightstands"
            }
        ],
        # DIFFERENTIATED MULTIPLE QUEST PRIORITIES!
        "priority_1_list": [
            {
                "tag": "PRIORITY 1A: QUEST OBJECTIVE (QUEST 8 — PUSHING BACK THE SHADOWS)",
                "title": "Retrieve Red Votive Candle",
                "cont_title": "Chapel Altar / Bench",
                "cont_img": "chapel_altar.webp",
                "item_img": "votive_candle.png",
                "drop_rate": "100%",
                "density": "1 spot (Active Q8)",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. Resting on chapel altar/bench in Chapel of Weeping Virgins."
            },
            {
                "tag": "PRIORITY 1B: QUEST TURN-IN (MR SWEET BRIBERY QUEST)",
                "title": "Deliver China Bowl, Opium Pipe & Opium",
                "cont_title": "Mr Sweet (Outer Ramparts)",
                "cont_img": "master_chest.webp",
                "item_img": "china_bowl.png",
                "drop_rate": "100%",
                "density": "Hand-in upon extraction",
                "spawn_info": "100% Guaranteed Hand-In",
                "desc": "Turn in the 3 contraband items to Mr Sweet in the Outer Ramparts hub to unlock Mount Sinai."
            }
        ],
        "hardest_targets": [
            ("Bullion / Jewellery Box", "bullion_box.webp", "Opium Pipe (Bribery)", "opium_pipe.png", "13.7%", "12 open spots", "Final chance for Opium Pipe on Sarlat!"),
            ("Wall Cabinet", "wall_cabinet.webp", "China Bowl (Bribery)", "china_bowl.png", "16.1%", "4 open spots", "Final check for China Bowl on Sarlat!")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 spots", "Workshop corners in Sarlat military battery"),
            ("Flour Sack", "flour_sack.webp", "5x Damp Rag (Q6)", "damp_rag.png", "32.4%", "30 spots", "Gather Damp Rags to finish Quest 6 early")
        ],
        "steps": [
            "Infiltrate Chapel of Weeping Virgins (South-East hill).",
            "Loot Red Votive Candle directly from chapel altar table (100% guaranteed).",
            "Sweep nearby village farmhouses for remaining Bribery items (Opium Pipe/Bowl).",
            "Extract safely and return to Château."
        ],
        "post_raid": "Hand in Candle to Eloise + Hand in Bribes to Mr Sweet -> Unlocks Quest 9: Down From Mount Sinai!",
        "roadmap": [
            {"quest": "Bribery: Mr Sweet Smuggling (Active)", "items": [("1x China Bowl", "china_bowl.png"), ("1x Opium Pipe", "opium_pipe.png"), ("1x Opium", "opium.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows (Active)", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: Mount Sinai (7 Books)", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 5: Sarlat Farm (Mount Sinai - Part 1: Sarlat Books 1, 2, 3)
    {
        "id": 5,
        "phase": "RAID 5 OF 7  —  MOUNT SINAI (SARLAT BOOKS 1, 2, 3)",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Part 1)",
        "key_status": ("KEYS: NONE NEEDED (ALL OPEN WORLD)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Ledger Desk", "ledger_desk.webp", "Book 1: Rozier", "book_rozier.png", "100%", "Windmill Platform"),
            ("Bedroom Table", "ledger_desk.webp", "Book 2: Catéchisme", "book_catechisme.png", "100%", "Farmhouse Bedroom"),
            ("Château Table", "ledger_desk.webp", "Book 3: Rondelet", "book_rondelet.png", "100%", "Château Terrace"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Upcoming Stash (Q6)")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 220, 'target_x': 710, 'target_y': 280,
                'color': (0, 229, 255),
                'title': "Book 3: Rondelet Fish",
                'count_text': "Château Terrace Table (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_rondelet.png',
                'sub_text': "North Chateau upper terrace"
            },
            {
                'box_x': 500, 'box_y': 620, 'target_x': 740, 'target_y': 800,
                'color': (0, 229, 255),
                'title': "Book 2: Catéchisme",
                'count_text': "Farmhouse Bedroom (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_catechisme.png',
                'sub_text': "Nightstand next to bed"
            },
            {
                'box_x': 900, 'box_y': 1000, 'target_x': 800, 'target_y': 1140,
                'color': (0, 229, 255),
                'title': "Book 1: Cours d'Agriculture",
                'count_text': "Windmill Platform (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_rozier.png',
                'sub_text': "South Windmill upper wooden platform"
            }
        ],
        "priority_1_list": [
            {
                "tag": "PRIORITY 1: RAID OBJECTIVE (MOUNT SINAI — SARLAT BOOKS 1, 2, 3)",
                "title": "Retrieve Books 1, 2, 3 (Sarlat Farm)",
                "cont_title": "Desks, Nightstands & Platforms",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "3 Open World Spots",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. All 3 tomes are in open structures — zero keys required!"
            }
        ],
        "hardest_targets": [
            ("Book 1: Rozier", "ledger_desk.webp", "Cours d'Agriculture", "book_rozier.png", "100%", "Windmill", "Upper platform inside the South Windmill (OPEN)"),
            ("Book 2: Catéchisme", "ledger_desk.webp", "Catéchisme Moral", "book_catechisme.png", "100%", "Farmhouse", "Bedroom nightstand in central farmhouse (OPEN)"),
            ("Book 3: Rondelet", "ledger_desk.webp", "Histoire des Poissons", "book_rondelet.png", "100%", "Château", "Terrace table on Château grounds (OPEN)")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "13 spots", "Workshop corners in Sarlat military battery"),
            ("Flour Sack", "flour_sack.webp", "10x Tallow Balm (Q6)", "tallow_balm.png", "15.0%", "30 spots", "Grab Balm from pantry cabinets")
        ],
        "steps": [
            "Deploy onto Sarlat Farm with 0 keys in inventory.",
            "Book 1: Loot 'Cours d'Agriculture' on South Windmill platform (X: 1968, Y: 3349).",
            "Book 2: Loot 'Catéchisme' from farmhouse bedroom nightstand (X: 1817, Y: 2280).",
            "Book 3: Loot 'Histoire des Poissons' from Château terrace table (X: 1729, Y: 729).",
            "Store all 3 books safely in secure pouch and extract."
        ],
        "post_raid": "Deposit Books 1-3 into Chateau Stash -> Deploy to Jacques Bridge for Books 4 & 5.",
        "roadmap": [
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 9: Mount Sinai - Part 1 (Active)", "items": [("Book 1: Rozier", "book_rozier.png"), ("Book 2: Catéchisme", "book_catechisme.png"), ("Book 3: Rondelet", "book_rondelet.png")]},
            {"quest": "Quest 9: Upcoming Bridge & Forest", "items": [("Books 4 & 5 (Bridge)", "book_buffon.png"), ("Books 6 & 7 (Forest)", "book_census.png")]}
        ]
    },

    # RAID 6: Jacques Bridge (Mount Sinai - Part 2: Bridge Books 4 & 5)
    {
        "id": 6,
        "phase": "RAID 6 OF 7  —  MOUNT SINAI (BRIDGE BOOKS 4 & 5)",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Part 2)",
        "key_status": ("KEYS: NONE NEEDED (ALL OPEN WORLD)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Bridge Tower Desk", "ledger_desk.webp", "Book 4: Montesquieu", "book_montesquieu.png", "100%", "Bridge Tower (Open)"),
            ("Carriage House", "ledger_desk.webp", "Book 5: Buffon", "book_buffon.png", "100%", "Carriage House (Open)"),
            ("Bullion Box", "bullion_box.webp", "Silver Currency", "bullion_box.webp", "100%", "Guardhouse Desks"),
            ("Tooling Bin", "tooling_bin.webp", "Saltpetre (Q6)", "saltpetre.png", "18.9%", "Fortress Battery")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 380, 'target_x': 570, 'target_y': 550,
                'color': (0, 229, 255),
                'title': "Book 4: Montesquieu",
                'count_text': "Bridge Tower Top Desk (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_montesquieu.png',
                'sub_text': "Top desk inside Jacques Bridge Tower"
            },
            {
                'box_x': 1050, 'box_y': 440, 'target_x': 850, 'target_y': 480,
                'color': (0, 229, 255),
                'title': "Book 5: Buffon History",
                'count_text': "Carriage House Fireplace (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_buffon.png',
                'sub_text': "Resting on fireplace mantle board"
            }
        ],
        "priority_1_list": [
            {
                "tag": "PRIORITY 1: RAID OBJECTIVE (MOUNT SINAI — BRIDGE BOOKS 4 & 5)",
                "title": "Retrieve Books 4 & 5 (Jacques Bridge)",
                "cont_title": "Bridge Tower & Carriage House",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_buffon.png",
                "drop_rate": "100%",
                "density": "2 Open Spots",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. Both books are in open structures — NO locked doors or Silver Keys needed!"
            }
        ],
        "hardest_targets": [
            ("Book 4: Montesquieu", "ledger_desk.webp", "Spirit of the Laws", "book_montesquieu.png", "100%", "Bridge Tower", "On the top desk inside the Jacques Bridge Tower (OPEN)"),
            ("Book 5: Buffon History", "ledger_desk.webp", "Natural History", "book_buffon.png", "100%", "Carriage House", "On the fireplace board in Carriage House (OPEN)")
        ],
        "upcoming_targets": [
            ("Tooling Bin", "tooling_bin.webp", "20x Saltpetre (Q6)", "saltpetre.png", "18.9%", "8 spots", "Workshop corners in fortress guardhouse"),
            ("Bullion Box", "bullion_box.webp", "Silver / Currency", "bullion_box.webp", "100%", "4 spots", "Guardhouse desks on Jacques Bridge road")
        ],
        "steps": [
            "Deploy onto Jacques Bridge with 0 keys in your inventory.",
            "Book 4: Loot 'The Spirit of the Laws - Montesquieu' from top desk in Bridge Tower (X: 1391, Y: 1535).",
            "Book 5: Loot 'Natural History - Buffon' from fireplace board in Carriage House (X: 2094, Y: 1346).",
            "Deposit both books safely into your secure pouch.",
            "Navigate to whichever extraction gate is currently open on your timer and extract safely."
        ],
        "post_raid": "Deposit Books 4 & 5 into stash -> Deploy to Sombre Forest for final Books 6 & 7.",
        "roadmap": [
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 9: Mount Sinai - Part 2 (Active)", "items": [("Book 4: Montesquieu", "book_montesquieu.png"), ("Book 5: Buffon", "book_buffon.png")]},
            {"quest": "Quest 9: Final Forest Books", "items": [("Books 6 & 7 (Forest Finale)", "book_census.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Mount Sinai - Part 3: Forest Books 6 & 7 Finale)
    {
        "id": 7,
        "phase": "RAID 7 OF 7  —  MOUNT SINAI FINALE (FOREST BOOKS 6 & 7)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 9: Down From Mount Sinai (Finale)",
        "key_status": ("KEYS: NONE NEEDED (ALL OPEN WORLD)", (0, 229, 255), (10, 15, 26)),
        "legend": [
            ("Hunters Lodge", "ledger_desk.webp", "Book 6: Census", "book_census.png", "100%", "Lodge Main Table"),
            ("Forest Mill", "ledger_desk.webp", "Book 7: Paracelsus", "book_buffon.png", "100%", "Mill Wood Table"),
            ("Ramparts Merchant", "sack.webp", "Final Supplies", "flour.png", "100%", "Camp Merchants"),
            ("Forest Sack", "sack.webp", "Loose Stash", "saltpetre.png", "25.0%", "Surface Stash")
        ],
        "callouts": [
            {
                'box_x': 500, 'box_y': 620, 'target_x': 770, 'target_y': 780,
                'color': (0, 229, 255),
                'title': "Book 6: Census of 1680",
                'count_text': "Hunters Lodge Desk (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_census.png',
                'sub_text': "Inside Hunters Lodge on main table"
            },
            {
                'box_x': 1050, 'box_y': 650, 'target_x': 1110, 'target_y': 800,
                'color': (0, 229, 255),
                'title': "Book 7: Paracelsus Hermetic",
                'count_text': "Forest Mill Worktable (OPEN)",
                'spawn_badge': "100% GUARANTEED",
                'is_100': True,
                'cont_img': 'ledger_desk.webp',
                'item_img': 'book_buffon.png',
                'sub_text': "On wood worktable inside Forest Mill"
            }
        ],
        "priority_1_list": [
            {
                "tag": "PRIORITY 1: RAID OBJECTIVE (MOUNT SINAI FINALE — BOOKS 6 & 7)",
                "title": "Retrieve Books 6 & 7 (Sombre Forest)",
                "cont_title": "Hunters Lodge & Forest Mill",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_census.png",
                "drop_rate": "100%",
                "density": "2 Open Spots",
                "spawn_info": "100% Guaranteed Spawn Rate",
                "desc": "Primary quest requirement. Both books are in open structures — NO locked doors or Gold Keys needed!"
            }
        ],
        "hardest_targets": [
            ("Book 6: Census", "ledger_desk.webp", "Census of 1680", "book_census.png", "100%", "Hunters Lodge", "On the main table inside Hunters Lodge (OPEN)"),
            ("Book 7: Paracelsus", "ledger_desk.webp", "Paracelsus Hermetic", "book_buffon.png", "100%", "Forest Mill", "On the wood table inside Forest Mill (OPEN)")
        ],
        "upcoming_targets": [
            ("Outer Ramparts Merchants", "sack.webp", "Final Supplies", "flour.png", "100%", "Encampment", "Check Louis & Piro for final ammunition and supplies"),
            ("Forest Sacks", "sack.webp", "Loose Stash", "saltpetre.png", "25.0%", "8 spots", "Surface sacks along forest path")
        ],
        "steps": [
            "Deploy into Sombre Forest with 0 keys in your inventory.",
            "Book 6: Loot 'Census of 1680' from main table in Hunters Lodge (X: 1888, Y: 2244).",
            "Book 7: Loot 'Paracelsus Hermetic' from wood table in Forest Mill (X: 2755, Y: 2314).",
            "Ensure all 7 books across the entire questline are safely stored in your secure pouch.",
            "Extract safely via nearest open forest extraction portal."
        ],
        "post_raid": "Hand in all 7 Mount Sinai books to Eloise -> Unlocks Quest 10: The Crossing (Grand Finale)!",
        "roadmap": [
            {"quest": "Quest 9: Mount Sinai - Finale (Active)", "items": [("Book 6: Census of 1680", "book_census.png"), ("Book 7: Paracelsus Hermetic", "book_buffon.png")]},
            {"quest": "Quest 10: The Crossing (Finale)", "items": [("Grand Finale Crossing Unlocked!", "gold_key.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (15, 23, 42))
    draw = ImageDraw.Draw(canvas)
    
    # 1. TOP HEADER BAR (Compact 72px)
    draw.rectangle([0, 0, CANVAS_W, 72], fill=(11, 15, 25))
    draw.line([0, 72, CANVAS_W, 72], fill=(51, 65, 85), width=2)
    
    draw.text((20, 10), cfg["phase"], fill=(255, 230, 0), font=F_HEADER_TAG)
    draw.text((20, 32), f"{cfg['quest_name']}  —  {cfg['map_name']}", fill=(255, 255, 255), font=F_HEADER_TITLE)
    
    # Key Badge (Uniform styling)
    badge_text, bg_col, text_col = cfg["key_status"]
    bw = int(draw.textlength(badge_text, font=F_HEADER_TAG)) + 36
    bx = CANVAS_W - bw - 20
    draw.rounded_rectangle([bx, 12, bx+bw, 58], radius=8, fill=bg_col, outline=(255, 255, 255), width=2)
    draw.text((bx+18, 22), badge_text, fill=text_col, font=F_HEADER_TAG)
    
    # 2. LEFT MAP PANEL
    raw_map = Image.open(cfg["map_img"]).convert("RGB")
    map_resized = raw_map.resize((MAP_W, MAP_H), Image.Resampling.LANCZOS)
    canvas.paste(map_resized, (MAP_X, MAP_Y))
    draw.rectangle([MAP_X-2, MAP_Y-2, MAP_X+MAP_W+2, MAP_Y+MAP_H+2], outline=(90, 110, 140), width=3)
    
    # Render Enhanced Legend with colored drop rate numbers and outline guide
    core.render_tactical_legend(draw, canvas, cfg.get("legend", []))
    
    # Render Raw Points as Small Dots (Radius ~5px)
    raw_points = loot.get_map_loot(cfg["map_name"])
    for pt in raw_points:
        mx, my = to_map_coord(pt['x'], pt['y'])
        r = 5
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=pt['color'], outline=(20, 30, 45), width=1)
        
    # Render Cluster Summary Callouts showing BOTH Container & Item images!
    for callout in cfg.get("callouts", []):
        core.render_summary_callout(draw, canvas, callout)
        
    # 3. RIGHT BRIEFING PANEL (Fits whole side seamlessly)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=(15, 20, 30), outline=(51, 65, 85), width=2)
    
    cur_y = PANEL_Y + 14
    
    # ==========================================
    # PRIORITY 1: RAID OBJECTIVES (DIFFERENTIATED MULTI-QUEST CARDS!)
    # ==========================================
    for p in cfg.get("priority_1_list", []):
        draw.text((PANEL_X+18, cur_y), p.get("tag", "PRIORITY 1: RAID OBJECTIVE (THIS MATCH)"), fill=(0, 229, 255), font=F_SECTION_TITLE)
        cur_y += 24
        
        p_box_h = 92
        draw.rounded_rectangle([PANEL_X+18, cur_y, PANEL_X+PANEL_W-18, cur_y+p_box_h], radius=8, fill=(18, 30, 48), outline=(0, 229, 255), width=2)
        
        # Container image
        c_img = core.CONTAINER_IMGS.get(p["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, cur_y+12, 68, 68), bg_color=(10, 16, 28), border_color=(0, 229, 255), border_w=2)
        
        # Target item image
        i_img = core.ITEM_IMGS.get(p["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+84, cur_y+38, 40, 40), bg_color=(10, 16, 28), border_color=(70, 85, 105), border_w=1)
        
        tx = PANEL_X + 134
        draw.text((tx, cur_y+8), f"{p['title']}", fill=(255, 255, 255), font=F_CARD_TITLE)
        
        # Spawn certainty badge
        draw.rounded_rectangle([tx, cur_y+32, tx+150, cur_y+48], radius=4, fill=(16, 185, 129))
        draw.text((tx+6, cur_y+34), p.get("spawn_info", "100% Guaranteed"), fill=(255, 255, 255), font=F_BADGE)
        
        # Drop rate in colored font
        r_col = core.get_rate_color(p['drop_rate'])
        draw.text((tx+160, cur_y+32), f"Drop Rate: {p['drop_rate']}", fill=r_col, font=F_BODY_BOLD)
        draw.text((tx+290, cur_y+32), f"•  {p['density']}", fill=(0, 229, 255), font=F_BODY)
        
        draw.text((tx, cur_y+54), p["desc"][:78], fill=(200, 215, 235), font=F_BODY)
        cur_y += p_box_h + 12
        
    cur_y += 4
    
    # ==========================================
    # PRIORITY 2: HARDEST DROPS (COLOR: BRIGHT GOLD #FFEA00)
    # ==========================================
    draw.text((PANEL_X+18, cur_y), "PRIORITY 2: HARDEST DROP RATES (RARE ITEMS)", fill=(255, 234, 0), font=F_SECTION_TITLE)
    cur_y += 24
    
    for c_title, c_icon, i_title, i_icon, rate, spots, note in cfg["hardest_targets"]:
        h_box_h = 68
        draw.rounded_rectangle([PANEL_X+18, cur_y, PANEL_X+PANEL_W-18, cur_y+h_box_h], radius=6, fill=(28, 26, 16), outline=(255, 234, 0), width=2)
        
        c_im = core.CONTAINER_IMGS.get(c_icon)
        core.paste_icon_safe(canvas, c_im, (PANEL_X+26, cur_y+8, 52, 52), bg_color=(15, 15, 10), border_color=(255, 234, 0), border_w=2)
        i_im = core.ITEM_IMGS.get(i_icon)
        core.paste_icon_safe(canvas, i_im, (PANEL_X+66, cur_y+26, 32, 32), bg_color=(20, 20, 12), border_color=(70, 85, 105), border_w=1)
        
        hx = PANEL_X + 108
        draw.text((hx, cur_y+6), f"{c_title}  —  {i_title}", fill=(255, 255, 255), font=F_BODY_BOLD)
        
        r_col = core.get_rate_color(rate)
        draw.text((hx, cur_y+26), f"Drop Rate: {rate}", fill=r_col, font=F_BODY_BOLD)
        draw.text((hx+130, cur_y+26), f"•  Spots: {spots}", fill=(255, 234, 0), font=F_BODY)
        draw.text((hx, cur_y+46), note[:80], fill=(210, 220, 235), font=F_SMALL)
        
        cur_y += h_box_h + 8
        
    cur_y += 4
    
    # ==========================================
    # PRIORITY 3: UPCOMING QUEST ITEMS (COLOR: EMERALD #10B981)
    # ==========================================
    draw.text((PANEL_X+18, cur_y), "PRIORITY 3: UPCOMING QUEST ITEMS (PRE-BANKING)", fill=(16, 185, 129), font=F_SECTION_TITLE)
    cur_y += 24
    
    for c_title, c_icon, i_title, i_icon, rate, spots, note in cfg["upcoming_targets"]:
        u_box_h = 66
        draw.rounded_rectangle([PANEL_X+18, cur_y, PANEL_X+PANEL_W-18, cur_y+u_box_h], radius=6, fill=(16, 28, 24), outline=(16, 185, 129), width=2)
        
        c_im = core.CONTAINER_IMGS.get(c_icon)
        core.paste_icon_safe(canvas, c_im, (PANEL_X+26, cur_y+8, 50, 50), bg_color=(10, 20, 16), border_color=(16, 185, 129), border_w=2)
        i_im = core.ITEM_IMGS.get(i_icon)
        core.paste_icon_safe(canvas, i_im, (PANEL_X+66, cur_y+26, 32, 32), bg_color=(12, 24, 18), border_color=(70, 85, 105), border_w=1)
        
        ux = PANEL_X + 108
        draw.text((ux, cur_y+6), f"{c_title}  —  {i_title}", fill=(255, 255, 255), font=F_BODY_BOLD)
        
        r_col = core.get_rate_color(rate)
        draw.text((ux, cur_y+26), f"Drop Rate: {rate}", fill=r_col, font=F_BODY_BOLD)
        draw.text((ux+130, cur_y+26), f"•  Spots: {spots}", fill=(16, 185, 129), font=F_BODY)
        draw.text((ux, cur_y+46), note[:80], fill=(210, 220, 235), font=F_SMALL)
        
        cur_y += u_box_h + 8

    cur_y += 6

    # ==========================================
    # EXECUTION STEPS (LARGE BOLD FONT)
    # ==========================================
    draw.text((PANEL_X+18, cur_y), "SPAWN-INDEPENDENT EXECUTION STEPS", fill=(255, 230, 0), font=F_SECTION_TITLE)
    cur_y += 24
    
    for i, step in enumerate(cfg["steps"], 1):
        draw.ellipse([PANEL_X+20, cur_y+2, PANEL_X+42, cur_y+24], fill=(0, 112, 244))
        draw.text((PANEL_X+27, cur_y+3), str(i), fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+48, cur_y+4), step[:85], fill=(240, 245, 255), font=F_BODY)
        cur_y += 26
        
    cur_y += 8
    
    # ==========================================
    # POST-RAID ACTION & HAND-IN PROTOCOL
    # ==========================================
    draw.rounded_rectangle([PANEL_X+18, cur_y, PANEL_X+PANEL_W-18, cur_y+54], radius=8, fill=(10, 36, 24), outline=(16, 185, 129), width=2)
    draw.text((PANEL_X+28, cur_y+5), "POST-RAID ACTION & HAND-IN PROTOCOL", fill=(16, 185, 129), font=F_BODY_BOLD)
    draw.text((PANEL_X+28, cur_y+26), cfg["post_raid"][:85], fill=(255, 255, 255), font=F_BODY_BOLD)
    cur_y += 66
    
    # ==========================================
    # COMPLETE QUESTLINE STASH ROADMAP (PROGRESSIVE & SEPARATED!)
    # ==========================================
    draw.text((PANEL_X+18, cur_y), "UPCOMING QUEST STASH ROADMAP (REMAINING ITEMS)", fill=(255, 255, 255), font=F_SECTION_TITLE)
    cur_y += 24
    
    for r_card in cfg.get("roadmap", []):
        card_h = 38
        draw.rounded_rectangle([PANEL_X+18, cur_y, PANEL_X+PANEL_W-18, cur_y+card_h], radius=6, fill=(20, 26, 38), outline=(51, 65, 85), width=1)
        draw.text((PANEL_X+24, cur_y+10), r_card["quest"], fill=(255, 230, 0), font=F_BODY_BOLD)
        
        item_x = PANEL_X + 270
        for item_name, item_ico in r_card["items"]:
            ico_im = core.ITEM_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, cur_y+6, 26, 26), bg_color=(12, 18, 28))
            draw.text((item_x+32, cur_y+10), item_name, fill=(255, 255, 255), font=F_BODY_BOLD)
            item_x += int(draw.textlength(item_name, font=F_BODY_BOLD)) + 45
            
        cur_y += card_h + 6

    # Save final artifact image
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

print("Generating all 7 perfect V7 briefings...")
for cfg in RAIDS_CONFIG:
    render_briefing(cfg)
print("All 7 V7 briefings generated successfully!")
