import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v12 as core

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

COLOR_SACK = core.COLOR_SACK
COLOR_BULLION = core.COLOR_BULLION
COLOR_CABINET = core.COLOR_CABINET
COLOR_ASH = core.COLOR_ASH
COLOR_TOOLING = core.COLOR_TOOLING
COLOR_STORY = core.COLOR_STORY

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
        "grouped_turnin_label": "ACTIVE: Q2 MAKING DOUGH",
        "story_pois": [],
        "active_objectives": [
            {
                "title": "Quest 2: Gather 20x Flour",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Flour Sack / Oak Barrel",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "40 total sacks in Master Granary & Village",
                "desc": "Primary quest requirement. Abundant in all farmhouses & granaries across Sarlat."
            }
        ],
        "contraband_sweep": {
            "title": "CHECK EVERY RAID: CONTRABAND (UNLOCKS MOUNT SINAI)",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Desks & Nightstands (40 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Living Quarters Walls (4 spots)"}
        },
        "directory": [
            {"shape": "circle", "color": COLOR_SACK, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "20x Flour", "i_ico": "flour.png", "loc": "WEST MAP: Master Granary — 18 Spots (1st/2nd floor)", "rate": "47.6%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "20x Flour", "i_ico": "flour.png", "loc": "EAST MAP: Village Granaries & Barrels — 14 Spots", "rate": "47.6%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "CENTER: Farmhouse Bedroom Desks — 22 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "WALLS: Farmhouse & Church Walls — 4 Spots", "rate": "16.1%"},
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "loc": "HEARTHS: Living Quarters Stoves & Hearths — 14 Spots", "rate": "52.6%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "SOUTH-EAST: Military Battery Workshops — 13 Spots", "rate": "18.9%"}
        ],
        "steps": [
            "Orient toward Master Granary (West) or Village Granaries (East).",
            "Loot Flour Sacks (47.6%) until securing 20x Flour in secure inventory.",
            "Sweep bedroom Bullion Boxes (Purple ◆) for Opium Pipe & Wall Cabinets (Blue ■) for China Bowl.",
            "Extract via designated match extraction gate and return to Château."
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 2: Jacques Bridge (Gavroche Camp & Flour Finish - GROUPED TURN-IN!)
    {
        "id": 2,
        "phase": "RAID 2 OF 7  —  EXPEDITION SCOUT & FLOUR FINISH",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: Gavroche Camp  &  Quest 2: Flour Finish",
        "grouped_turnin_label": "GROUPED TURN-IN: Q3 GAVROCHE + Q2 FLOUR",
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp (Lower Deck)"}
        ],
        "active_objectives": [
            {
                "title": "Turn-In 1: Scout Gavroche Camp (Quest 3)",
                "npc": "Discover Camp at Jacques Bridge Lower Deck",
                "cont_name": "Camp Perimeter Trigger (X: 1479, Y: 313)",
                "cont_img": "master_chest.webp",
                "item_img": "flour.png",
                "drop_rate": "100%",
                "density": "Instant Discovery Trigger",
                "desc": "Walk directly into the camp perimeter on the lower bridge deck to complete Quest 3."
            },
            {
                "title": "Turn-In 2: Gather Remaining 20x Flour (Quest 2)",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Bridge Tower Sacks & Barrels",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "40 spots in bridge towers",
                "desc": "Finish any remaining Flour from Bridge storerooms to ready the hand-in upon return."
            }
        ],
        "contraband_sweep": {
            "title": "CHECK EVERY RAID: CONTRABAND (UNLOCKS MOUNT SINAI)",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Guardhouse Desks on Bridge Road (28 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Tollhouse & Tower Walls (3 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Gavroche Camp", "c_ico": "master_chest.webp", "item": "Camp Trigger", "i_ico": "flour.png", "loc": "CENTER: Lower Bridge Deck Perimeter (X: 1479, Y: 313)", "rate": "100%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "20x Flour", "i_ico": "flour.png", "loc": "NORTH TOWERS: Bridge Storerooms & Sacks — 12 Spots", "rate": "47.6%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "ROAD DESKS: Fortress Guardhouse Desks — 28 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "TOLLHOUSES: Tower Living Quarters Walls — 3 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "WORKSHOPS: Fortress Battery Corners — 24 Spots", "rate": "18.9%"},
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "loc": "FIREPLACES: Carriage House & Guardhouse — 13 Spots", "rate": "52.6%"}
        ],
        "steps": [
            "Check bridge spawn and navigate to Gavroche Camp (X: 1479, Y: 313) to trigger Quest 3.",
            "Loot Bridge tower storerooms to complete 20x Flour hand-in.",
            "Sweep Fortress Guardhouse Bullion Boxes (Purple ◆) for Opium Pipe and Cabinets (Blue ■) for China Bowl.",
            "Extract safely via open bridge extraction gate."
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 3: Sarlat Farm (Charcoal Finish & Bribery)
    {
        "id": 3,
        "phase": "RAID 3 OF 7  —  FUEL HARVEST & BRIBERY SWEEP",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 4: Last Embers (Charcoal)",
        "grouped_turnin_label": "ACTIVE: Q4 LAST EMBERS",
        "story_pois": [],
        "active_objectives": [
            {
                "title": "Quest 4: Gather 15x Charcoal",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Pile of Ash / Fireplace",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png",
                "drop_rate": "52.6%",
                "density": "14 open hearth spots across farmhouses",
                "desc": "Primary quest requirement. Found in hearths and stoves in every Sarlat farmhouse."
            }
        ],
        "contraband_sweep": {
            "title": "CHECK EVERY RAID: CONTRABAND (UNLOCKS MOUNT SINAI)",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Desks & Nightstands (40 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Living Quarters Walls (4 spots)"}
        },
        "directory": [
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "loc": "HEARTHS: Master Granary & Village Hearths — 14 Spots", "rate": "52.6%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "CENTER: Farmhouse Bedroom Desks — 22 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "WALLS: Farmhouse Walls & Hallways — 4 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "SOUTH-EAST: Military Battery Workshops — 13 Spots", "rate": "18.9%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Old Cabinet", "c_ico": "flour_sack.webp", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "loc": "PANTRY: Living Quarters Old Cabinets — 21 Spots", "rate": "32.4%"}
        ],
        "steps": [
            "Sweep Master Granary hearths or Village kitchens for 15x Charcoal (52.6%).",
            "Actively check every Bullion Box (Purple ◆) for the rare Opium Pipe (13.7%).",
            "Inspect wall cabinets (Blue ■) for the China Bowl (16.1%).",
            "Extract safely and return to Château to hand in Quest 4."
        ],
        "roadmap": [
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Sarlat Farm (Red Candle & Bribery Delivery - GROUPED TURN-IN!)
    {
        "id": 4,
        "phase": "RAID 4 OF 7  —  SHADOWS SANCTUARY & BRIBERY FINISH",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8: Red Candle  &  Bribery Turn-In",
        "grouped_turnin_label": "GROUPED TURN-IN: Q8 CANDLE + BRIBERY",
        "story_pois": [
            {"x": 3048, "y": 2488, "label": "Chapel of Weeping Virgins Altar"}
        ],
        "active_objectives": [
            {
                "title": "Turn-In 1: Retrieve Red Votive Candle (Quest 8)",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Chapel Altar / Bench",
                "cont_img": "chapel_altar.webp",
                "item_img": "votive_candle.png",
                "drop_rate": "100%",
                "density": "1 Spot (X: 3048, Y: 2488)",
                "desc": "Primary quest requirement. Resting on altar bench in Chapel of Weeping Virgins."
            },
            {
                "title": "Turn-In 2: Deliver Contraband to Mr Sweet (Quest 9)",
                "npc": "Deliver 1x China Bowl, 1x Opium Pipe, 1x Opium to Mr Sweet",
                "cont_name": "Mr Sweet Contraband Delivery",
                "cont_img": "master_chest.webp",
                "item_img": "china_bowl.png",
                "drop_rate": "100%",
                "density": "Hub Turn-in upon Extraction",
                "desc": "Turn in contraband to Mr Sweet in Outer Ramparts to unlock Down From Mount Sinai."
            }
        ],
        "contraband_sweep": {
            "title": "FINAL CHECK: SECURE REMAINING CONTRABAND FOR MR SWEET",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Final chance in farmhouse nightstands!"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Final check in church & farmhouse walls!"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Chapel Altar", "c_ico": "chapel_altar.webp", "item": "Red Candle", "i_ico": "votive_candle.png", "loc": "SOUTH-EAST: Chapel of Weeping Virgins Altar (X: 3048, Y: 2488)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "CENTER: Farmhouse Bedroom Desks — 22 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "WALLS: Church & Farmhouse Wall Cupboards — 4 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "SOUTH-EAST: Military Battery Workshops — 13 Spots", "rate": "18.9%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Old Cabinet", "c_ico": "flour_sack.webp", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "loc": "PANTRY: Pantry Cupboards & Shelves — 21 Spots", "rate": "32.4%"}
        ],
        "steps": [
            "Infiltrate Chapel of Weeping Virgins (South-East hill).",
            "Loot Red Votive Candle directly from chapel altar table (100% guaranteed).",
            "Sweep nearby village farmhouses for remaining Bribery items (Opium Pipe/Bowl).",
            "Extract safely and return to Château to turn in Quest 8 & Bribery."
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Part 1)", "items": [("Books 1, 2, 3 (Sarlat)", "book_rozier.png")]},
            {"quest": "Quest 10: Mount Sinai (Part 2)", "items": [("Books 4, 5 (Bridge)", "book_buffon.png")]},
            {"quest": "Quest 10: Mount Sinai (Part 3)", "items": [("Books 6, 7 (Forest)", "book_census.png")]}
        ]
    },

    # RAID 5: Sarlat Farm (Mount Sinai - Part 1: Sarlat Books 1, 2, 3)
    {
        "id": 5,
        "phase": "RAID 5 OF 7  —  MOUNT SINAI (SARLAT BOOKS 1, 2, 3)",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Part 1)",
        "grouped_turnin_label": "ACTIVE: Q10 BOOKS 1, 2, 3",
        "story_pois": [
            {"x": 1968, "y": 3349, "label": "Book 1: Rozier (Windmill)"},
            {"x": 1817, "y": 2280, "label": "Book 2: Catéchisme (Farmhouse)"},
            {"x": 1729, "y": 729, "label": "Book 3: Rondelet (Château)"}
        ],
        "active_objectives": [
            {
                "title": "Retrieve Books 1, 2, 3 (Sarlat Farm)",
                "npc": "Deposit into Chateau Stash (Zero Keys Required)",
                "cont_name": "Windmill, Farmhouse & Château Desks",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "3 Open World Guaranteed Tomes",
                "desc": "Primary quest requirement. All 3 tomes are in open structures — zero keys required!"
            }
        ],
        "contraband_sweep": {
            "title": "OPTIONAL CONTRABAND & VALUABLES SWEEP",
            "bullion": {"item": "Silver Currency", "i_ico": "bullion_box.webp", "rate": "100%", "loc": "Farmhouse Desks & Strongboxes"},
            "cabinet": {"item": "Château Valuables", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Château Private Chambers Walls"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Windmill Desk", "c_ico": "ledger_desk.webp", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "loc": "SOUTH: South Windmill (Upper Wooden Platform - OPEN)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Bedroom Table", "c_ico": "ledger_desk.webp", "item": "Book 2: Catéchisme", "i_ico": "book_catechisme.png", "loc": "CENTER: Farmhouse Bedroom Nightstand (OPEN)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Château Table", "c_ico": "ledger_desk.webp", "item": "Book 3: Rondelet", "i_ico": "book_rondelet.png", "loc": "NORTH: Château Terrace Dining Table (OPEN)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Currency / Silver", "i_ico": "bullion_box.webp", "loc": "CENTER: Farmhouse Bedroom Desks — 22 Spots", "rate": "100%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "Rare Valuables", "i_ico": "china_bowl.png", "loc": "CHÂTEAU: Private Chambers Cupboards — 4 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "Saltpetre & Scrap", "i_ico": "saltpetre.png", "loc": "SOUTH-EAST: Military Battery Workshops — 13 Spots", "rate": "18.9%"}
        ],
        "steps": [
            "Deploy onto Sarlat Farm with 0 keys in inventory.",
            "Book 1: Loot 'Cours d'Agriculture' on South Windmill platform (X: 1968, Y: 3349).",
            "Book 2: Loot 'Catéchisme' from farmhouse bedroom nightstand (X: 1817, Y: 2280).",
            "Book 3: Loot 'Histoire des Poissons' from Château terrace table (X: 1729, Y: 729).",
            "Store all 3 books safely in secure pouch and extract."
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Part 2)", "items": [("Books 4 & 5 (Bridge)", "book_buffon.png")]},
            {"quest": "Quest 10: Mount Sinai (Part 3)", "items": [("Books 6 & 7 (Forest)", "book_census.png")]},
            {"quest": "Quest 11: The Crossing", "items": [("Grand Finale Crossing Unlocked!", "gold_key.png")]}
        ]
    },

    # RAID 6: Jacques Bridge (Mount Sinai - Part 2: Bridge Books 4 & 5)
    {
        "id": 6,
        "phase": "RAID 6 OF 7  —  MOUNT SINAI (BRIDGE BOOKS 4 & 5)",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Part 2)",
        "grouped_turnin_label": "ACTIVE: Q10 BOOKS 4 & 5",
        "story_pois": [
            {"x": 1391, "y": 1535, "label": "Book 4: Montesquieu (Bridge Tower)"},
            {"x": 2094, "y": 1346, "label": "Book 5: Buffon (Carriage House)"}
        ],
        "active_objectives": [
            {
                "title": "Retrieve Books 4 & 5 (Jacques Bridge)",
                "npc": "Deposit into Chateau Stash (Zero Keys Required)",
                "cont_name": "Bridge Tower & Carriage House",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_buffon.png",
                "drop_rate": "100%",
                "density": "2 Open Spots (Zero Keys Needed)",
                "desc": "Primary quest requirement. Both books are in open structures — NO locked doors or Silver Keys needed!"
            }
        ],
        "contraband_sweep": {
            "title": "FORTRESS VALUABLES & SCRAP SWEEP",
            "bullion": {"item": "Silver Currency", "i_ico": "bullion_box.webp", "rate": "100%", "loc": "Guardhouse Desks on Bridge Road (28 spots)"},
            "cabinet": {"item": "Tollhouse Valuables", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Tower Living Quarters Walls (3 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Bridge Tower Desk", "c_ico": "ledger_desk.webp", "item": "Book 4: Montesquieu", "i_ico": "book_montesquieu.png", "loc": "NORTH TOWER: Top Floor Desk inside Tower (OPEN)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Carriage House", "c_ico": "ledger_desk.webp", "item": "Book 5: Buffon", "i_ico": "book_buffon.png", "loc": "SOUTH ROAD: Carriage House Fireplace Mantle (OPEN)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Silver Currency", "i_ico": "bullion_box.webp", "loc": "FORTRESS: Guardhouse Desks on Bridge Road — 28 Spots", "rate": "100%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "Saltpetre & Scrap", "i_ico": "saltpetre.png", "loc": "WORKSHOPS: Fortress Battery Corners — 24 Spots", "rate": "18.9%"}
        ],
        "steps": [
            "Deploy onto Jacques Bridge with 0 keys in your inventory.",
            "Book 4: Loot 'The Spirit of the Laws - Montesquieu' from top desk in Bridge Tower (X: 1391, Y: 1535).",
            "Book 5: Loot 'Natural History - Buffon' from fireplace board in Carriage House (X: 2094, Y: 1346).",
            "Deposit both books safely into your secure pouch.",
            "Navigate to whichever extraction gate is currently open on your timer and extract safely."
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Part 3)", "items": [("Books 6 & 7 (Forest Finale)", "book_census.png")]},
            {"quest": "Quest 11: The Crossing", "items": [("Grand Finale Crossing Unlocked!", "gold_key.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Mount Sinai - Part 3: Forest Books 6 & 7 Finale)
    {
        "id": 7,
        "phase": "RAID 7 OF 7  —  MOUNT SINAI FINALE (FOREST BOOKS 6 & 7)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Finale)",
        "grouped_turnin_label": "ACTIVE: Q10 FINALE BOOKS 6 & 7",
        "story_pois": [
            {"x": 1888, "y": 2244, "label": "Book 6: Census (Hunters Lodge)"},
            {"x": 2755, "y": 2314, "label": "Book 7: Paracelsus (Forest Mill)"}
        ],
        "active_objectives": [
            {
                "title": "Retrieve Books 6 & 7 (Sombre Forest)",
                "npc": "Hand in all 7 books to Eloise to unlock Quest 11",
                "cont_name": "Hunters Lodge & Forest Mill",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_census.png",
                "drop_rate": "100%",
                "density": "2 Open Spots (Zero Keys Needed)",
                "desc": "Primary quest requirement. Both books are in open structures — NO locked doors or Gold Keys needed!"
            }
        ],
        "contraband_sweep": {
            "title": "FOREST CONTRABAND & CAMP MERCHANTS",
            "bullion": {"item": "Silver Currency", "i_ico": "bullion_box.webp", "rate": "100%", "loc": "Encampment Desks (12 spots)"},
            "cabinet": {"item": "Ramparts Supplies", "i_ico": "flour.png", "rate": "100%", "loc": "Outer Ramparts Encampment (Louis & Piro)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Hunters Lodge Table", "c_ico": "ledger_desk.webp", "item": "Book 6: Census", "i_ico": "book_census.png", "loc": "NORTH: Hunters Lodge Main Hall Table (OPEN)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Mill Table", "c_ico": "ledger_desk.webp", "item": "Book 7: Paracelsus", "i_ico": "book_buffon.png", "loc": "EAST: Forest Mill Worktable (OPEN)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Silver Currency", "i_ico": "bullion_box.webp", "loc": "ENCAMPMENT: Forest Desks — 12 Spots", "rate": "100%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Forest Sack", "c_ico": "flour_sack.webp", "item": "Saltpetre & Scrap", "i_ico": "saltpetre.png", "loc": "PATHS: Surface Sacks Along Forest Path — 40 Spots", "rate": "25.0%"}
        ],
        "steps": [
            "Deploy into Sombre Forest with 0 keys in your inventory.",
            "Book 6: Loot 'Census of 1680' from main table in Hunters Lodge (X: 1888, Y: 2244).",
            "Book 7: Loot 'Paracelsus Hermetic' from wood table in Forest Mill (X: 2755, Y: 2314).",
            "Ensure all 7 books across the entire questline are safely stored in your secure pouch.",
            "Extract safely via nearest open forest extraction portal."
        ],
        "roadmap": [
            {"quest": "Quest 11: The Crossing (Grand Finale)", "items": [("Grand Finale Crossing Unlocked!", "gold_key.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (15, 23, 42))
    draw = ImageDraw.Draw(canvas)
    
    # 1. TOP HEADER BAR (Compact 72px)
    draw.rectangle([0, 0, CANVAS_W, 72], fill=(11, 15, 25))
    draw.line([0, 72, CANVAS_W, 72], fill=(51, 65, 85), width=2)
    
    draw.text((20, 10), cfg["phase"], fill=COLOR_SACK, font=F_HEADER_TAG)
    draw.text((20, 32), f"{cfg['quest_name']}  —  {cfg['map_name']}", fill=(255, 255, 255), font=F_HEADER_TITLE)
    
    # 2. LEFT MAP PANEL (100% CLEAN MAP — NO TEXT, NO BADGES, NO OVERLAY BOXES!)
    raw_map = Image.open(cfg["map_img"]).convert("RGB")
    map_resized = raw_map.resize((MAP_W, MAP_H), Image.Resampling.LANCZOS)
    canvas.paste(map_resized, (MAP_X, MAP_Y))
    draw.rectangle([MAP_X-2, MAP_Y-2, MAP_X+MAP_W+2, MAP_Y+MAP_H+2], outline=(90, 110, 140), width=3)
    
    # Render Sleek Questline Progression HUD Bar at the Top of Map
    core.render_questline_progression_bar(draw, cfg["id"], cfg.get("grouped_turnin_label"))
    
    # Render All Database Loot Points using Distinct Container Shapes & Matching Colors!
    db_points = core.get_map_loot_from_db(cfg["map_name"])
    for pt in db_points:
        mx, my = to_map_coord(pt['x'], pt['y'])
        r = 7 if pt.get('is_prio') else 6
        core.draw_container_shape(draw, pt['shape'], mx, my, r, pt['color'], outline=(15, 20, 30), width=2)
        
    # Render Story Objective POIs using Radiant Gold Stars (✦)
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_container_shape(draw, 'star', mx, my, 9, COLOR_STORY, outline=(10, 15, 20), width=2)
        
    # 3. RIGHT BRIEFING PANEL (Evenly Spaced 5 Blocks, No Repetition, Bigger Visuals!)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=(15, 20, 30), outline=(51, 65, 85), width=2)
    
    # Vertical Spacing Allocation:
    # Available height = 1270 px
    # 5 Blocks with 16px gaps
    b1_y = PANEL_Y + 14   # 96
    b1_h = 175
    gap = 16
    
    b2_y = b1_y + b1_h + gap # 287
    b2_h = 145
    
    b3_y = b2_y + b2_h + gap # 448
    b3_h = 125
    
    b4_y = b3_y + b3_h + gap # 589
    b4_h = 485
    
    b5_y = b4_y + b4_h + gap # 1090
    b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 276
    
    # ==========================================
    # BLOCK 1: ACTIVE RAID OBJECTIVES (GROUPED TURN-INS)
    # ==========================================
    draw.text((PANEL_X+18, b1_y), "ACTIVE RAID OBJECTIVE (TURN-IN REQUIREMENT)", fill=COLOR_SACK, font=F_SECTION_TITLE)
    
    objs = cfg.get("active_objectives", [])
    if len(objs) == 1:
        # Single Objective Card (Spacious, Big 72x72 Image)
        o = objs[0]
        card_y = b1_y + 26
        card_h = b1_h - 26
        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=(28, 26, 16), outline=COLOR_SACK, width=2)
        
        c_img = core.CONTAINER_IMGS.get(o["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, card_y+10, 72, 72), bg_color=(16, 16, 10), border_color=COLOR_SACK, border_w=2)
        i_img = core.ITEM_IMGS.get(o["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+86, card_y+38, 44, 44), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)
        
        tx = PANEL_X + 144
        draw.text((tx, card_y+10), o["title"], fill=(255, 255, 255), font=F_CARD_TITLE)
        r_col = core.get_rate_color(o["drop_rate"])
        draw.text((tx, card_y+36), f"Drop Rate: {o['drop_rate']}", fill=r_col, font=F_BODY_BOLD)
        draw.text((tx+140, card_y+36), f"•  {o['density']}", fill=COLOR_SACK, font=F_BODY)
        draw.text((tx, card_y+62), o["desc"][:75], fill=(210, 225, 245), font=F_BODY)
        draw.text((tx, card_y+88), o["npc"], fill=(34, 197, 94), font=F_BODY_BOLD)
    else:
        # Grouped Multiple Turn-Ins (2 Stacked Cards)
        card_y = b1_y + 24
        each_h = 68
        for i, o in enumerate(objs):
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=(28, 26, 16), outline=COLOR_SACK, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+24, card_y+6, 54, 54), bg_color=(16, 16, 10), border_color=COLOR_SACK, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+68, card_y+24, 34, 34), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)
            
            tx = PANEL_X + 116
            draw.text((tx, card_y+6), o["title"], fill=(255, 255, 255), font=F_BODY_BOLD)
            r_col = core.get_rate_color(o["drop_rate"])
            draw.text((tx, card_y+26), f"Drop Rate: {o['drop_rate']}", fill=r_col, font=F_BODY_BOLD)
            draw.text((tx+130, card_y+26), f"•  {o['density']}", fill=COLOR_SACK, font=F_SMALL)
            draw.text((tx, card_y+46), o["npc"], fill=(34, 197, 94), font=F_SMALL_BOLD)
            card_y += each_h + 8

    # ==========================================
    # BLOCK 2: ⭐ HIGH-PRIORITY EVERY-RAID SWEEP (CONTRABAND)
    # ==========================================
    cs = cfg.get("contraband_sweep", {})
    draw.text((PANEL_X+18, b2_y), cs.get("title", "⭐ CHECK EVERY RAID (MR SWEET'S CONTRABAND)"), fill=COLOR_BULLION, font=F_SECTION_TITLE)
    
    c_card_y = b2_y + 26
    c_card_w = (PANEL_W - 36 - 12) // 2
    
    # Left Card: Bullion Box (Opium Pipe)
    b_data = cs.get("bullion", {})
    draw.rounded_rectangle([PANEL_X+18, c_card_y, PANEL_X+18+c_card_w, c_card_y+b2_h-26], radius=8, fill=(26, 18, 36), outline=COLOR_BULLION, width=2)
    # Bullion Box Icon
    c_img = core.CONTAINER_IMGS.get("bullion_box.webp")
    core.paste_icon_safe(canvas, c_img, (PANEL_X+26, c_card_y+10, 52, 52), bg_color=(18, 12, 26), border_color=COLOR_BULLION, border_w=2)
    i_img = core.ITEM_IMGS.get(b_data.get("i_ico", "opium_pipe.png"))
    core.paste_icon_safe(canvas, i_img, (PANEL_X+68, c_card_y+30, 34, 34), bg_color=(22, 14, 32), border_color=(70, 85, 105), border_w=1)
    
    bx = PANEL_X + 112
    draw.text((bx, c_card_y+8), f"◆ {b_data.get('item', 'Opium Pipe')}", fill=(255, 255, 255), font=F_CARD_TITLE)
    r_col = core.get_rate_color(b_data.get("rate", "13.7%"))
    draw.text((bx, c_card_y+34), f"Drop Rate: {b_data.get('rate')}", fill=r_col, font=F_BODY_BOLD)
    draw.text((bx, c_card_y+58), b_data.get("loc", "Desks")[:32], fill=(210, 220, 240), font=F_SMALL)
    draw.text((bx, c_card_y+80), "⭐ Priority Contraband", fill=COLOR_BULLION, font=F_SMALL_BOLD)
    
    # Right Card: Wall Cabinet (China Bowl)
    c_data = cs.get("cabinet", {})
    right_x = PANEL_X + 18 + c_card_w + 12
    draw.rounded_rectangle([right_x, c_card_y, right_x+c_card_w, c_card_y+b2_h-26], radius=8, fill=(16, 26, 42), outline=COLOR_CABINET, width=2)
    # Wall Cabinet Icon
    c_img = core.CONTAINER_IMGS.get("wall_cabinet.webp")
    core.paste_icon_safe(canvas, c_img, (right_x+8, c_card_y+10, 52, 52), bg_color=(12, 20, 32), border_color=COLOR_CABINET, border_w=2)
    i_img = core.ITEM_IMGS.get(c_data.get("i_ico", "china_bowl.png"))
    core.paste_icon_safe(canvas, i_img, (right_x+50, c_card_y+30, 34, 34), bg_color=(14, 24, 38), border_color=(70, 85, 105), border_w=1)
    
    cx = right_x + 94
    draw.text((cx, c_card_y+8), f"■ {c_data.get('item', 'China Bowl')}", fill=(255, 255, 255), font=F_CARD_TITLE)
    r_col = core.get_rate_color(c_data.get("rate", "16.1%"))
    draw.text((cx, c_card_y+34), f"Drop Rate: {c_data.get('rate')}", fill=r_col, font=F_BODY_BOLD)
    draw.text((cx, c_card_y+58), c_data.get("loc", "Walls")[:32], fill=(210, 220, 240), font=F_SMALL)
    draw.text((cx, c_card_y+80), "⭐ Priority Contraband", fill=COLOR_CABINET, font=F_SMALL_BOLD)

    # ==========================================
    # BLOCK 3: TACTICAL ROTATION & EXTRACTION ROUTE
    # ==========================================
    draw.text((PANEL_X+18, b3_y), "SPAWN-INDEPENDENT EXECUTION & ROTATION ROUTE", fill=COLOR_SACK, font=F_SECTION_TITLE)
    
    step_y = b3_y + 26
    for i, step in enumerate(cfg["steps"], 1):
        draw.ellipse([PANEL_X+20, step_y+2, PANEL_X+42, step_y+24], fill=(0, 112, 244))
        draw.text((PANEL_X+27, step_y+3), str(i), fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+50, step_y+4), step[:85], fill=(240, 245, 255), font=F_BODY)
        step_y += 24

    # ==========================================
    # BLOCK 4: MAP CONTAINER DIRECTORY & DROP ODDS (LINKED TO MAP SHAPES)
    # ==========================================
    draw.rounded_rectangle([PANEL_X+18, b4_y, PANEL_X+PANEL_W-18, b4_y+b4_h], radius=10, fill=(12, 16, 26), outline=(70, 85, 110), width=2)
    draw.text((PANEL_X+32, b4_y+10), f"MAP CONTAINER DIRECTORY & DROP ODDS  —  {cfg['map_name']}", fill=COLOR_SACK, font=F_CARD_TITLE)
    
    # Legend Bar (Matching Shapes & Colors!)
    sb_y = b4_y + 36
    draw.rounded_rectangle([PANEL_X+30, sb_y, PANEL_X+PANEL_W-30, sb_y+40], radius=6, fill=(18, 24, 38), outline=(50, 65, 88), width=1)
    
    # Row 1: Shapes
    draw.ellipse([PANEL_X+38, sb_y+7, PANEL_X+48, sb_y+17], fill=COLOR_SACK, outline=(10, 15, 20), width=1)
    draw.text((PANEL_X+54, sb_y+5), "● Sacks (Yellow)", fill=COLOR_SACK, font=F_TINY)
    
    draw.polygon([(PANEL_X+168, sb_y+6), (PANEL_X+174, sb_y+12), (PANEL_X+168, sb_y+18), (PANEL_X+162, sb_y+12)], fill=COLOR_BULLION)
    draw.text((PANEL_X+180, sb_y+5), "◆ Bullion (Purple ⭐)", fill=COLOR_BULLION, font=F_TINY)
    
    draw.rectangle([PANEL_X+318, sb_y+7, PANEL_X+328, sb_y+17], fill=COLOR_CABINET)
    draw.text((PANEL_X+334, sb_y+5), "■ Cabinets (Blue ⭐)", fill=COLOR_CABINET, font=F_TINY)
    
    draw.ellipse([PANEL_X+470, sb_y+7, PANEL_X+480, sb_y+17], outline=COLOR_ASH, width=2)
    draw.text((PANEL_X+486, sb_y+5), "◎ Ash (Orange)", fill=COLOR_ASH, font=F_TINY)
    
    # Row 2: Drop Rates
    draw.text((PANEL_X+38, sb_y+23), "Drop Rates: ", fill=(160, 180, 205), font=F_TINY)
    draw.text((PANEL_X+110, sb_y+23), "■ <20% (Red: Rare)", fill=(239, 68, 68), font=F_TINY)
    draw.text((PANEL_X+250, sb_y+23), "■ 20-49% (Orange: Medium)", fill=(249, 115, 22), font=F_TINY)
    draw.text((PANEL_X+430, sb_y+23), "■ 50-100% (Green: High)", fill=(34, 197, 94), font=F_TINY)
    
    # Render Directory Rows (Big 40x40 Icons, Clear Shapes)
    dir_y = sb_y + 48
    for itm in cfg.get("directory", []):
        # 1. Matching Map Shape
        core.draw_container_shape(draw, itm['shape'], PANEL_X+44, dir_y+20, 8, itm['color'], outline=(10, 15, 22), width=2)
        
        # 2. Container Icon
        c_im = core.CONTAINER_IMGS.get(itm.get('c_ico'))
        core.paste_icon_safe(canvas, c_im, (PANEL_X+60, dir_y+2, 38, 38), bg_color=(15, 20, 30), border_color=itm['color'], border_w=2)
        
        # 3. Item Icon
        i_im = core.ITEM_IMGS.get(itm.get('i_ico'))
        core.paste_icon_safe(canvas, i_im, (PANEL_X+104, dir_y+2, 38, 38), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)
        
        # 4. Text Info (Container -> Item)
        draw.text((PANEL_X+150, dir_y+2), f"{itm['cont']} ➔ {itm['item']}", fill=(255, 255, 255), font=F_BODY_BOLD)
        
        # 5. Location / Landmark
        draw.text((PANEL_X+150, dir_y+22), itm['loc'][:65], fill=(185, 200, 225), font=F_SMALL)
        
        # 6. Drop Rate percentage
        r_col = core.get_rate_color(itm['rate'])
        draw.text((PANEL_X+PANEL_W-90, dir_y+10), itm['rate'], fill=r_col, font=F_BODY_BOLD)
        
        dir_y += 44

    # ==========================================
    # BLOCK 5: FUTURE STASH PRE-BANKER (UPCOMING QUESTS)
    # ==========================================
    draw.text((PANEL_X+18, b5_y), "UPCOMING QUEST STASH ROADMAP (FUTURE BANKED ITEMS)", fill=(255, 255, 255), font=F_SECTION_TITLE)
    
    r_y = b5_y + 26
    for r_card in cfg.get("roadmap", []):
        card_h = 42
        draw.rounded_rectangle([PANEL_X+18, r_y, PANEL_X+PANEL_W-18, r_y+card_h], radius=6, fill=(20, 26, 38), outline=(51, 65, 85), width=1)
        draw.text((PANEL_X+26, r_y+11), r_card["quest"], fill=COLOR_SACK, font=F_BODY_BOLD)
        
        item_x = PANEL_X + 270
        for item_name, item_ico in r_card["items"]:
            ico_im = core.ITEM_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, r_y+6, 30, 30), bg_color=(12, 18, 28))
            draw.text((item_x+36, r_y+11), item_name, fill=(255, 255, 255), font=F_BODY_BOLD)
            item_x += int(draw.textlength(item_name, font=F_BODY_BOLD)) + 45
            
        r_y += card_h + 8

    # Save final artifact image
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating all 7 perfect V12 briefings...")
    for cfg in RAIDS_CONFIG:
        render_briefing(cfg)
    print("All 7 V12 briefings generated successfully!")
