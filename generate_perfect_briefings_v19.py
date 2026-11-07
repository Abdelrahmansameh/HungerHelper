import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v19 as core

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

PRIO_YELLOW = core.PRIO_YELLOW
PRIO_PURPLE = core.PRIO_PURPLE
PRIO_BLUE   = core.PRIO_BLUE
PRIO_GREEN  = core.PRIO_GREEN
PRIO_GREY   = core.PRIO_GREY

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
        "phase": "RAID 1 OF 7  -  INTRODUCTORY GATHERING",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 2: Making Dough",
        "story_pois": [],
        "active_objectives": [
            {
                "title": "Quest 2: Gather 20x Flour",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Flour Sack / Granaries",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "40 Spots across farmhouses & granaries",
                "desc": "Primary quest requirement. Collect 20x Flour to unlock Quest 3."
            }
        ],
        "priority_focus": {
            "title": "Quest 4: Bank 15x Charcoal",
            "item": "15x Charcoal",
            "cont": "Pile of Ash",
            "c_ico": "pile_of_ash.webp",
            "i_ico": "charcoal.png",
            "rate": "52.6%",
            "color": PRIO_PURPLE,
            "desc": "Search fireplace hearths in living quarters to bank Charcoal for Q4."
        },
        "rotation_steps": [
            "Find 20x Flour in farmhouses and granaries (Quest 2).",
            "Search hearths and fire pits for 15x Charcoal (Quest 4).",
            "Search Tooling Bins, Graves, and Cabinets for Quest 6.",
            "Search desks for Bullion Box and living quarters for Wall Cabinet.",
            "Extract to Château and turn in 20x Flour to Eloise."
        ],
        "container_priority_map": {
            "flour_sack": {"keyword": "Flour Sack", "shape": "wide_circle", "color": PRIO_YELLOW, "label": "Flour Sack (20x Flour - Active Q2)", "is_prio": True},
            "pile_of_ash": {"keyword": "Pile of Ash", "shape": "circle", "color": PRIO_PURPLE, "label": "Pile of Ash (15x Charcoal - Future Q4)"},
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "circle", "color": PRIO_BLUE, "label": "Tooling Bin (20x Saltpetre - Future Q6)"},
            "stone_grave": {"keyword": "Stone Grave", "shape": "circle", "color": PRIO_BLUE, "label": "Stone Grave (5x Damp Rag - Future Q6)"},
            "physician": {"keyword": "Physician", "shape": "circle", "color": PRIO_BLUE, "label": "Physician Cabinet (10x Tallow Balm - Future Q6)"},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_GREEN, "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_GREEN, "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "20x Flour (Active Q2)", "i_ico": "flour.png", "rate": "47.6%", "spots": "40 Spots"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal (Future Q4)", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "14 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre (Future Q6)", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Stone Grave", "c_ico": "stone_grave.webp", "item": "5x Damp Rag (Future Q6)", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Physician's Cabinet", "c_ico": "physician_bag.webp", "item": "10x Tallow Balm (Future Q6)", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Qtrs"},
            {"shape": "circle", "color": PRIO_GREEN, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe (Future Q9)", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots"},
            {"shape": "circle", "color": PRIO_GREEN, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl (Future Q9)", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots"}
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 2: Jacques Bridge (Gavroche Camp & Charcoal MUST BOTH BE COMPLETED)
    # Priority Focus: Bare Necessities in PURPLE
    {
        "id": 2,
        "phase": "RAID 2 OF 7  -  DUAL REQUIRED TURN-INS (CAMP & CHARCOAL)",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: Gavroche Camp  &  Quest 4: Charcoal",
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp", "offset_dir": "bottom"}
        ],
        "active_objectives": [
            {
                "title": "Quest 3: Locate Gavroche Family Camp",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Lower Bridge Deck Perimeter",
                "cont_img": "ledger_desk.webp",
                "item_img": "silver_key.png",
                "drop_rate": "100%",
                "density": "Instant Discovery Trigger (X: 1479, Y: 313)",
                "desc": "Infiltrate Jacques Bridge lower deck and step into the camp perimeter to complete Quest 3."
            },
            {
                "title": "Quest 4: Gather 15x Charcoal (REQUIRED NOW!)",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Guardhouse Hearths & Carriage Houses",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png",
                "drop_rate": "52.6%",
                "density": "13 Hearths across bridge guardposts",
                "desc": "MUST gather 15x Charcoal now. Both Q3 & Q4 must be handed in together to unlock Quest 5!"
            }
        ],
        "priority_focus": {
            "title": "Quest 6: Pre-Farm Bare Necessities",
            "item": "20x Saltpetre, 5x Damp Rag, 10x Balm",
            "cont": "Tooling Bins / Buckets / Doctor Cabinet",
            "c_ico": "tooling_bin.webp",
            "i_ico": "saltpetre.png",
            "rate": "18.9% / 23.3% / 9.1%",
            "color": PRIO_PURPLE,
            "desc": "Pre-farm Saltpetre, Damp Rags, and Tallow Balm for the multiple turn-ins of Quest 6."
        },
        "rotation_steps": [
            "Go to lower bridge deck and scout Gavroche Camp (Quest 3).",
            "Search guardhouse hearths to gather 15x Charcoal (Quest 4).",
            "Search Tooling Bins, Buckets, and Infirmary for Bare Necessities (Quest 6).",
            "Search desks for Bullion Box and towers for Wall Cabinet (Quest 9).",
            "Extract to Château and turn in BOTH Quest 3 & Quest 4 to unlock Quest 5!"
        ],
        "container_priority_map": {
            "pile_of_ash": {"keyword": "Pile of Ash", "shape": "wide_circle", "color": PRIO_YELLOW, "label": "Pile of Ash (15x Charcoal - Active Q4)", "is_prio": True},
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "circle", "color": PRIO_PURPLE, "label": "Tooling Bin (20x Saltpetre - Focus Q6)"},
            "old_bucket": {"keyword": "Old Bucket", "shape": "circle", "color": PRIO_PURPLE, "label": "Old Bucket (5x Damp Rag - Focus Q6)"},
            "physician": {"keyword": "Physician", "shape": "circle", "color": PRIO_PURPLE, "label": "Physician Cabinet (10x Tallow Balm - Focus Q6)"},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_BLUE, "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Gavroche Camp", "c_ico": "ledger_desk.webp", "item": "Camp Trigger (Active Q3)", "i_ico": "silver_key.png", "rate": "100%", "spots": "Lower Deck"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal (Active Q4)", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "13 Spots"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre (Focus Q6)", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "24 Spots"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Old Bucket / Grave", "c_ico": "stone_grave.webp", "item": "5x Damp Rag (Focus Q6)", "i_ico": "damp_rag.png", "rate": "23.3%", "spots": "10 Spots"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Physician's Cabinet", "c_ico": "physician_bag.webp", "item": "10x Tallow Balm (Focus Q6)", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "3 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe (Future Q9)", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "28 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl (Future Q9)", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "3 Spots"}
        ],
        "roadmap": [
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 3: Sarlat Farm (Charcoal Done; Fort Recon & Bare Necessities Multi-Turn-In)
    {
        "id": 3,
        "phase": "RAID 3 OF 7  -  FORT RECON & MULTI-TURN-IN SUPPLIES",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 5: Front Recon  &  Quest 6: Bare Necessities",
        "story_pois": [
            {"x": 1140, "y": 1307, "label": "Gunline Fort Tactical Map", "offset_dir": "top"}
        ],
        "active_objectives": [
            {
                "title": "Quest 5: Scout Gunline Fort Tactical Map",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Tactical Map Table (X: 1140, Y: 1307)",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "Guaranteed Interactive Map Table",
                "desc": "Scout Gunline Fort and inspect the Tactical Map table to complete Mapping the Front."
            },
            {
                "title": "Quest 6: Gather Bare Necessities Supplies",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Tooling Bins, Graves & Doctor's Quarters",
                "cont_img": "tooling_bin.webp",
                "item_img": "saltpetre.png",
                "drop_rate": "Multi-Turn-In",
                "density": "20x Saltpetre, 5x Damp Rag, 10x Balm",
                "desc": "Gather all 3 items to complete the multiple turn-in requirements for Quest 6."
            }
        ],
        "priority_focus": {
            "title": "Quest 9: Pre-Farm Opium Pipe",
            "item": "1x Opium Pipe",
            "cont": "Bullion Box",
            "c_ico": "bullion_box.webp",
            "i_ico": "opium_pipe.png",
            "rate": "13.7%",
            "color": PRIO_PURPLE,
            "desc": "Search bedroom desks on Sarlat to pre-bank Opium Pipe for upcoming Quest 9."
        },
        "rotation_steps": [
            "Go to Gunline Fort and inspect the Tactical Map table (Quest 5).",
            "Find 20x Saltpetre in workshops from Tooling Bins (Quest 6).",
            "Find 5x Damp Rags in graveyards from Stone Graves (Quest 6).",
            "Find 10x Tallow Balm in Doctor's Quarters cabinets (Quest 6).",
            "Search bedroom desks for Bullion Box for Quest 9.",
            "Extract to Château and turn in Fort Recon and Bare Necessities."
        ],
        "container_priority_map": {
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "wide_circle", "color": PRIO_YELLOW, "label": "Tooling Bin (20x Saltpetre - Active Q6)", "is_prio": True},
            "stone_grave": {"keyword": "Stone Grave", "shape": "wide_circle", "color": PRIO_YELLOW, "label": "Stone Grave (5x Damp Rag - Active Q6)", "is_prio": True},
            "physician": {"keyword": "Physician", "shape": "wide_circle", "color": PRIO_YELLOW, "label": "Physician Cabinet (10x Tallow Balm - Active Q6)", "is_prio": True},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_PURPLE, "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Gunline Fort", "c_ico": "ledger_desk.webp", "item": "Tactical Map (Active Q5)", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Western Fort"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre (Active Q6)", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Stone Grave", "c_ico": "stone_grave.webp", "item": "5x Damp Rag (Active Q6)", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Physician's Cabinet", "c_ico": "physician_bag.webp", "item": "10x Tallow Balm (Active Q6)", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Qtrs"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe (Future Q9)", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl (Future Q9)", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots"}
        ],
        "roadmap": [
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Sarlat Farm (Candle & Bribery)
    {
        "id": 4,
        "phase": "RAID 4 OF 7  -  CHAPEL INFILTRATION & BRIBERY",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8: Sanctuary  &  Quest 9: Bribery",
        "story_pois": [
            {"x": 2697, "y": 807, "label": "Sarlat Chapel Altar (Candle)", "offset_dir": "bottom"}
        ],
        "active_objectives": [
            {
                "title": "Quest 8: Recover Red Votive Candle",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Sarlat Chapel Altar (X: 2697, Y: 807)",
                "cont_img": "strongbox.webp",
                "item_img": "votive_candle.png",
                "drop_rate": "100%",
                "density": "Guaranteed Interactive Altar",
                "desc": "Infiltrate Sarlat Chapel and recover the Red Votive Candle from the central altar."
            }
        ],
        "priority_focus": {
            "title": "Quest 9: Contraband Opium Pipe",
            "item": "1x Opium Pipe",
            "cont": "Bullion Box",
            "c_ico": "bullion_box.webp",
            "i_ico": "opium_pipe.png",
            "rate": "13.7%",
            "color": PRIO_PURPLE,
            "desc": "Search bedroom desks in farmhouse manors for Bullion Box Opium Pipe."
        },
        "rotation_steps": [
            "Go to the Sarlat Chapel altar and recover the Red Votive Candle (Quest 8).",
            "Search bedroom desks across farmhouses for Bullion Boxes (Quest 9).",
            "Search living quarters for Wall Cabinets to find China Bowl (Quest 9).",
            "Extract to Château and turn in Red Votive Candle to Eloise."
        ],
        "container_priority_map": {
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_PURPLE, "label": "Bullion Box (Opium Pipe - Active Q9)", "is_prio": True},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "label": "Wall Cabinet (China Bowl - Active Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Chapel Altar", "c_ico": "strongbox.webp", "item": "Red Votive Candle (Active Q8)", "i_ico": "votive_candle.png", "rate": "100%", "spots": "Guaranteed"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe (Active Q9)", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl (Active Q9)", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots"}
        ],
        "roadmap": [
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 5: Sarlat Farm (Mount Sinai Books 1, 2, 3)
    {
        "id": 5,
        "phase": "RAID 5 OF 7  -  EXPEDITION: SARLAT ARCHIVES",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 1)",
        "story_pois": [
            {"x": 2379.86, "y": 2045.2,  "label": "Book 1: Rozier (Granary Cache)", "offset_dir": "bottom"},
            {"x": 2085.66, "y": 887.49,  "label": "Book 2: Census 1806 (Farmhouse Desk)", "offset_dir": "top"},
            {"x": 2697.0,  "y": 807.0,   "label": "Book 3: Catéchisme (Chapel Altar)", "offset_dir": "right"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10: Recover Sarlat Books 1, 2, and 3",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Sarlat Fixed Book Spawns",
                "cont_img": "strongbox.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "3 Fixed Relic Locations",
                "desc": "Collect Rozier (Granary Cache), Census 1806 (Farmhouse Desk), and Catéchisme (Chapel Altar)."
            }
        ],
        "priority_focus": {
            "title": "Quest 10: Sarlat Relic Books",
            "item": "Books 1, 2, 3",
            "cont": "Sarlat Fixed Spots",
            "c_ico": "strongbox.webp",
            "i_ico": "book_rozier.png",
            "rate": "100%",
            "color": PRIO_YELLOW,
            "desc": "Granary Cache (Rozier), Farmhouse Desk (Census 1806) & Chapel (Catéchisme)."
        },
        "rotation_steps": [
            "Go to Master Granary upper cache and take Book 1: Rozier.",
            "Go to Sarlat Village farmhouse desk and take Book 2: Census 1806.",
            "Go to Chapel Altar and take Book 3: Catéchisme.",
            "Extract to Château with all 3 Sarlat archive books secured."
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Granary Cache", "c_ico": "strongbox.webp", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Master Granary"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Farmhouse Desk", "c_ico": "ledger_desk.webp", "item": "Book 2: Census 1806", "i_ico": "book_census.png", "rate": "100%", "spots": "Sarlat Village"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Chapel Altar", "c_ico": "strongbox.webp", "item": "Book 3: Catéchisme", "i_ico": "book_catechisme.png", "rate": "100%", "spots": "Chapel Altar"}
        ],
        "roadmap": [
            {"quest": "Mount Sinai (Part 2: Jacques Bridge)", "items": [("Book 4: Montesquieu", "book_montesquieu.png"), ("Book 5: Buffon", "book_buffon.png")]},
            {"quest": "Mount Sinai (Part 3: Sombre Forest Finale)", "items": [("Book 6: Rondelet", "book_rondelet.png"), ("Book 7: Codex Medicamentarius", "book_mortuary.png")]}
        ]
    },

    # RAID 6: Jacques Bridge (Mount Sinai Books 4, 5)
    {
        "id": 6,
        "phase": "RAID 6 OF 7  -  EXPEDITION: BRIDGE FORTRESS",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 2)",
        "story_pois": [
            {"x": 1391.83, "y": 1535.7,  "label": "Book 4: Montesquieu (North Tower)", "offset_dir": "left"},
            {"x": 2094.88, "y": 1346.36, "label": "Book 5: Buffon (Guardpost Storeroom)", "offset_dir": "right"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10: Recover Bridge Books 4 and 5",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Jacques Bridge Book Locations",
                "cont_img": "strongbox.webp",
                "item_img": "book_montesquieu.png",
                "drop_rate": "100%",
                "density": "2 Fixed Fortress Spots",
                "desc": "Collect Montesquieu from North Tower and Buffon from Guardpost Storeroom."
            }
        ],
        "priority_focus": {
            "title": "Quest 10: Bridge Relic Books",
            "item": "Books 4 & 5",
            "cont": "Bridge Locations",
            "c_ico": "strongbox.webp",
            "i_ico": "book_montesquieu.png",
            "rate": "100%",
            "color": PRIO_YELLOW,
            "desc": "North Bridge Tower (Montesquieu) & Guardpost (Buffon)."
        },
        "rotation_steps": [
            "Go to North Bridge Tower storeroom and take Book 4: Montesquieu.",
            "Go to Guardpost barracks table and take Book 5: Buffon.",
            "Extract to Château with both Bridge archive books secured."
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Bridge Tower", "c_ico": "strongbox.webp", "item": "Book 4: Montesquieu", "i_ico": "book_montesquieu.png", "rate": "100%", "spots": "North Tower"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Guardpost Desk", "c_ico": "ledger_desk.webp", "item": "Book 5: Buffon", "i_ico": "book_buffon.png", "rate": "100%", "spots": "Guardpost"}
        ],
        "roadmap": [
            {"quest": "Mount Sinai (Part 3: Sombre Forest Finale)", "items": [("Book 6: Rondelet", "book_rondelet.png"), ("Book 7: Codex Medicamentarius", "book_mortuary.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Mount Sinai Books 6, 7 & Finale!)
    {
        "id": 7,
        "phase": "RAID 7 OF 7  -  EXPEDITION FINALE: SOMBRE FOREST",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai Finale",
        "story_pois": [
            {"x": 3168.6, "y": 2405.75, "label": "Book 6: Rondelet (Ruins Shrine)", "offset_dir": "left"},
            {"x": 2592.18, "y": 2992.87, "label": "Book 7: Codex Medicamentarius (Ridge)", "offset_dir": "top"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10 Finale: Recover Books 6 and 7",
                "npc": "Turn in to: Eloise at Château (Completes Questline!)",
                "cont_name": "Sombre Forest Book Locations",
                "cont_img": "strongbox.webp",
                "item_img": "book_rondelet.png",
                "drop_rate": "100%",
                "density": "Final 2 Relic Books",
                "desc": "Collect Rondelet from Ruins Shrine and Codex Medicamentarius from Ridge Shrine."
            }
        ],
        "priority_focus": {
            "title": "Quest 10: Final Forest Relic Books",
            "item": "Books 6 & 7",
            "cont": "Forest Shrines",
            "c_ico": "strongbox.webp",
            "i_ico": "book_rondelet.png",
            "rate": "100%",
            "color": PRIO_YELLOW,
            "desc": "Forest Ruins (Rondelet) & Southern Ridge (Codex Medicamentarius)."
        },
        "rotation_steps": [
            "Go to South-Eastern Forest Ruins and take Book 6: Rondelet.",
            "Go to Southern Ridge Shrine and take Book 7: Codex Medicamentarius.",
            "Extract to Château and hand in all 7 books to Eloise to complete the storyline!"
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Forest Ruins", "c_ico": "strongbox.webp", "item": "Book 6: Rondelet", "i_ico": "book_rondelet.png", "rate": "100%", "spots": "Forest Ruins"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Ridge Shrine", "c_ico": "strongbox.webp", "item": "Book 7: Codex Medicamentarius", "i_ico": "book_mortuary.png", "rate": "100%", "spots": "Ridge Shrine"}
        ],
        "roadmap": [
            {"quest": "Eloise Storyline 100% Complete!", "items": [("Storyline Cleared!", "gold_key.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (10, 14, 22, 255))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    draw.rectangle([0, 0, CANVAS_W, 78], fill=(13, 17, 26))
    draw.line([(0, 78), (CANVAS_W, 78)], fill=(38, 48, 65), width=2)

    tag_txt = cfg["phase"].upper()
    draw.rounded_rectangle([20, 16, 20 + int(draw.textlength(tag_txt, font=F_HEADER_TAG)) + 24, 60], radius=6, fill=(35, 45, 65), outline=PRIO_YELLOW, width=1)
    draw.text((32, 26), tag_txt, fill=PRIO_YELLOW, font=F_HEADER_TAG)

    title_x = 20 + int(draw.textlength(tag_txt, font=F_HEADER_TAG)) + 45
    main_title = f"{cfg['map_name'].upper()}  -  {cfg['quest_name'].upper()}"
    draw.text((title_x, 22), main_title, fill=(255, 255, 255), font=F_HEADER_TITLE)

    # Right tag: Wipe Speedrun
    status_txt = "SPEEDRUN STRATEGY - 7 DEDICATED DEPLOYMENTS"
    st_w = int(draw.textlength(status_txt, font=F_HEADER_TAG))
    draw.text((CANVAS_W - st_w - 24, 28), status_txt, fill=(148, 163, 184), font=F_HEADER_TAG)

    # 2. LEFT MAP VIEWPORT
    map_box = [MAP_X, MAP_Y, MAP_X+MAP_W, MAP_Y+MAP_H]
    draw.rectangle(map_box, fill=(10, 12, 18), outline=(51, 65, 85), width=2)

    if os.path.exists(cfg["map_img"]):
        raw_map = Image.open(cfg["map_img"]).convert("RGBA")
        resized_map = raw_map.resize((MAP_W-4, MAP_H-4), Image.Resampling.LANCZOS)
        canvas.paste(resized_map, (MAP_X+2, MAP_Y+2), resized_map)

    # 2a. PLOT DB FILTERED POINTS (WIDE CIRCLE FOR ACTIVE, SIMPLE CIRCLE FOR OTHERS)
    db_points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    for pt in db_points:
        mx, my = to_map_coord(pt['x'], pt['y'])
        r = 10 if pt.get('is_prio') else 9
        core.draw_container_shape(draw, pt['shape'], mx, my, r, pt['color'], outline=(10, 14, 20), width=2)

    # 2b. PROMINENT STORY OBJECTIVE POI MARKERS (CIRCULAR WITH WIDE OUTER LINE)
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'))

    # 2c. QUESTLINE PROGRESSION HUD BAR (EVENLY SPACED 7 COLUMNS)
    core.render_questline_progression_bar(draw, cfg["id"])

    # 3. RIGHT BRIEFING PANEL (UNIFORM TITLES: Objective, Focus, Priorities, Drops, Quests)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=(15, 20, 30), outline=(51, 65, 85), width=2)

    # Vertical Height Allocation across 1298px panel:
    # 5 evenly balanced sections with 14px gaps
    b1_y = PANEL_Y + 14   # 96
    b1_h = 160
    gap = 14

    b2_y = b1_y + b1_h + gap # 270
    b2_h = 124

    b3_y = b2_y + b2_h + gap # 408
    b3_h = 166

    b4_y = b3_y + b3_h + gap # 588
    b4_h = 420

    b5_y = b4_y + b4_h + gap # 1022
    b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 344

    # ==========================================
    # CATEGORY 1: Objective
    # ==========================================
    draw.text((PANEL_X+18, b1_y), "Objective", fill=PRIO_YELLOW, font=F_SECTION_TITLE)

    objs = cfg.get("active_objectives", [])
    if len(objs) == 1:
        o = objs[0]
        card_y = b1_y + 30
        card_h = b1_h - 30
        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=(28, 26, 16), outline=PRIO_YELLOW, width=2)

        c_img = core.CONTAINER_IMGS.get(o["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, card_y+14, 72, 72), bg_color=(16, 16, 10), border_color=PRIO_YELLOW, border_w=2)
        i_img = core.ITEM_IMGS.get(o["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+84, card_y+42, 44, 44), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)

        tx = PANEL_X + 140
        max_tw = PANEL_W - 165
        draw.text((tx, card_y+12), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
        
        rate_density = f"Drop Rate: {o['drop_rate']}   -   {o['density']}"
        draw.text((tx, card_y+38), core.fit_text(draw, rate_density, F_BODY_BOLD, max_tw), fill=(240, 245, 255), font=F_BODY_BOLD)
        draw.text((tx, card_y+64), core.fit_text(draw, o["desc"], F_BODY, max_tw), fill=(210, 225, 245), font=F_BODY)
        draw.text((tx, card_y+92), core.fit_text(draw, o["npc"], F_BODY_BOLD, max_tw), fill=(34, 197, 94), font=F_BODY_BOLD)
    else:
        # Dual Active Objectives (Raid 2 & Raid 3)
        card_y = b1_y + 30
        each_h = 60
        for i, o in enumerate(objs):
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=(28, 26, 16), outline=PRIO_YELLOW, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+26, card_y+6, 48, 48), bg_color=(16, 16, 10), border_color=PRIO_YELLOW, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+64, card_y+20, 32, 32), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)

            tx = PANEL_X + 108
            max_tw = PANEL_W - 135
            draw.text((tx, card_y+6), core.fit_text(draw, o["title"], F_BODY_BOLD, max_tw), fill=(255, 255, 255), font=F_BODY_BOLD)
            line2 = f"Drop: {o['drop_rate']}  |  {o['density']}"
            draw.text((tx, card_y+30), core.fit_text(draw, line2, F_SMALL, max_tw), fill=(240, 245, 255), font=F_SMALL)
            card_y += each_h + 8

    # ==========================================
    # CATEGORY 2: Focus
    # ==========================================
    pf = cfg.get("priority_focus", {})
    pf_color = pf.get("color", PRIO_PURPLE)
    draw.text((PANEL_X+18, b2_y), "Focus", fill=pf_color, font=F_SECTION_TITLE)

    card_y = b2_y + 28
    card_h = b2_h - 28

    draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=(24, 18, 34), outline=pf_color, width=2)

    c_img = core.CONTAINER_IMGS.get(pf.get("c_ico"))
    core.paste_icon_safe(canvas, c_img, (PANEL_X+26, card_y+10, 56, 56), bg_color=(18, 12, 26), border_color=pf_color, border_w=2)
    i_img = core.ITEM_IMGS.get(pf.get("i_ico"))
    core.paste_icon_safe(canvas, i_img, (PANEL_X+70, card_y+30, 36, 36), bg_color=(22, 14, 32), border_color=(70, 85, 105), border_w=1)

    tx = PANEL_X + 118
    max_tw = PANEL_W - 145
    draw.text((tx, card_y+8), core.fit_text(draw, f"{pf.get('title', '')}: {pf.get('item')}", F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
    draw.text((tx, card_y+34), core.fit_text(draw, f"Source: {pf.get('cont')}  -  Drop Rate: {pf.get('rate')}", F_BODY_BOLD, max_tw), fill=(240, 245, 255), font=F_BODY_BOLD)
    draw.text((tx, card_y+58), core.fit_text(draw, pf.get("desc", ""), F_SMALL, max_tw), fill=(210, 220, 240), font=F_SMALL)

    # ==========================================
    # CATEGORY 3: Priorities (Clean, Punchy Action Steps)
    # ==========================================
    draw.text((PANEL_X+18, b3_y), "Priorities", fill=PRIO_YELLOW, font=F_SECTION_TITLE)

    # Structured Card Background for Priorities
    draw.rounded_rectangle([PANEL_X+18, b3_y+28, PANEL_X+PANEL_W-18, b3_y+b3_h], radius=8, fill=(16, 21, 32), outline=(45, 58, 80), width=1)

    step_y = b3_y + 34
    for i, step in enumerate(cfg["rotation_steps"], 1):
        draw.ellipse([PANEL_X+28, step_y+1, PANEL_X+48, step_y+21], fill=(0, 112, 244))
        draw.text((PANEL_X+34, step_y+2), str(i), fill=(255, 255, 255), font=F_BODY_BOLD)
        draw.text((PANEL_X+56, step_y+2), core.fit_text(draw, step, F_BODY, PANEL_W - 85), fill=(240, 245, 255), font=F_BODY)
        step_y += 25

    # ==========================================
    # CATEGORY 4: Drops (Single Line Rows, Wide Circle for Objective, Simple for Future)
    # ==========================================
    draw.rounded_rectangle([PANEL_X+18, b4_y, PANEL_X+PANEL_W-18, b4_y+b4_h], radius=10, fill=(12, 16, 26), outline=(70, 85, 110), width=2)
    draw.text((PANEL_X+32, b4_y+10), "Drops", fill=PRIO_YELLOW, font=F_CARD_TITLE)

    # Priority Color Order Legend Bar
    sb_y = b4_y + 36
    draw.rounded_rectangle([PANEL_X+28, sb_y, PANEL_X+PANEL_W-28, sb_y+26], radius=5, fill=(18, 24, 38), outline=(50, 65, 88), width=1)

    # Active Objective (Circle with Wide Outer Line)
    core.draw_container_shape(draw, 'wide_circle', PANEL_X+42, sb_y+13, 5, PRIO_YELLOW)
    draw.text((PANEL_X+54, sb_y+6), "Wide Ring: Objective", fill=PRIO_YELLOW, font=F_TINY)

    core.draw_container_shape(draw, 'circle', PANEL_X+210, sb_y+13, 6, PRIO_PURPLE)
    draw.text((PANEL_X+222, sb_y+6), "Circle: Focus", fill=PRIO_PURPLE, font=F_TINY)

    core.draw_container_shape(draw, 'circle', PANEL_X+350, sb_y+13, 6, PRIO_BLUE)
    draw.text((PANEL_X+362, sb_y+6), "Circle: Prio 3", fill=PRIO_BLUE, font=F_TINY)

    core.draw_container_shape(draw, 'circle', PANEL_X+490, sb_y+13, 6, PRIO_GREEN)
    draw.text((PANEL_X+502, sb_y+6), "Circle: Prio 4", fill=PRIO_GREEN, font=F_TINY)

    # Render Directory Rows (Single Line, Spots Next to Rate, Guaranteed No Overlap)
    dir_y = sb_y + 34
    row_count = len(cfg.get("directory", []))
    row_h = 44 if row_count >= 6 else (54 if row_count >= 3 else 60)

    for itm in cfg.get("directory", []):
        # Marker shape
        core.draw_container_shape(draw, itm['shape'], PANEL_X+44, dir_y+19, 10, itm['color'], outline=(10, 14, 20), width=2)

        # Container Icon
        c_im = core.CONTAINER_IMGS.get(itm.get('c_ico'))
        core.paste_icon_safe(canvas, c_im, (PANEL_X+64, dir_y+2, 36, 36), bg_color=(15, 20, 30), border_color=itm['color'], border_w=2)

        # Item Icon
        i_im = core.ITEM_IMGS.get(itm.get('i_ico'))
        core.paste_icon_safe(canvas, i_im, (PANEL_X+106, dir_y+2, 36, 36), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)

        # Right label: Drop Rate (Spots)
        spots_str = itm.get('spots', '')
        rate_str = itm.get('rate', '')
        right_label = f"{rate_str}  ({spots_str})" if spots_str else rate_str
        rw = int(draw.textlength(right_label, font=F_CARD_TITLE))
        draw.text((PANEL_X + PANEL_W - 32 - rw, dir_y+9), right_label, fill=(240, 245, 255), font=F_CARD_TITLE)

        # Left label: Container -> Item (Clamped to prevent touching right label!)
        max_left_w = PANEL_W - 190 - rw
        label_text = f"{itm['cont']}  ->  {itm['item']}"
        draw.text((PANEL_X+150, dir_y+9), core.fit_text(draw, label_text, F_CARD_TITLE, max_left_w), fill=(255, 255, 255), font=F_CARD_TITLE)

        dir_y += row_h

    # ==========================================
    # CATEGORY 5: Quests (Never Clips Horizontally!)
    # ==========================================
    draw.text((PANEL_X+18, b5_y), "Quests", fill=(255, 255, 255), font=F_SECTION_TITLE)

    r_y = b5_y + 30
    roadmap_list = cfg.get("roadmap", [])
    card_h = 44 if len(roadmap_list) >= 4 else 52

    for r_card in roadmap_list:
        draw.rounded_rectangle([PANEL_X+18, r_y, PANEL_X+PANEL_W-18, r_y+card_h], radius=6, fill=(20, 26, 38), outline=(51, 65, 85), width=1)
        
        # Left: Quest Title (Max 210px)
        draw.text((PANEL_X+26, r_y+int((card_h-18)/2)), core.fit_text(draw, r_card["quest"], F_BODY_BOLD, 210), fill=PRIO_YELLOW, font=F_BODY_BOLD)

        # Right: Items laid out as compact pills (No horizontal overflow!)
        item_x = PANEL_X + 245
        for item_name, item_ico in r_card["items"]:
            ico_im = core.ITEM_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, r_y+int((card_h-26)/2), 26, 26), bg_color=(12, 18, 28))
            draw.text((item_x+32, r_y+int((card_h-18)/2)), item_name, fill=(255, 255, 255), font=F_SMALL_BOLD)
            item_x += int(draw.textlength(item_name, font=F_SMALL_BOLD)) + 40

        r_y += card_h + 8

    # Save final artifact image
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating all 7 perfect V19 briefings...")
    for raid in RAIDS_CONFIG:
        render_briefing(raid)
    print("All 7 briefings generated successfully!")
