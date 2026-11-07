import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v24 as core

CANVAS_W = core.CANVAS_W
CANVAS_H = core.CANVAS_H
HEADER_H = core.HEADER_H
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

# Standard Fonts
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
                "cont_img": "flour_sack.webp",
                "item_img": "flour.png"
            }
        ],
        "priority_focus": {
            "title": "15x Charcoal",
            "item": "15x Charcoal",
            "c_ico": "pile_of_ash.webp",
            "i_ico": "charcoal.png",
            "color": PRIO_PURPLE,
            "detail": "52.6% Drop Rate  •  In Fireplace Hearths North of Village"
        },
        "rotation_steps": [
            {"step": "Gather 20x Flour.", "color": PRIO_YELLOW},
            {"step": "Gather 15x Charcoal.", "color": PRIO_PURPLE},
            {"step": "Search for Bare Necessities supplies: Saltpetre, Damp Rags, Balm.", "color": PRIO_BLUE},
            {"step": "Search for Opium Pipe and China Bowl.", "color": PRIO_GREEN},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "flour_sack": {"keyword": "Flour Sack", "color": PRIO_YELLOW, "cont_img": "flour_sack.webp", "item_img": "flour.png", "label": "Flour Sack", "is_prio": True},
            "pile_of_ash": {"keyword": "Pile of Ash", "color": PRIO_PURPLE, "cont_img": "pile_of_ash.webp", "item_img": "charcoal.png", "label": "Pile of Ash"},
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_BLUE, "cont_img": "tooling_bin.webp", "item_img": "saltpetre.png", "label": "Tooling Bin"},
            "stone_grave": {"keyword": "Stone Grave", "color": PRIO_BLUE, "cont_img": "stone_grave.webp", "item_img": "damp_rag.png", "label": "Stone Grave"},
            "physician": {"keyword": "Physician", "color": PRIO_BLUE, "cont_img": "physician_bag.webp", "item_img": "tallow_balm.png", "label": "Physician Cabinet"},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_GREEN, "cont_img": "bullion_box.webp", "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_GREEN, "cont_img": "wall_cabinet.webp", "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "20x Flour", "i_ico": "flour.png", "rate": "47.6%", "spots": "40 Spots in Central Village & Granaries East of Château"},
            {"color": PRIO_PURPLE, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "14 Spots in Manor Hearths North of Village"},
            {"color": PRIO_BLUE, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots in Workshops North of Windmill & Gunline Fort"},
            {"color": PRIO_BLUE, "cont": "Stone Grave", "c_ico": "stone_grave.webp", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots in Chapel Cemetery East of Central Village"},
            {"color": PRIO_BLUE, "cont": "Physician's Cabinet", "c_ico": "physician_bag.webp", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters South of Master Granary"},
            {"color": PRIO_GREEN, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_GREEN, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 2: Jacques Bridge (Camp & Charcoal)
    {
        "id": 2,
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3 & 4: Camp & Charcoal",
        "has_focus": True,
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp", "offset_dir": "bottom", "cont_img": "ledger_desk.webp"}
        ],
        "active_objectives": [
            {
                "title": "Quest 3: Locate Gavroche Family Camp",
                "cont_img": "ledger_desk.webp",
                "item_img": "silver_key.png"
            },
            {
                "title": "Quest 4: Gather 15x Charcoal",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png"
            }
        ],
        "priority_focus": {
            "title": "Bare Necessities Supplies",
            "item": "Saltpetre, Damp Rags, Tallow Balm",
            "c_ico": "tooling_bin.webp",
            "i_ico": "saltpetre.png",
            "color": PRIO_PURPLE,
            "detail": "High-Density Supplies in Bridge Workshops & Fort Desks"
        },
        "rotation_steps": [
            {"step": "Scout Gavroche Family Camp on Lower Bridge Deck.", "color": PRIO_YELLOW},
            {"step": "Gather 15x Charcoal.", "color": PRIO_YELLOW},
            {"step": "Search for Bare Necessities supplies: Saltpetre, Damp Rags, Balm.", "color": PRIO_PURPLE},
            {"step": "Search for Opium Pipe and China Bowl in officer quarters.", "color": PRIO_BLUE},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "pile_of_ash": {"keyword": "Pile of Ash", "color": PRIO_YELLOW, "cont_img": "pile_of_ash.webp", "item_img": "charcoal.png", "label": "Pile of Ash", "is_prio": True},
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_PURPLE, "cont_img": "tooling_bin.webp", "item_img": "saltpetre.png", "label": "Tooling Bin"},
            "old_bucket": {"keyword": "Old Bucket", "color": PRIO_PURPLE, "cont_img": "basket.webp", "item_img": "damp_rag.png", "label": "Old Bucket"},
            "physician": {"keyword": "Physician", "color": PRIO_PURPLE, "cont_img": "jacques_medicinals.webp", "item_img": "tallow_balm.png", "label": "Physician Cabinet"},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_BLUE, "cont_img": "bullion_box.webp", "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_BLUE, "cont_img": "wall_cabinet.webp", "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "13 Spots in Bridge Guardhouses & Lower Deck Hearths"},
            {"color": PRIO_PURPLE, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "24 Spots in Workshops Across Bridge Roadway"},
            {"color": PRIO_PURPLE, "cont": "Old Bucket", "c_ico": "basket.webp", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "10 Spots in Lower Deck Shanties & Bilges"},
            {"color": PRIO_PURPLE, "cont": "Physician's Cabinet", "c_ico": "jacques_medicinals.webp", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Field Hospital Post on Middle Pier"},
            {"color": PRIO_BLUE, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "27 Spots in Officer Bunkers North & South"},
            {"color": PRIO_BLUE, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "3 Spots in Officer Messrooms West of Guardhouse"}
        ],
        "roadmap": [
            {"quest": "Quest 6: Bare Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
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
            {"x": 1140, "y": 1307, "label": "Gunline Fort Tactical Map", "offset_dir": "top", "cont_img": "ledger_desk.webp"}
        ],
        "active_objectives": [
            {
                "title": "Quest 5: Scout Gunline Fort Tactical Map",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png"
            },
            {
                "title": "Quest 6: Gather Bare Necessities Supplies",
                "cont_img": "tooling_bin.webp",
                "item_img": "saltpetre.png"
            }
        ],
        "priority_focus": {
            "title": "Opium Pipe & China Bowl",
            "item": "1x Opium Pipe & 1x China Bowl",
            "c_ico": "bullion_box.webp",
            "i_ico": "opium_pipe.png",
            "color": PRIO_PURPLE,
            "detail": "13.7% / 16.1% Drop Rate  •  In Manor Desks & Kitchen Cabinets East of Windmill"
        },
        "rotation_steps": [
            {"step": "Inspect Tactical Map in Gunline Fort command bunker.", "color": PRIO_YELLOW},
            {"step": "Gather 20x Saltpetre.", "color": PRIO_YELLOW},
            {"step": "Gather 5x Damp Rags.", "color": PRIO_YELLOW},
            {"step": "Gather 10x Tallow Balm.", "color": PRIO_YELLOW},
            {"step": "Search for Opium Pipe and China Bowl.", "color": PRIO_PURPLE},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "tooling_bin": {"keyword": "Tooling Bin", "color": PRIO_YELLOW, "cont_img": "tooling_bin.webp", "item_img": "saltpetre.png", "label": "Tooling Bin", "is_prio": True},
            "stone_grave": {"keyword": "Stone Grave", "color": PRIO_YELLOW, "cont_img": "stone_grave.webp", "item_img": "damp_rag.png", "label": "Stone Grave", "is_prio": True},
            "physician": {"keyword": "Physician", "color": PRIO_YELLOW, "cont_img": "physician_bag.webp", "item_img": "tallow_balm.png", "label": "Physician Cabinet", "is_prio": True},
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_PURPLE, "cont_img": "bullion_box.webp", "item_img": "opium_pipe.png", "label": "Bullion Box"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_BLUE, "cont_img": "wall_cabinet.webp", "item_img": "china_bowl.png", "label": "Wall Cabinet"}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Gunline Fort", "c_ico": "ledger_desk.webp", "item": "Tactical Map", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Western Fort Command Bunker Table"},
            {"color": PRIO_YELLOW, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Spots in Workshops North of Windmill & Gunline Fort"},
            {"color": PRIO_YELLOW, "cont": "Stone Grave", "c_ico": "stone_grave.webp", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Spots in Chapel Cemetery East of Central Village"},
            {"color": PRIO_YELLOW, "cont": "Physician's Cabinet", "c_ico": "physician_bag.webp", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters South of Master Granary"},
            {"color": PRIO_PURPLE, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_BLUE, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 9: A Touch of Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Sarlat Farm (Candle & Bribery) - NO FOCUS NEEDED
    {
        "id": 4,
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8 & 9: Candle & Bribery",
        "has_focus": False,
        "story_pois": [
            {"x": 2697, "y": 807, "label": "Sarlat Chapel Altar", "offset_dir": "bottom", "cont_img": "stone_grave.webp"}
        ],
        "active_objectives": [
            {
                "title": "Quest 8: Recover Red Votive Candle",
                "cont_img": "stone_grave.webp",
                "item_img": "votive_candle.png"
            },
            {
                "title": "Quest 9: Recover Opium Pipe & China Bowl",
                "cont_img": "bullion_box.webp",
                "item_img": "opium_pipe.png"
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Red Votive Candle from Sarlat Chapel altar.", "color": PRIO_YELLOW},
            {"step": "Gather 1x Opium Pipe.", "color": PRIO_YELLOW},
            {"step": "Gather 1x China Bowl.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "bullion_box": {"keyword": "Bullion Box", "color": PRIO_YELLOW, "cont_img": "bullion_box.webp", "item_img": "opium_pipe.png", "label": "Bullion Box", "is_prio": True},
            "wall_cabinet": {"keyword": "Wall Cabinet", "color": PRIO_YELLOW, "cont_img": "wall_cabinet.webp", "item_img": "china_bowl.png", "label": "Wall Cabinet", "is_prio": True}
        },
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Chapel Altar", "c_ico": "stone_grave.webp", "item": "Votive Candle", "i_ico": "votive_candle.png", "rate": "100%", "spots": "Main Altar Table inside Sarlat Chapel"},
            {"color": PRIO_YELLOW, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Spots in Manor Desks North & East of Village"},
            {"color": PRIO_YELLOW, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Spots in Kitchen Wall Cabinets East of Windmill"}
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 5: Sarlat Farm (Sinai Part 1) - NO FOCUS NEEDED
    {
        "id": 5,
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 1)",
        "has_focus": False,
        "story_pois": [
            {"x": 2187, "y": 807, "label": "Book 1: Rozier (Manor Library)", "offset_dir": "top", "cont_img": "ledger_desk.webp"},
            {"x": 2724, "y": 1420, "label": "Book 2: Census (Master Granary)", "offset_dir": "right", "cont_img": "strongbox.webp"},
            {"x": 2697, "y": 807, "label": "Book 3: Catechisme (Chapel Altar)", "offset_dir": "bottom", "cont_img": "stone_grave.webp"}
        ],
        "active_objectives": [
            {
                "title": "Book 1: Rozier (Cours Complet d'Agriculture)",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_rozier.png"
            },
            {
                "title": "Book 2: Census of Sarlat Parish",
                "cont_img": "strongbox.webp",
                "item_img": "book_census.png"
            },
            {
                "title": "Book 3: Catechisme du Diocese",
                "cont_img": "stone_grave.webp",
                "item_img": "book_catechisme.png"
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Book 1: Rozier from Manor Library bookshelf.", "color": PRIO_YELLOW},
            {"step": "Recover Book 2: Census from Master Granary ledger desk.", "color": PRIO_YELLOW},
            {"step": "Recover Book 3: Catechisme from Sarlat Chapel altar.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Manor Library", "c_ico": "ledger_desk.webp", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Upper Floor Library Bookshelf in Sarlat Manor"},
            {"color": PRIO_YELLOW, "cont": "Master Granary", "c_ico": "strongbox.webp", "item": "Book 2: Census", "i_ico": "book_census.png", "rate": "100%", "spots": "Foreman Ledger Desk inside Central Granary"},
            {"color": PRIO_YELLOW, "cont": "Chapel Altar", "c_ico": "stone_grave.webp", "item": "Book 3: Catechisme", "i_ico": "book_catechisme.png", "rate": "100%", "spots": "Stone Altar Pedestal inside Sarlat Chapel"}
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Part 2)", "items": [("Books 4 & 5", "book_montesquieu.png")]},
            {"quest": "Quest 10: Mount Sinai (Finale)", "items": [("Books 6 & 7", "book_rondelet.png")]}
        ]
    },

    # RAID 6: Jacques Bridge (Sinai Part 2) - NO FOCUS NEEDED
    {
        "id": 6,
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 10: Mount Sinai (Part 2)",
        "has_focus": False,
        "story_pois": [
            {"x": 1500, "y": 320, "label": "Book 4: Montesquieu (Lower Bridge)", "offset_dir": "bottom", "cont_img": "ledger_desk.webp"},
            {"x": 1690, "y": 880, "label": "Book 5: Buffon (Bridge Fort Table)", "offset_dir": "top", "cont_img": "strongbox.webp"}
        ],
        "active_objectives": [
            {
                "title": "Book 4: Montesquieu (De l'Esprit des Lois)",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_montesquieu.png"
            },
            {
                "title": "Book 5: Buffon (Histoire Naturelle)",
                "cont_img": "strongbox.webp",
                "item_img": "book_buffon.png"
            }
        ],
        "priority_focus": None,
        "rotation_steps": [
            {"step": "Recover Book 4: Montesquieu from lower deck shanty table.", "color": PRIO_YELLOW},
            {"step": "Recover Book 5: Buffon from command post fort desk.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"color": PRIO_YELLOW, "cont": "Lower Bridge Deck", "c_ico": "ledger_desk.webp", "item": "Book 4: Montesquieu", "i_ico": "book_montesquieu.png", "rate": "100%", "spots": "Camp Table beside Gavroche Quarters"},
            {"color": PRIO_YELLOW, "cont": "Bridge Fort Post", "c_ico": "strongbox.webp", "item": "Book 5: Buffon", "i_ico": "book_buffon.png", "rate": "100%", "spots": "Fort Command Bunker Map Table North Roadway"}
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Finale)", "items": [("Books 6 & 7", "book_rondelet.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Sinai Finale) - NO FOCUS NEEDED
    {
        "id": 7,
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Mount Sinai (Finale)",
        "has_focus": False,
        "story_pois": [
            {"x": 3168.6, "y": 2405.75, "label": "Book 6: Rondelet (Ruins Shrine)", "offset_dir": "left", "cont_img": "strongbox.webp"},
            {"x": 2592.18, "y": 2992.87, "label": "Book 7: Codex Medicamentarius (Ridge)", "offset_dir": "top", "cont_img": "stone_grave.webp"}
        ],
        "active_objectives": [
            {
                "title": "Book 6: Rondelet (Histoire des Poissons)",
                "cont_img": "strongbox.webp",
                "item_img": "book_rondelet.png"
            },
            {
                "title": "Book 7: Codex Medicamentarius",
                "cont_img": "strongbox.webp",
                "item_img": "book_mortuary.png"
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
            {"color": PRIO_YELLOW, "cont": "Forest Ruins", "c_ico": "strongbox.webp", "item": "Book 6: Rondelet", "i_ico": "book_rondelet.png", "rate": "100%", "spots": "Ancient Stone Shrine inside South-Eastern Forest Ruins"},
            {"color": PRIO_YELLOW, "cont": "Ridge Shrine", "c_ico": "stone_grave.webp", "item": "Book 7: Codex Medicamentarius", "i_ico": "book_mortuary.png", "rate": "100%", "spots": "Cliffside Altar atop Southern Ridge"}
        ],
        "roadmap": [
            {"quest": "Eloise Storyline 100% Complete!", "items": [("Storyline Cleared!", "gold_key.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS + (255,))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR: Full-Width 7-Raid Progression Bar Edge-to-Edge!
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(17, 17, 14))
    draw.line([(0, HEADER_H), (CANVAS_W, HEADER_H)], fill=BORDER_SUBTLE, width=2)
    core.render_header_progression_bar(draw, cfg["id"])

    # 2. LEFT MAP VIEWPORT (Full vertical view, NO HUD overlay!)
    map_box = [MAP_X, MAP_Y, MAP_X+MAP_W, MAP_Y+MAP_H]
    draw.rectangle(map_box, fill=(12, 12, 10), outline=BORDER_SUBTLE, width=2)

    if os.path.exists(cfg["map_img"]):
        raw_map = Image.open(cfg["map_img"]).convert("RGBA")
        resized_map = raw_map.resize((MAP_W-4, MAP_H-4), Image.Resampling.LANCZOS)
        canvas.paste(resized_map, (MAP_X+2, MAP_Y+2), resized_map)

    # 2a. PLOT DECLUSTERED MAP MARKERS:
    # - BIGGER BADGES (r=24)
    # - WIDER CONNECTING LINES (width=4)
    # - CONTAINER IMAGES
    # - GUARANTEED ZERO OVERLAPS
    db_points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    core.plot_declustered_points(draw, canvas, db_points, to_map_coord)

    # 2b. PROMINENT STORY OBJECTIVE POI MARKERS (r=22)
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'), cont_img_name=poi.get('cont_img'), canvas=canvas)

    # 3. RIGHT BRIEFING PANEL (HUNGER COMPANION OBSIDIAN CARD STYLING)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=BG_PANEL, outline=BORDER_SUBTLE, width=2)

    has_focus = cfg.get("has_focus", True)
    gap = 14

    if has_focus:
        # Raids 1 to 3 (5 categories)
        b1_y = PANEL_Y + 14   # 102
        b1_h = 160            # Punchy Objectives (No small text!)

        b2_y = b1_y + b1_h + gap # 276
        b2_h = 104            # Punchy Focus

        b3_y = b2_y + b2_h + gap # 394
        b3_h = 210            # Spacious Priorities

        b4_y = b3_y + b3_h + gap # 618
        b4_h = 420            # Big readable Drops

        b5_y = b4_y + b4_h + gap # 1052
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 314
    else:
        # Raids 4, 5, 6, 7 (NO FOCUS NEEDED -> 4 categories)
        b1_y = PANEL_Y + 14   # 102
        b1_h = 240            # Objectives (No small text!)

        b2_y = b1_y
        b2_h = 0

        b3_y = b1_y + b1_h + gap # 356
        b3_h = 210            # Spacious Priorities

        b4_y = b3_y + b3_h + gap # 580
        b4_h = 300            # Big Drops

        b5_y = b4_y + b4_h + gap # 894
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 472 (Expansive Quests)

    # ==========================================
    # CATEGORY 1: Objectives (NO SMALL TEXT, BOLD & CLEAN)
    # ==========================================
    draw.text((PANEL_X+18, b1_y), "Objectives", fill=COLOR_GOLD, font=F_SECTION_TITLE)

    objs = cfg.get("active_objectives", [])
    if len(objs) == 1:
        o = objs[0]
        card_y = b1_y + 32
        card_h = b1_h - 32
        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=BG_CARD, outline=COLOR_GOLD, width=2)

        c_img = core.CONTAINER_IMGS.get(o["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, card_y+int((card_h-74)/2), 74, 74), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
        i_img = core.ITEM_IMGS.get(o["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+88, card_y+int((card_h-74)/2)+26, 46, 46), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

        tx = PANEL_X + 154
        draw.text((tx, card_y+int((card_h-22)/2)), o["title"], fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
    elif len(objs) == 2:
        card_y = b1_y + 32
        each_h = int((b1_h - 32 - 8) / 2)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+24, card_y+int((each_h-50)/2), 50, 50), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+64, card_y+int((each_h-50)/2)+16, 32, 32), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

            tx = PANEL_X + 114
            draw.text((tx, card_y+int((each_h-20)/2)), o["title"], fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
            card_y += each_h + 8
    else:
        # 3 Objectives (Raid 5)
        card_y = b1_y + 32
        each_h = int((b1_h - 32 - 16) / 3)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+22, card_y+int((each_h-46)/2), 46, 46), bg_color=(16, 16, 13), border_color=COLOR_GOLD, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+58, card_y+int((each_h-46)/2)+14, 30, 30), bg_color=(16, 16, 13), border_color=BORDER_SUBTLE, border_w=1)

            tx = PANEL_X + 104
            draw.text((tx, card_y+int((each_h-20)/2)), o["title"], fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
            card_y += each_h + 8

    # ==========================================
    # CATEGORY 2: Focus (No Repetition, Item Name Without 'Focus:' Prefix)
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
        draw.text((tx, card_y+10), pf.get('title', ''), fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
        draw.text((tx, card_y+38), pf.get('detail', ''), fill=pf_color, font=F_BODY_BOLD)

    # ==========================================
    # CATEGORY 3: Priorities (No Locations for Drops, Standard Extraction Phrasing)
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

        draw.text((PANEL_X+66, step_y+2), step_text, fill=COLOR_PARCHMENT, font=F_CARD_TITLE)
        step_y += step_spacing

    # ==========================================
    # CATEGORY 4: Drops (Big, Highly Readable, POI Directions, Container Image)
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

    # Render Big Readable Directory Rows with Container Badges
    dir_y = sb_y + 34
    dir_items = cfg.get("directory", [])
    row_count = len(dir_items)
    
    avail_rows_h = b4_h - 70
    row_h = min(58, int(avail_rows_h / max(1, row_count)))

    for itm in dir_items:
        badge_cx = PANEL_X + 48
        badge_cy = dir_y + int(row_h / 2)
        core.draw_container_shape(draw, badge_cx, badge_cy, 16, itm['color'], cont_img_name=itm.get('c_ico'), canvas=canvas)

        # Line 1: Big Clear Title
        label_text = f"{itm['cont']}  ->  {itm['item']}"
        draw.text((PANEL_X+76, dir_y+3), label_text, fill=COLOR_PARCHMENT, font=F_CARD_TITLE)

        # Line 2: Drop rate and spots with POI direction
        spots_str = itm.get('spots', '')
        rate_str = itm.get('rate', '')
        sub_info = f"Drop Rate: {rate_str}   •   {spots_str}" if spots_str else f"Drop Rate: {rate_str}"
        draw.text((PANEL_X+76, dir_y+27), sub_info, fill=COLOR_MUTED, font=F_SMALL_BOLD)

        dir_y += row_h

    # ==========================================
    # CATEGORY 5: Quests (NO TEXT CLIPPING ON TOP OF ANOTHER!)
    # ==========================================
    draw.text((PANEL_X+18, b5_y), "Quests", fill=COLOR_GOLD, font=F_SECTION_TITLE)

    r_y = b5_y + 32
    roadmap_list = cfg.get("roadmap", [])
    card_h = 44 if len(roadmap_list) >= 4 else 52

    for r_card in roadmap_list:
        draw.rounded_rectangle([PANEL_X+18, r_y, PANEL_X+PANEL_W-18, r_y+card_h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
        
        q_title = r_card["quest"]
        q_tw = int(draw.textlength(q_title, font=F_BODY_BOLD))
        draw.text((PANEL_X+26, r_y+int((card_h-18)/2)), q_title, fill=COLOR_GOLD, font=F_BODY_BOLD)

        # Dynamic offset ensures item icons & labels NEVER clip into quest title!
        item_x = max(PANEL_X + 236, PANEL_X + 26 + q_tw + 18)
        for item_name, item_ico in r_card["items"]:
            ico_im = core.ITEM_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, r_y+int((card_h-26)/2), 26, 26), bg_color=(16, 16, 13))
            draw.text((item_x+32, r_y+int((card_h-18)/2)), item_name, fill=COLOR_PARCHMENT, font=F_SMALL_BOLD)
            item_x += int(draw.textlength(item_name, font=F_SMALL_BOLD)) + 36

        r_y += card_h + 8

    # Save final artifact image
    out_name = f"raid{cfg['id']}_map.jpg"
    out_path = os.path.join(ARTIFACT_DIR, out_name)
    canvas.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating all 7 perfect V24 briefings...")
    for raid in RAIDS_CONFIG:
        render_briefing(raid)
    print("All 7 briefings generated successfully!")
