import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v21 as core

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

# Hunger Companion Colors
BG_CANVAS = core.BG_CANVAS
BG_PANEL = core.BG_PANEL
BG_CARD = core.BG_CARD
BORDER_SUBTLE = core.BORDER_SUBTLE
COLOR_GOLD = core.COLOR_GOLD
COLOR_PARCHMENT = core.COLOR_PARCHMENT
COLOR_MUTED = core.COLOR_MUTED

PRIO_YELLOW = core.PRIO_YELLOW
PRIO_PURPLE = core.PRIO_PURPLE
PRIO_BLUE   = core.PRIO_BLUE
PRIO_GREEN  = core.PRIO_GREEN
PRIO_GREY   = core.PRIO_GREY

# Fonts
F_HEADER_TITLE  = core.F_HEADER_TITLE
F_HEADER_TAG    = core.F_HEADER_TAG
F_SECTION_TITLE = core.F_SECTION_TITLE
F_CARD_TITLE    = core.F_CARD_TITLE
F_BODY_BOLD     = core.F_BODY_BOLD
F_BODY          = core.F_BODY
F_SMALL_BOLD    = core.F_SMALL_BOLD
F_SMALL         = core.F_SMALL
F_TINY          = core.F_TINY

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
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 2: Making Dough",
        "has_focus": True,
        "story_pois": [],
        "active_objectives": [
            {
                "title": "Quest 2: Gather 20x Flour",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Flour Sack / Granaries East of Château",
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png",
                "drop_rate": "47.6%",
                "density": "40 Spots across farmhouses & granaries",
                "desc": "Collect 20x Flour to complete Making Dough and unlock Quest 3."
            }
        ],
        "priority_focus": {
            "title": "Focus: 15x Charcoal",
            "item": "15x Charcoal",
            "cont": "Pile of Ash",
            "c_ico": "pile_of_ash.webp",
            "i_ico": "charcoal.png",
            "rate": "52.6%",
            "color": PRIO_PURPLE,
            "detail": "52.6% Drop Rate  •  In Fireplace Hearths North of Village"
        },
        "rotation_steps": [
            {"step": "Gather 20x Flour from farmhouses in Central Village and Granaries.", "color": PRIO_YELLOW},
            {"step": "Gather 15x Charcoal from fireplace hearths North of Village.", "color": PRIO_PURPLE},
            {"step": "Search Tooling Bins, Graves, and Infirmary for Bare Necessities supplies.", "color": PRIO_BLUE},
            {"step": "Search manor desks and cabinets for Opium Pipe and China Bowl.", "color": PRIO_GREEN},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "flour_sack": {"keyword": "Flour Sack", "color": PRIO_YELLOW, "item_img": "flour.png", "label": "Flour Sack", "is_prio": True},
            "pile_of_ash": {"keyword": "Pile of Ash", "color": PRIO_PURPLE, "item_img": "charcoal.png", "label": "Pile of Ash"},
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_BLUE, "item_img": "saltpetre.png", "label": "Tooling Bin"},
            "stone_grave": {"keyword": "Stone Grave", "color": PRIO_BLUE, "item_img": "damp_rag.png", "label": "Stone Grave"},
            "physician": {"keyword": "Physician", "color": PRIO_BLUE, "item_img": "tallow_balm.png", "label": "Physician Cabinet"},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_GREEN, "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_GREEN, "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Flour Sack", "item": "20x Flour", "i_ico": "flour.png", "rate": "47.6%", "spots": "40 Spots in Central Village & Granaries East of Château"},
            {"color": PRIO_PURPLE, "cont": "Pile of Ash", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "14 Spots in Manor Hearths North of Village"},
            {"color": PRIO_BLUE, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots in Workshops North of Windmill & Gunline Fort"},
            {"color": PRIO_BLUE, "cont": "Stone Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots in Chapel Cemetery East of Central Village"},
            {"color": PRIO_BLUE, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters South of Master Granary"},
            {"color": PRIO_GREEN, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_GREEN, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 2: Jacques Bridge (Camp & Charcoal) - NO REQUIRED NOW
    {
        "id": 2,
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3 & 4: Camp & Charcoal",
        "has_focus": True,
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp", "offset_dir": "bottom", "item_img": "silver_key.png"}
        ],
        "active_objectives": [
            {
                "title": "Quest 3: Locate Gavroche Family Camp",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Lower Bridge Deck Perimeter East of Arch",
                "cont_img": "ledger_desk.webp",
                "item_img": "silver_key.png",
                "drop_rate": "100%",
                "density": "Instant Discovery Trigger on Lower Deck",
                "desc": "Infiltrate Jacques Bridge lower deck and step into the camp perimeter."
            },
            {
                "title": "Quest 4: Gather 15x Charcoal",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "In Guardhouse Hearths along Towers",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png",
                "drop_rate": "52.6%",
                "density": "13 Hearths across bridge guardposts",
                "desc": "Gather 15x Charcoal to complete Last Embers and unlock Quest 5."
            }
        ],
        "priority_focus": {
            "title": "Focus: Bare Necessities Supplies",
            "item": "20x Saltpetre, 5x Damp Rag, 10x Balm",
            "cont": "Tooling Bins / Buckets / Doctor Cabinet",
            "c_ico": "tooling_bin.webp",
            "i_ico": "saltpetre.png",
            "rate": "18.9% / 23.3% / 9.1%",
            "color": PRIO_PURPLE,
            "detail": "20x Saltpetre (18.9%), 5x Damp Rag (23.3%), 10x Balm (9.1%)  •  In Lower Deck & Barracks"
        },
        "rotation_steps": [
            {"step": "Scout Gavroche Family Camp on Lower Bridge Deck.", "color": PRIO_YELLOW},
            {"step": "Gather 15x Charcoal from guardhouse hearths along bridge towers.", "color": PRIO_YELLOW},
            {"step": "Search Tooling Bins, Buckets, and Infirmary for Bare Necessities supplies.", "color": PRIO_PURPLE},
            {"step": "Search fortress desks and messrooms for Opium Pipe and China Bowl.", "color": PRIO_BLUE},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "pile_of_ash": {"keyword": "Pile of Ash", "color": PRIO_YELLOW, "item_img": "charcoal.png", "label": "Pile of Ash", "is_prio": True},
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_PURPLE, "item_img": "saltpetre.png", "label": "Tooling Bin"},
            "old_bucket": {"keyword": "Old Bucket", "color": PRIO_PURPLE, "item_img": "damp_rag.png", "label": "Old Bucket"},
            "physician": {"keyword": "Physician", "color": PRIO_PURPLE, "item_img": "tallow_balm.png", "label": "Physician Cabinet"},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_BLUE, "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_BLUE, "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Gavroche Camp", "item": "Camp Trigger", "i_ico": "silver_key.png", "rate": "100%", "spots": "Lower Bridge Deck East of Support Arch"},
            {"color": PRIO_YELLOW, "cont": "Pile of Ash", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "13 Spots in Guardhouse Hearths along Towers"},
            {"color": PRIO_PURPLE, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "24 Spots on Lower Deck West of River"},
            {"color": PRIO_PURPLE, "cont": "Old Bucket / Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.3%", "spots": "10 Spots in Barracks North of Lower Roadway"},
            {"color": PRIO_PURPLE, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "3 Spots in Field Infirmary inside South Tower"},
            {"color": PRIO_BLUE, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "28 Spots in Fortress Desks inside Towers"},
            {"color": PRIO_BLUE, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "3 Spots in Officer Messrooms West of Guardhouse"}
        ],
        "roadmap": [
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 3: Sarlat Farm (Fort Recon & Supplies)
    {
        "id": 3,
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 5 & 6: Fort Recon & Supplies",
        "has_focus": True,
        "story_pois": [
            {"x": 1140, "y": 1307, "label": "Gunline Fort Tactical Map", "offset_dir": "top", "item_img": "book_rozier.png"}
        ],
        "active_objectives": [
            {
                "title": "Quest 5: Scout Gunline Fort Tactical Map",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Western Fort Command Bunker Table",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "Guaranteed Interactive Map Table",
                "desc": "Scout Gunline Fort and inspect the Tactical Map table to complete Mapping the Front."
            },
            {
                "title": "Quest 6: Gather Bare Necessities Supplies",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Workshops, Graves & Doctor's Quarters",
                "cont_img": "tooling_bin.webp",
                "item_img": "saltpetre.png",
                "drop_rate": "Multi-Turn-In",
                "density": "20x Saltpetre, 5x Damp Rag, 10x Balm",
                "desc": "Gather all 3 items to complete the requirements for Bare Necessities."
            }
        ],
        "priority_focus": {
            "title": "Focus: Opium Pipe & China Bowl",
            "item": "1x Opium Pipe & 1x China Bowl",
            "cont": "Bullion Box & Wall Cabinet",
            "c_ico": "bullion_box.webp",
            "i_ico": "opium_pipe.png",
            "rate": "13.7% / 16.1%",
            "color": PRIO_PURPLE,
            "detail": "13.7% / 16.1% Drop Rate  •  In Manor Desks & Kitchen Wall Cabinets East of Windmill"
        },
        "rotation_steps": [
            {"step": "Inspect Tactical Map table in Gunline Fort command bunker.", "color": PRIO_YELLOW},
            {"step": "Gather 20x Saltpetre from workshops North of Windmill.", "color": PRIO_YELLOW},
            {"step": "Gather 5x Damp Rags from graves in Chapel Cemetery.", "color": PRIO_YELLOW},
            {"step": "Gather 10x Tallow Balm from Doctor's Quarters South of Granary.", "color": PRIO_YELLOW},
            {"step": "Search manor desks and cabinets for Opium Pipe and China Bowl.", "color": PRIO_PURPLE},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_YELLOW, "item_img": "saltpetre.png", "label": "Tooling Bin", "is_prio": True},
            "stone_grave": {"keyword": "Stone Grave", "color": PRIO_YELLOW, "item_img": "damp_rag.png", "label": "Stone Grave", "is_prio": True},
            "physician": {"keyword": "Physician", "color": PRIO_YELLOW, "item_img": "tallow_balm.png", "label": "Physician Cabinet", "is_prio": True},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_PURPLE, "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_BLUE, "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Gunline Fort", "item": "Tactical Map", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Western Fort Command Bunker Table"},
            {"color": PRIO_YELLOW, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots in Workshops North of Windmill & Gunline Fort"},
            {"color": PRIO_YELLOW, "cont": "Stone Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots in Chapel Cemetery East of Central Village"},
            {"color": PRIO_YELLOW, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters South of Master Granary"},
            {"color": PRIO_PURPLE, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_BLUE, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Sarlat Farm (Candle & Bribery) - OPIUM PIPE & CHINA BOWL ARE NOW OBJECTIVES
    {
        "id": 4,
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8 & 9: Candle & Bribery",
        "has_focus": False,
        "story_pois": [
            {"x": 2697, "y": 807, "label": "Sarlat Chapel Altar", "offset_dir": "bottom", "item_img": "votive_candle.png"}
        ],
        "active_objectives": [
            {
                "title": "Quest 8: Recover Red Votive Candle",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Central Altar in Sarlat Chapel East of Village",
                "cont_img": "strongbox.webp",
                "item_img": "votive_candle.png",
                "drop_rate": "100%",
                "density": "Guaranteed Interactive Altar",
                "desc": "Infiltrate Sarlat Chapel and recover the Red Votive Candle from the central altar."
            },
            {
                "title": "Quest 9: Contraband Opium Pipe & China Bowl",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Manor Desks North & Kitchen Cabinets East of Windmill",
                "cont_img": "bullion_box.webp",
                "item_img": "opium_pipe.png",
                "drop_rate": "13.7% / 16.1%",
                "density": "22 Desks & 4 Wall Cabinets",
                "desc": "Recover 1x Opium Pipe and 1x China Bowl to complete A Touch of Bribery."
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Red Votive Candle from altar in Sarlat Chapel.", "color": PRIO_YELLOW},
            {"step": "Recover Opium Pipe from manor desks North & East of Village.", "color": PRIO_YELLOW},
            {"step": "Recover China Bowl from kitchen wall cabinets East of Windmill.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_YELLOW, "item_img": "opium_pipe.png", "label": "Bullion Box", "is_prio": True},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_YELLOW, "item_img": "china_bowl.png", "label": "Wall Cabinet", "is_prio": True}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Chapel Altar", "item": "Red Votive Candle", "i_ico": "votive_candle.png", "rate": "100%", "spots": "Central Altar in Sarlat Chapel East of Village"},
            {"color": PRIO_YELLOW, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_YELLOW, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 10: Down From Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 5: Sarlat Farm (Mount Sinai Books 1, 2, 3) - NO FOCUS NEEDED
    {
        "id": 5,
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 1)",
        "has_focus": False,
        "story_pois": [
            {"x": 2379.86, "y": 2045.2,  "label": "Book 1: Rozier (Master Granary)", "offset_dir": "bottom", "item_img": "book_rozier.png"},
            {"x": 2085.66, "y": 887.49,  "label": "Book 2: Census 1806 (Village Manor)", "offset_dir": "top", "item_img": "book_census.png"},
            {"x": 2697.0,  "y": 807.0,   "label": "Book 3: Catéchisme (Chapel Altar)", "offset_dir": "right", "item_img": "book_catechisme.png"}
        ],
        "active_objectives": [
            {
                "title": "Book 1: Rozier (Cours Complet)",
                "npc": "Master Granary Upper Cache South-East of Village",
                "cont_name": "Granary Cache Strongbox",
                "cont_img": "strongbox.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Climb into the upper Master Granary cache and collect Book 1: Rozier."
            },
            {
                "title": "Book 2: Census 1806",
                "npc": "Manor Desk inside Central Village",
                "cont_name": "Farmhouse Ledger Desk",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_census.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Search the ground floor desk in Sarlat village manor to retrieve Book 2: Census 1806."
            },
            {
                "title": "Book 3: Catéchisme",
                "npc": "Central Altar in Sarlat Chapel East of Village",
                "cont_name": "Chapel Altar Cache",
                "cont_img": "strongbox.webp",
                "item_img": "book_catechisme.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Search the sacred altar inside Sarlat Chapel to secure Book 3: Catéchisme."
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Book 1: Rozier from Master Granary upper cache.", "color": PRIO_YELLOW},
            {"step": "Recover Book 2: Census 1806 from Sarlat Village manor desk.", "color": PRIO_YELLOW},
            {"step": "Recover Book 3: Catéchisme from Sarlat Chapel altar.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Granary Cache", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Master Granary Upper Cache South-East of Village"},
            {"color": PRIO_YELLOW, "cont": "Farmhouse Desk", "item": "Book 2: Census 1806", "i_ico": "book_census.png", "rate": "100%", "spots": "Manor Desk inside Central Village"},
            {"color": PRIO_YELLOW, "cont": "Chapel Altar", "item": "Book 3: Catéchisme", "i_ico": "book_catechisme.png", "rate": "100%", "spots": "Central Altar in Sarlat Chapel East of Village"}
        ],
        "roadmap": [
            {"quest": "Mount Sinai (Part 2: Jacques Bridge)", "items": [("Book 4: Montesquieu", "book_montesquieu.png"), ("Book 5: Buffon", "book_buffon.png")]},
            {"quest": "Mount Sinai (Part 3: Sombre Forest Finale)", "items": [("Book 6: Rondelet", "book_rondelet.png"), ("Book 7: Codex Medicamentarius", "book_mortuary.png")]}
        ]
    },

    # RAID 6: Jacques Bridge (Mount Sinai Books 4, 5) - NO FOCUS NEEDED
    {
        "id": 6,
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 2)",
        "has_focus": False,
        "story_pois": [
            {"x": 1391.83, "y": 1535.7,  "label": "Book 4: Montesquieu (North Tower)", "offset_dir": "left", "item_img": "book_montesquieu.png"},
            {"x": 2094.88, "y": 1346.36, "label": "Book 5: Buffon (Guardpost Storeroom)", "offset_dir": "right", "item_img": "book_buffon.png"}
        ],
        "active_objectives": [
            {
                "title": "Book 4: Montesquieu (De l'Esprit des Lois)",
                "npc": "Storeroom inside North Fortress Tower",
                "cont_name": "North Tower Archive Chest",
                "cont_img": "strongbox.webp",
                "item_img": "book_montesquieu.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Climb into the North Bridge fortress tower and take Book 4: Montesquieu."
            },
            {
                "title": "Book 5: Buffon (Histoire Naturelle)",
                "npc": "Guardpost Barracks East of South Tower",
                "cont_name": "Guardpost Storeroom Desk",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_buffon.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Infiltrate the lower bridge guardpost barracks and secure Book 5: Buffon."
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Book 4: Montesquieu from North Fortress Tower storeroom.", "color": PRIO_YELLOW},
            {"step": "Recover Book 5: Buffon from Guardpost storeroom desk.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Bridge Tower", "item": "Book 4: Montesquieu", "i_ico": "book_montesquieu.png", "rate": "100%", "spots": "Storeroom inside North Fortress Tower"},
            {"color": PRIO_YELLOW, "cont": "Guardpost Desk", "item": "Book 5: Buffon", "i_ico": "book_buffon.png", "rate": "100%", "spots": "Guardpost Barracks East of South Tower"}
        ],
        "roadmap": [
            {"quest": "Mount Sinai (Part 3: Sombre Forest Finale)", "items": [("Book 6: Rondelet", "book_rondelet.png"), ("Book 7: Codex Medicamentarius", "book_mortuary.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Mount Sinai Books 6, 7 & Finale!) - NO FOCUS NEEDED
    {
        "id": 7,
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Mount Sinai (Finale)",
        "has_focus": False,
        "story_pois": [
            {"x": 3168.6, "y": 2405.75, "label": "Book 6: Rondelet (Ruins Shrine)", "offset_dir": "left", "item_img": "book_rondelet.png"},
            {"x": 2592.18, "y": 2992.87, "label": "Book 7: Codex Medicamentarius (Ridge)", "offset_dir": "top", "item_img": "book_mortuary.png"}
        ],
        "active_objectives": [
            {
                "title": "Book 6: Rondelet (Histoire des Poissons)",
                "npc": "Ancient Stone Shrine inside South-Eastern Forest Ruins",
                "cont_name": "Ruins Stone Altar Cache",
                "cont_img": "strongbox.webp",
                "item_img": "book_rondelet.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Deep in Sombre Forest, search the stone shrine in ancient ruins to recover Book 6: Rondelet."
            },
            {
                "title": "Book 7: Codex Medicamentarius",
                "npc": "Cliffside Altar atop Southern Ridge overlooking Forest",
                "cont_name": "Ridge Shrine Strongbox",
                "cont_img": "strongbox.webp",
                "item_img": "book_mortuary.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Scale the Southern Ridge overlooking Sombre Forest to recover the final Codex Medicamentarius."
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Book 6: Rondelet from ancient shrine in Forest Ruins.", "color": PRIO_YELLOW},
            {"step": "Recover Book 7: Codex Medicamentarius from Southern Ridge altar.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Forest Ruins", "item": "Book 6: Rondelet", "i_ico": "book_rondelet.png", "rate": "100%", "spots": "Ancient Stone Shrine inside South-Eastern Forest Ruins"},
            {"color": PRIO_YELLOW, "cont": "Ridge Shrine", "item": "Book 7: Codex Medicamentarius", "i_ico": "book_mortuary.png", "rate": "100%", "spots": "Cliffside Altar atop Southern Ridge"}
        ],
        "roadmap": [
            {"quest": "Eloise Storyline 100% Complete!", "items": [("Storyline Cleared!", "gold_key.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS + (255,))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    draw.rectangle([0, 0, CANVAS_W, 78], fill=(17, 17, 14))
    draw.line([(0, 78), (CANVAS_W, 78)], fill=BORDER_SUBTLE, width=2)

    # Clean Pill: Just "RAID X OF 7"
    tag_txt = f"RAID {cfg['id']} OF 7"
    pill_tw = int(draw.textlength(tag_txt, font=F_HEADER_TAG))
    draw.rounded_rectangle([20, 16, 20 + pill_tw + 26, 60], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=1)
    draw.text((33, 26), tag_txt, fill=COLOR_GOLD, font=F_HEADER_TAG)

    # Title: MAP NAME - QUEST NAME (Hunger Companion Gold Serif)
    title_x = 20 + pill_tw + 45
    main_title = f"{cfg['map_name'].upper()}  -  {cfg['quest_name'].upper()}"
    draw.text((title_x, 22), main_title, fill=COLOR_GOLD, font=F_HEADER_TITLE)

    # Right tag: Wipe Speedrun
    status_txt = "SPEEDRUN STRATEGY - 7 DEDICATED DEPLOYMENTS"
    st_w = int(draw.textlength(status_txt, font=F_HEADER_TAG))
    draw.text((CANVAS_W - st_w - 24, 28), status_txt, fill=COLOR_MUTED, font=F_HEADER_TAG)

    # 2. LEFT MAP VIEWPORT
    map_box = [MAP_X, MAP_Y, MAP_X+MAP_W, MAP_Y+MAP_H]
    draw.rectangle(map_box, fill=(12, 12, 10), outline=BORDER_SUBTLE, width=2)

    if os.path.exists(cfg["map_img"]):
        raw_map = Image.open(cfg["map_img"]).convert("RGBA")
        resized_map = raw_map.resize((MAP_W-4, MAP_H-4), Image.Resampling.LANCZOS)
        canvas.paste(resized_map, (MAP_X+2, MAP_Y+2), resized_map)

    # 2a. PLOT DB FILTERED POINTS WITH CLUSTERING & CONNECTING LINES
    db_points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    core.plot_declustered_points(draw, canvas, db_points, to_map_coord)

    # 2b. PROMINENT STORY OBJECTIVE POI MARKERS
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'), item_img_name=poi.get('item_img'), canvas=canvas)

    # 2c. QUESTLINE PROGRESSION HUD BAR (MATCHES QUEST TITLES)
    core.render_questline_progression_bar(draw, cfg["id"])

    # 3. RIGHT BRIEFING PANEL (HUNGER COMPANION OBSIDIAN CARD STYLING)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=BG_PANEL, outline=BORDER_SUBTLE, width=2)

    has_focus = cfg.get("has_focus", True)
    gap = 14

    if has_focus:
        # Standard Raids 1 to 3 (5 categories)
        b1_y = PANEL_Y + 14   # 96
        b1_h = 176

        b2_y = b1_y + b1_h + gap # 286
        b2_h = 110            # Punchy Focus without repetitive text!

        b3_y = b2_y + b2_h + gap # 410
        b3_h = 200            # More spacious Priorities!

        b4_y = b3_y + b3_h + gap # 624
        b4_h = 400            # Drops with two lines

        b5_y = b4_y + b4_h + gap # 1038
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 328
    else:
        # Raids 4, 5, 6, 7 (NO FOCUS NEEDED -> 4 spacious categories)
        b1_y = PANEL_Y + 14   # 96
        b1_h = 280            # All active objectives expanded!

        b2_y = b1_y
        b2_h = 0

        b3_y = b1_y + b1_h + gap # 390
        b3_h = 200            # Spacious Priorities!

        b4_y = b3_y + b3_h + gap # 604
        b4_h = 280            # Drops

        b5_y = b4_y + b4_h + gap # 898
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 468 (Expansive Quests roadmap)

    # ==========================================
    # CATEGORY 1: Objectives (Serif Gold Title, Coherent Info, No Coords)
    # ==========================================
    draw.text((PANEL_X+18, b1_y), "Objectives", fill=COLOR_GOLD, font=F_SECTION_TITLE)

    objs = cfg.get("active_objectives", [])
    if len(objs) == 1:
        o = objs[0]
        card_y = b1_y + 32
        card_h = b1_h - 32
        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=BG_CARD, outline=COLOR_GOLD, width=2)

        c_img = core.CONTAINER_IMGS.get(o["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, card_y+16, 76, 76), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
        i_img = core.ITEM_IMGS.get(o["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+88, card_y+46, 46, 46), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

        tx = PANEL_X + 148
        max_tw = PANEL_W - 170
        draw.text((tx, card_y+14), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
        
        rate_density = f"Drop Rate: {o['drop_rate']}   -   {o['density']}"
        draw.text((tx, card_y+42), core.fit_text(draw, rate_density, F_BODY_BOLD, max_tw), fill=COLOR_GOLD, font=F_BODY_BOLD)
        draw.text((tx, card_y+70), core.fit_text(draw, o["desc"], F_BODY, max_tw), fill=COLOR_MUTED, font=F_BODY)
        draw.text((tx, card_y+98), core.fit_text(draw, o["npc"], F_BODY_BOLD, max_tw), fill=(74, 222, 128), font=F_BODY_BOLD)
    elif len(objs) == 2:
        card_y = b1_y + 32
        each_h = int((b1_h - 32 - 8) / 2)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+24, card_y+8, 52, 52), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+66, card_y+24, 34, 34), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

            tx = PANEL_X + 114
            max_tw = PANEL_W - 140
            draw.text((tx, card_y+8), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
            line2 = f"Drop: {o['drop_rate']}  |  {o['density']}"
            draw.text((tx, card_y+34), core.fit_text(draw, line2, F_BODY, max_tw), fill=COLOR_GOLD, font=F_BODY)
            card_y += each_h + 8
    else:
        # 3 Objectives (Raid 5)
        card_y = b1_y + 32
        each_h = int((b1_h - 32 - 16) / 3)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+22, card_y+8, 52, 52), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+64, card_y+22, 34, 34), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

            tx = PANEL_X + 110
            max_tw = PANEL_W - 135
            draw.text((tx, card_y+8), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
            draw.text((tx, card_y+34), core.fit_text(draw, f"Location: {o['npc']}", F_BODY, max_tw), fill=(74, 222, 128), font=F_BODY)
            card_y += each_h + 8

    # ==========================================
    # CATEGORY 2: Focus (No Repetition, Drop Rate & POI Location Cleanly Fitted)
    # ==========================================
    if has_focus:
        pf = cfg.get("priority_focus", {})
        pf_color = pf.get("color", PRIO_PURPLE)
        draw.text((PANEL_X+18, b2_y), "Focus", fill=COLOR_GOLD, font=F_SECTION_TITLE)

        card_y = b2_y + 30
        card_h = b2_h - 30

        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=BG_CARD, outline=pf_color, width=2)

        c_img = core.CONTAINER_IMGS.get(pf.get("c_ico"))
        core.paste_icon_safe(canvas, c_img, (PANEL_X+26, card_y+10, 56, 56), bg_color=(16, 16, 13), border_color=pf_color, border_w=2)
        i_img = core.ITEM_IMGS.get(pf.get("i_ico"))
        core.paste_icon_safe(canvas, i_img, (PANEL_X+70, card_y+28, 36, 36), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

        tx = PANEL_X + 120
        max_tw = PANEL_W - 145
        draw.text((tx, card_y+10), core.fit_text(draw, pf.get('title', ''), F_CARD_TITLE, max_tw), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
        draw.text((tx, card_y+38), core.fit_text(draw, pf.get('detail', ''), F_BODY_BOLD, max_tw), fill=pf_color, font=F_BODY_BOLD)

    # ==========================================
    # CATEGORY 3: Priorities (Spaced Out, Bigger, Coherent Extraction Phrasing)
    # ==========================================
    draw.text((PANEL_X+18, b3_y), "Priorities", fill=COLOR_GOLD, font=F_SECTION_TITLE)
    draw.rounded_rectangle([PANEL_X+18, b3_y+30, PANEL_X+PANEL_W-18, b3_y+b3_h], radius=8, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)

    step_y = b3_y + 38
    steps_list = cfg["rotation_steps"]
    step_spacing = min(36, int((b3_h - 44) / max(1, len(steps_list))))

    for i, s_obj in enumerate(steps_list, 1):
        step_text = s_obj["step"]
        prio_color = s_obj["color"]

        num_cx = PANEL_X + 42
        num_cy = step_y + 12
        draw.ellipse([num_cx-12, num_cy-12, num_cx+12, num_cy+12], fill=prio_color, outline=(10, 10, 8), width=1)
        num_fg = (10, 10, 8) if prio_color in (PRIO_YELLOW, PRIO_GREEN) else (255, 255, 255)
        num_tw = draw.textlength(str(i), font=F_SMALL_BOLD)
        draw.text((num_cx - num_tw/2, num_cy - 8), str(i), fill=num_fg, font=F_SMALL_BOLD)

        draw.text((PANEL_X+66, step_y+2), core.fit_text(draw, step_text, F_CARD_TITLE, PANEL_W - 95), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
        step_y += step_spacing

    # ==========================================
    # CATEGORY 4: Drops (POI Directions, Embedded Item Thumbnail Badge)
    # ==========================================
    draw.rounded_rectangle([PANEL_X+18, b4_y, PANEL_X+PANEL_W-18, b4_y+b4_h], radius=10, fill=BG_CARD, outline=BORDER_SUBTLE, width=2)
    draw.text((PANEL_X+32, b4_y+10), "Drops", fill=COLOR_GOLD, font=F_SECTION_TITLE)

    # Legend Bar: Priority 1, Priority 2, Priority 3, Priority 4
    sb_y = b4_y + 36
    draw.rounded_rectangle([PANEL_X+28, sb_y, PANEL_X+PANEL_W-28, sb_y+26], radius=5, fill=(18, 18, 15), outline=BORDER_SUBTLE, width=1)

    draw.ellipse([PANEL_X+38, sb_y+8, PANEL_X+48, sb_y+18], fill=PRIO_YELLOW)
    draw.text((PANEL_X+54, sb_y+6), "Priority 1", fill=PRIO_YELLOW, font=F_TINY)

    draw.ellipse([PANEL_X+180, sb_y+8, PANEL_X+190, sb_y+18], fill=PRIO_PURPLE)
    draw.text((PANEL_X+196, sb_y+6), "Priority 2", fill=PRIO_PURPLE, font=F_TINY)

    draw.ellipse([PANEL_X+320, sb_y+8, PANEL_X+330, sb_y+18], fill=PRIO_BLUE)
    draw.text((PANEL_X+336, sb_y+6), "Priority 3", fill=PRIO_BLUE, font=F_TINY)

    draw.ellipse([PANEL_X+460, sb_y+8, PANEL_X+470, sb_y+18], fill=PRIO_GREEN)
    draw.text((PANEL_X+476, sb_y+6), "Priority 4", fill=PRIO_GREEN, font=F_TINY)

    # Render Directory Rows
    dir_y = sb_y + 34
    dir_items = cfg.get("directory", [])
    row_count = len(dir_items)
    
    avail_rows_h = b4_h - 70
    row_h = min(58, int(avail_rows_h / max(1, row_count)))

    for itm in dir_items:
        badge_cx = PANEL_X + 46
        badge_cy = dir_y + int(row_h / 2)
        core.draw_container_shape(draw, badge_cx, badge_cy, 12, itm['color'], item_img_name=itm.get('i_ico'), canvas=canvas)

        # Line 1: Container -> Item
        label_text = f"{itm['cont']}  ->  {itm['item']}"
        draw.text((PANEL_X+72, dir_y+3), core.fit_text(draw, label_text, F_CARD_TITLE, PANEL_W - 110), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)

        # Line 2: Drop rate and spots with POI direction!
        spots_str = itm.get('spots', '')
        rate_str = itm.get('rate', '')
        sub_info = f"Drop Rate: {rate_str}   •   {spots_str}" if spots_str else f"Drop Rate: {rate_str}"
        draw.text((PANEL_X+72, dir_y+27), core.fit_text(draw, sub_info, F_SMALL, PANEL_W - 110), fill=COLOR_MUTED, font=F_SMALL)

        dir_y += row_h

    # ==========================================
    # CATEGORY 5: Quests (Grammatically Correct, Never Overflows)
    # ==========================================
    draw.text((PANEL_X+18, b5_y), "Quests", fill=COLOR_GOLD, font=F_SECTION_TITLE)

    r_y = b5_y + 32
    roadmap_list = cfg.get("roadmap", [])
    card_h = 44 if len(roadmap_list) >= 4 else 52

    for r_card in roadmap_list:
        draw.rounded_rectangle([PANEL_X+18, r_y, PANEL_X+PANEL_W-18, r_y+card_h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
        
        # Left: Quest Title
        draw.text((PANEL_X+26, r_y+int((card_h-18)/2)), core.fit_text(draw, r_card["quest"], F_BODY_BOLD, 210), fill=COLOR_GOLD, font=F_BODY_BOLD)

        # Right: Items laid out as compact pills
        item_x = PANEL_X + 245
        for item_name, item_ico in r_card["items"]:
            ico_im = core.ITEM_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, r_y+int((card_h-26)/2), 26, 26), bg_color=(16, 16, 13))
            draw.text((item_x+32, r_y+int((card_h-18)/2)), item_name, fill=COLOR_PARCHMENT, font=F_SMALL_BOLD)
            item_x += int(draw.textlength(item_name, font=F_SMALL_BOLD)) + 40

        r_y += card_h + 8

    # Save final artifact image
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating all 7 perfect V21 briefings with Hunger Companion theme & declustering...")
    for raid in RAIDS_CONFIG:
        render_briefing(raid)
    print("All 7 briefings generated successfully!")
