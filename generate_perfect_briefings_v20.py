import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v20 as core

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
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 2: Making Dough",
        "has_focus": True,
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
            {"step": "Find 20x Flour in farmhouses and granaries (Quest 2).", "color": PRIO_YELLOW},
            {"step": "Search hearths and fire pits for 15x Charcoal (Quest 4).", "color": PRIO_PURPLE},
            {"step": "Search Tooling Bins, Graves, and Cabinets for Quest 6.", "color": PRIO_BLUE},
            {"step": "Search desks for Bullion Box and living quarters for Wall Cabinet.", "color": PRIO_GREEN},
            {"step": "Extract to Château and turn in 20x Flour to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "flour_sack": {"keyword": "Flour Sack", "shape": "wide_circle", "color": PRIO_YELLOW, "item_img": "flour.png", "label": "Flour Sack (20x Flour - Active Q2)", "is_prio": True},
            "pile_of_ash": {"keyword": "Pile of Ash", "shape": "circle", "color": PRIO_PURPLE, "item_img": "charcoal.png", "label": "Pile of Ash (15x Charcoal - Future Q4)"},
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "circle", "color": PRIO_BLUE, "item_img": "saltpetre.png", "label": "Tooling Bin (20x Saltpetre - Future Q6)"},
            "stone_grave": {"keyword": "Stone Grave", "shape": "circle", "color": PRIO_BLUE, "item_img": "damp_rag.png", "label": "Stone Grave (5x Damp Rag - Future Q6)"},
            "physician": {"keyword": "Physician", "shape": "circle", "color": PRIO_BLUE, "item_img": "tallow_balm.png", "label": "Physician Cabinet (10x Tallow Balm - Future Q6)"},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_GREEN, "item_img": "opium_pipe.png", "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_GREEN, "item_img": "china_bowl.png", "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Flour Sack", "item": "20x Flour", "i_ico": "flour.png", "rate": "47.6%", "spots": "40 Spots across farmhouses & granaries"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Pile of Ash", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "14 Fireplace hearths"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Tooling bins in sheds"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Stone Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Graves in church cemetery"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters medical bags"},
            {"shape": "circle", "color": PRIO_GREEN, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Bedroom desks in manors"},
            {"shape": "circle", "color": PRIO_GREEN, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Kitchen wall cabinets"}
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
    {
        "id": 2,
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 3: Gavroche Camp  &  Quest 4: Charcoal",
        "has_focus": True,
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp", "offset_dir": "bottom", "item_img": "silver_key.png"}
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
            {"step": "Go to lower bridge deck and scout Gavroche Camp (Quest 3).", "color": PRIO_YELLOW},
            {"step": "Search guardhouse hearths to gather 15x Charcoal (Quest 4).", "color": PRIO_YELLOW},
            {"step": "Search Tooling Bins, Buckets, and Infirmary for Bare Necessities (Quest 6).", "color": PRIO_PURPLE},
            {"step": "Search desks for Bullion Box and towers for Wall Cabinet (Quest 9).", "color": PRIO_BLUE},
            {"step": "Extract to Château and turn in BOTH Quest 3 & Quest 4 to unlock Quest 5!", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "pile_of_ash": {"keyword": "Pile of Ash", "shape": "wide_circle", "color": PRIO_YELLOW, "item_img": "charcoal.png", "label": "Pile of Ash (15x Charcoal - Active Q4)", "is_prio": True},
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "circle", "color": PRIO_PURPLE, "item_img": "saltpetre.png", "label": "Tooling Bin (20x Saltpetre - Focus Q6)"},
            "old_bucket": {"keyword": "Old Bucket", "shape": "circle", "color": PRIO_PURPLE, "item_img": "damp_rag.png", "label": "Old Bucket (5x Damp Rag - Focus Q6)"},
            "physician": {"keyword": "Physician", "shape": "circle", "color": PRIO_PURPLE, "item_img": "tallow_balm.png", "label": "Physician Cabinet (10x Tallow Balm - Focus Q6)"},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_BLUE, "item_img": "opium_pipe.png", "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "item_img": "china_bowl.png", "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Gavroche Camp", "item": "Camp Trigger", "i_ico": "silver_key.png", "rate": "100%", "spots": "Lower Bridge Deck perimeter"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Pile of Ash", "item": "15x Charcoal", "i_ico": "charcoal.png", "rate": "52.6%", "spots": "13 Hearths across bridge guardposts"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "24 Tooling bins on lower deck"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Old Bucket / Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.3%", "spots": "10 Wash buckets near barracks"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "3 Field medicine kits"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "28 Office desks in towers"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "3 Officer mess wall cabinets"}
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
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 5: Front Recon  &  Quest 6: Bare Necessities",
        "has_focus": True,
        "story_pois": [
            {"x": 1140, "y": 1307, "label": "Gunline Fort Tactical Map", "offset_dir": "top", "item_img": "book_rozier.png"}
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
            {"step": "Go to Gunline Fort and inspect the Tactical Map table (Quest 5).", "color": PRIO_YELLOW},
            {"step": "Find 20x Saltpetre in workshops from Tooling Bins (Quest 6).", "color": PRIO_YELLOW},
            {"step": "Find 5x Damp Rags in graveyards from Stone Graves (Quest 6).", "color": PRIO_YELLOW},
            {"step": "Find 10x Tallow Balm in Doctor's Quarters cabinets (Quest 6).", "color": PRIO_YELLOW},
            {"step": "Search bedroom desks for Bullion Box for Quest 9.", "color": PRIO_PURPLE},
            {"step": "Extract to Château and turn in Fort Recon and Bare Necessities.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "tooling_bin": {"keyword": "Tooling Bin", "shape": "wide_circle", "color": PRIO_YELLOW, "item_img": "saltpetre.png", "label": "Tooling Bin (20x Saltpetre - Active Q6)", "is_prio": True},
            "stone_grave": {"keyword": "Stone Grave", "shape": "wide_circle", "color": PRIO_YELLOW, "item_img": "damp_rag.png", "label": "Stone Grave (5x Damp Rag - Active Q6)", "is_prio": True},
            "physician": {"keyword": "Physician", "shape": "wide_circle", "color": PRIO_YELLOW, "item_img": "tallow_balm.png", "label": "Physician Cabinet (10x Tallow Balm - Active Q6)", "is_prio": True},
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_PURPLE, "item_img": "opium_pipe.png", "label": "Bullion Box (Opium Pipe - Future Q9)"},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "item_img": "china_bowl.png", "label": "Wall Cabinet (China Bowl - Future Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Gunline Fort", "item": "Tactical Map", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Western Fort Command Bunker"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Tooling Bin", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "rate": "18.9%", "spots": "13 Tooling bins in workshops"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Stone Grave", "item": "5x Damp Rag", "i_ico": "damp_rag.png", "rate": "23.8%", "spots": "40 Graves in church cemetery"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Physician's Cabinet", "item": "10x Tallow Balm", "i_ico": "tallow_balm.png", "rate": "9.1%", "spots": "Doctor's Quarters medical bags"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Bedroom desks in manors"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Kitchen wall cabinets"}
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
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 8: Sanctuary  &  Quest 9: Bribery",
        "has_focus": True,
        "story_pois": [
            {"x": 2697, "y": 807, "label": "Sarlat Chapel Altar (Candle)", "offset_dir": "bottom", "item_img": "votive_candle.png"}
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
            {"step": "Go to the Sarlat Chapel altar and recover the Red Votive Candle (Quest 8).", "color": PRIO_YELLOW},
            {"step": "Search bedroom desks across farmhouses for Bullion Boxes (Quest 9).", "color": PRIO_PURPLE},
            {"step": "Search living quarters for Wall Cabinets to find China Bowl (Quest 9).", "color": PRIO_BLUE},
            {"step": "Extract to Château and turn in Red Votive Candle to Eloise.", "color": PRIO_GREY}
        ],
        "container_priority_map": {
            "bullion_box": {"keyword": "Bullion Box", "shape": "circle", "color": PRIO_PURPLE, "item_img": "opium_pipe.png", "label": "Bullion Box (Opium Pipe - Active Q9)", "is_prio": True},
            "wall_cabinet": {"keyword": "Wall Cabinet", "shape": "circle", "color": PRIO_BLUE, "item_img": "china_bowl.png", "label": "Wall Cabinet (China Bowl - Active Q9)"}
        },
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Chapel Altar", "item": "Red Votive Candle", "i_ico": "votive_candle.png", "rate": "100%", "spots": "Guaranteed central altar spawn"},
            {"shape": "circle", "color": PRIO_PURPLE, "cont": "Bullion Box", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "spots": "22 Bedroom desks in manors"},
            {"shape": "circle", "color": PRIO_BLUE, "cont": "Wall Cabinet", "item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "spots": "4 Kitchen wall cabinets"}
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
            {"x": 2379.86, "y": 2045.2,  "label": "Book 1: Rozier (Granary Cache)", "offset_dir": "bottom", "item_img": "book_rozier.png"},
            {"x": 2085.66, "y": 887.49,  "label": "Book 2: Census 1806 (Farmhouse Desk)", "offset_dir": "top", "item_img": "book_census.png"},
            {"x": 2697.0,  "y": 807.0,   "label": "Book 3: Catéchisme (Chapel Altar)", "offset_dir": "right", "item_img": "book_catechisme.png"}
        ],
        "active_objectives": [
            {
                "title": "Book 1: Rozier (Cours Complet)",
                "npc": "Master Granary Cache (X: 2380, Y: 2045)",
                "cont_name": "Granary Cache Strongbox",
                "cont_img": "strongbox.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Climb into the upper Master Granary cache and collect Book 1: Rozier."
            },
            {
                "title": "Book 2: Census 1806",
                "npc": "Sarlat Village Desk (X: 2086, Y: 887)",
                "cont_name": "Farmhouse Ledger Desk",
                "cont_img": "ledger_desk.webp",
                "item_img": "book_census.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Search the ground floor desk in Sarlat village manor to retrieve Book 2: Census 1806."
            },
            {
                "title": "Book 3: Catéchisme",
                "npc": "Chapel Altar (X: 2697, Y: 807)",
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
            {"step": "Go to Master Granary upper cache and take Book 1: Rozier.", "color": PRIO_YELLOW},
            {"step": "Go to Sarlat Village farmhouse desk and take Book 2: Census 1806.", "color": PRIO_YELLOW},
            {"step": "Go to Chapel Altar and take Book 3: Catéchisme.", "color": PRIO_YELLOW},
            {"step": "Extract to Château with all 3 Sarlat archive books secured.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Granary Cache", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "rate": "100%", "spots": "Master Granary upper cache"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Farmhouse Desk", "item": "Book 2: Census 1806", "i_ico": "book_census.png", "rate": "100%", "spots": "Sarlat Village manor desk"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Chapel Altar", "item": "Book 3: Catéchisme", "i_ico": "book_catechisme.png", "rate": "100%", "spots": "Sarlat Chapel central altar"}
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
                "npc": "North Bridge Tower (X: 1392, Y: 1536)",
                "cont_name": "North Tower Archive Chest",
                "cont_img": "strongbox.webp",
                "item_img": "book_montesquieu.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Climb into the North Bridge fortress tower and take Book 4: Montesquieu."
            },
            {
                "title": "Book 5: Buffon (Histoire Naturelle)",
                "npc": "Guardpost Storeroom (X: 2095, Y: 1346)",
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
            {"step": "Go to North Bridge Tower storeroom and take Book 4: Montesquieu.", "color": PRIO_YELLOW},
            {"step": "Go to Guardpost barracks table and take Book 5: Buffon.", "color": PRIO_YELLOW},
            {"step": "Extract to Château with both Bridge archive books secured.", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Bridge Tower", "item": "Book 4: Montesquieu", "i_ico": "book_montesquieu.png", "rate": "100%", "spots": "North Bridge Tower storeroom"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Guardpost Desk", "item": "Book 5: Buffon", "i_ico": "book_buffon.png", "rate": "100%", "spots": "Guardpost storeroom barracks"}
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
        "quest_name": "Quest 10: Down From Mount Sinai Finale",
        "has_focus": False,
        "story_pois": [
            {"x": 3168.6, "y": 2405.75, "label": "Book 6: Rondelet (Ruins Shrine)", "offset_dir": "left", "item_img": "book_rondelet.png"},
            {"x": 2592.18, "y": 2992.87, "label": "Book 7: Codex Medicamentarius (Ridge)", "offset_dir": "top", "item_img": "book_mortuary.png"}
        ],
        "active_objectives": [
            {
                "title": "Book 6: Rondelet (Histoire des Poissons)",
                "npc": "Forest Ruins Shrine (X: 3169, Y: 2406)",
                "cont_name": "Ruins Stone Altar Cache",
                "cont_img": "strongbox.webp",
                "item_img": "book_rondelet.png",
                "drop_rate": "100%",
                "density": "Guaranteed Fixed Spawn",
                "desc": "Deep in Sombre Forest, search the stone shrine in ancient ruins to recover Book 6: Rondelet."
            },
            {
                "title": "Book 7: Codex Medicamentarius",
                "npc": "Southern Ridge Shrine (X: 2592, Y: 2993)",
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
            {"step": "Go to South-Eastern Forest Ruins and take Book 6: Rondelet.", "color": PRIO_YELLOW},
            {"step": "Go to Southern Ridge Shrine and take Book 7: Codex Medicamentarius.", "color": PRIO_YELLOW},
            {"step": "Extract to Château and hand in all 7 books to Eloise to complete the storyline!", "color": PRIO_GREY}
        ],
        "container_priority_map": {},
        "directory": [
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Forest Ruins", "item": "Book 6: Rondelet", "i_ico": "book_rondelet.png", "rate": "100%", "spots": "South-Eastern Forest Ruins shrine"},
            {"shape": "wide_circle", "color": PRIO_YELLOW, "cont": "Ridge Shrine", "item": "Book 7: Codex Medicamentarius", "i_ico": "book_mortuary.png", "rate": "100%", "spots": "Southern Ridge overlooking forest"}
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

    # Clean Pill: Just "RAID X OF 7"
    tag_txt = f"RAID {cfg['id']} OF 7"
    pill_tw = int(draw.textlength(tag_txt, font=F_HEADER_TAG))
    draw.rounded_rectangle([20, 16, 20 + pill_tw + 26, 60], radius=6, fill=(35, 45, 65), outline=PRIO_YELLOW, width=1)
    draw.text((33, 26), tag_txt, fill=PRIO_YELLOW, font=F_HEADER_TAG)

    # Title: MAP NAME - QUEST NAME
    title_x = 20 + pill_tw + 45
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

    # 2a. PLOT DB FILTERED POINTS (WITH EMBEDDED ITEM ICON)
    db_points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    for pt in db_points:
        mx, my = to_map_coord(pt['x'], pt['y'])
        r = 13 if pt.get('is_prio') else 11
        core.draw_container_shape(draw, pt['shape'], mx, my, r, pt['color'], item_img_name=pt.get('item_img'), canvas=canvas)

    # 2b. PROMINENT STORY OBJECTIVE POI MARKERS
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'), item_img_name=poi.get('item_img'), canvas=canvas)

    # 2c. QUESTLINE PROGRESSION HUD BAR (EVENLY SPACED 7 COLUMNS)
    core.render_questline_progression_bar(draw, cfg["id"])

    # 3. RIGHT BRIEFING PANEL (GRAMMATICALLY CORRECT TITLES, NO EMPTY SPACES)
    draw.rounded_rectangle([PANEL_X, PANEL_Y, PANEL_X+PANEL_W, PANEL_Y+PANEL_H], radius=12, fill=(15, 20, 30), outline=(51, 65, 85), width=2)

    has_focus = cfg.get("has_focus", True)
    gap = 14

    if has_focus:
        # Standard Raids 1 to 4 (5 categories)
        b1_y = PANEL_Y + 14   # 96
        b1_h = 176

        b2_y = b1_y + b1_h + gap # 286
        b2_h = 134

        b3_y = b2_y + b2_h + gap # 434
        b3_h = 176

        b4_y = b3_y + b3_h + gap # 624
        b4_h = 410

        b5_y = b4_y + b4_h + gap # 1048
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 318
    else:
        # Book Quest Raids 5, 6, 7 (NO FOCUS NEEDED -> 4 expanded categories)
        b1_y = PANEL_Y + 14   # 96
        b1_h = 280            # Expanded for all book objectives!

        b2_y = b1_y           # Not used
        b2_h = 0

        b3_y = b1_y + b1_h + gap # 390
        b3_h = 176            # Priorities

        b4_y = b3_y + b3_h + gap # 580
        b4_h = 280            # Drops (3 books)

        b5_y = b4_y + b4_h + gap # 874
        b5_h = (PANEL_Y + PANEL_H - 14) - b5_y # 492 (Expansive Quests roadmap)

    # ==========================================
    # CATEGORY 1: Objectives (Grammatically correct plural)
    # ==========================================
    draw.text((PANEL_X+18, b1_y), "Objectives", fill=PRIO_YELLOW, font=F_SECTION_TITLE)

    objs = cfg.get("active_objectives", [])
    if len(objs) == 1:
        o = objs[0]
        card_y = b1_y + 30
        card_h = b1_h - 30
        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=(28, 26, 16), outline=PRIO_YELLOW, width=2)

        c_img = core.CONTAINER_IMGS.get(o["cont_img"])
        core.paste_icon_safe(canvas, c_img, (PANEL_X+28, card_y+16, 76, 76), bg_color=(16, 16, 10), border_color=PRIO_YELLOW, border_w=2)
        i_img = core.ITEM_IMGS.get(o["item_img"])
        core.paste_icon_safe(canvas, i_img, (PANEL_X+88, card_y+46, 46, 46), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)

        tx = PANEL_X + 148
        max_tw = PANEL_W - 170
        draw.text((tx, card_y+14), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
        
        rate_density = f"Drop Rate: {o['drop_rate']}   -   {o['density']}"
        draw.text((tx, card_y+42), core.fit_text(draw, rate_density, F_BODY_BOLD, max_tw), fill=(240, 245, 255), font=F_BODY_BOLD)
        draw.text((tx, card_y+70), core.fit_text(draw, o["desc"], F_BODY, max_tw), fill=(210, 225, 245), font=F_BODY)
        draw.text((tx, card_y+98), core.fit_text(draw, o["npc"], F_BODY_BOLD, max_tw), fill=(34, 197, 94), font=F_BODY_BOLD)
    elif len(objs) == 2:
        card_y = b1_y + 30
        each_h = int((b1_h - 30 - 8) / 2)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=(28, 26, 16), outline=PRIO_YELLOW, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+26, card_y+8, 52, 52), bg_color=(16, 16, 10), border_color=PRIO_YELLOW, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+68, card_y+24, 34, 34), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)

            tx = PANEL_X + 114
            max_tw = PANEL_W - 140
            draw.text((tx, card_y+8), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
            line2 = f"Drop: {o['drop_rate']}  |  {o['density']}"
            draw.text((tx, card_y+34), core.fit_text(draw, line2, F_BODY, max_tw), fill=(240, 245, 255), font=F_BODY)
            card_y += each_h + 8
    else:
        # 3 Book Objectives (Raid 5)
        card_y = b1_y + 30
        each_h = int((b1_h - 30 - 16) / 3)
        for o in objs:
            draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+each_h], radius=6, fill=(28, 26, 16), outline=PRIO_YELLOW, width=2)
            c_img = core.CONTAINER_IMGS.get(o["cont_img"])
            core.paste_icon_safe(canvas, c_img, (PANEL_X+24, card_y+8, 52, 52), bg_color=(16, 16, 10), border_color=PRIO_YELLOW, border_w=2)
            i_img = core.ITEM_IMGS.get(o["item_img"])
            core.paste_icon_safe(canvas, i_img, (PANEL_X+66, card_y+22, 34, 34), bg_color=(16, 16, 10), border_color=(70, 85, 105), border_w=1)

            tx = PANEL_X + 112
            max_tw = PANEL_W - 135
            draw.text((tx, card_y+8), core.fit_text(draw, o["title"], F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
            draw.text((tx, card_y+34), core.fit_text(draw, f"Spawn: {o['npc']}", F_BODY, max_tw), fill=(74, 222, 128), font=F_BODY)
            card_y += each_h + 8

    # ==========================================
    # CATEGORY 2: Focus (Omitted in Book Raids)
    # ==========================================
    if has_focus:
        pf = cfg.get("priority_focus", {})
        pf_color = pf.get("color", PRIO_PURPLE)
        draw.text((PANEL_X+18, b2_y), "Focus", fill=pf_color, font=F_SECTION_TITLE)

        card_y = b2_y + 28
        card_h = b2_h - 28

        draw.rounded_rectangle([PANEL_X+18, card_y, PANEL_X+PANEL_W-18, card_y+card_h], radius=8, fill=(24, 18, 34), outline=pf_color, width=2)

        c_img = core.CONTAINER_IMGS.get(pf.get("c_ico"))
        core.paste_icon_safe(canvas, c_img, (PANEL_X+26, card_y+10, 60, 60), bg_color=(18, 12, 26), border_color=pf_color, border_w=2)
        i_img = core.ITEM_IMGS.get(pf.get("i_ico"))
        core.paste_icon_safe(canvas, i_img, (PANEL_X+72, card_y+32, 38, 38), bg_color=(22, 14, 32), border_color=(70, 85, 105), border_w=1)

        tx = PANEL_X + 122
        max_tw = PANEL_W - 145
        draw.text((tx, card_y+8), core.fit_text(draw, f"{pf.get('title', '')}: {pf.get('item')}", F_CARD_TITLE, max_tw), fill=(255, 255, 255), font=F_CARD_TITLE)
        draw.text((tx, card_y+36), core.fit_text(draw, f"Source: {pf.get('cont')}  -  Drop Rate: {pf.get('rate')}", F_BODY_BOLD, max_tw), fill=(240, 245, 255), font=F_BODY_BOLD)
        draw.text((tx, card_y+62), core.fit_text(draw, pf.get("desc", ""), F_BODY, max_tw), fill=(210, 220, 240), font=F_BODY)

    # ==========================================
    # CATEGORY 3: Priorities (Task Number in Circle of the SAME Priority Color)
    # ==========================================
    draw.text((PANEL_X+18, b3_y), "Priorities", fill=PRIO_YELLOW, font=F_SECTION_TITLE)
    draw.rounded_rectangle([PANEL_X+18, b3_y+28, PANEL_X+PANEL_W-18, b3_y+b3_h], radius=8, fill=(16, 21, 32), outline=(45, 58, 80), width=1)

    step_y = b3_y + 34
    for i, s_obj in enumerate(cfg["rotation_steps"], 1):
        step_text = s_obj["step"]
        prio_color = s_obj["color"]

        # Number circle matching the exact priority color!
        num_cx = PANEL_X + 38
        num_cy = step_y + 11
        draw.ellipse([num_cx-11, num_cy-11, num_cx+11, num_cy+11], fill=prio_color, outline=(10, 14, 20), width=1)
        # High contrast digit
        num_fg = (10, 14, 20) if prio_color in (PRIO_YELLOW, PRIO_GREEN) else (255, 255, 255)
        num_tw = draw.textlength(str(i), font=F_SMALL_BOLD)
        draw.text((num_cx - num_tw/2, num_cy - 7), str(i), fill=num_fg, font=F_SMALL_BOLD)

        draw.text((PANEL_X+58, step_y+2), core.fit_text(draw, step_text, F_BODY, PANEL_W - 88), fill=(240, 245, 255), font=F_BODY)
        step_y += 26

    # ==========================================
    # CATEGORY 4: Drops (Color & Outline Marker with Item Image Inside, Small Drop Rate & Spots Underneath)
    # ==========================================
    draw.rounded_rectangle([PANEL_X+18, b4_y, PANEL_X+PANEL_W-18, b4_y+b4_h], radius=10, fill=(12, 16, 26), outline=(70, 85, 110), width=2)
    draw.text((PANEL_X+32, b4_y+10), "Drops", fill=PRIO_YELLOW, font=F_CARD_TITLE)

    # Legend Bar: Priority 1, Priority 2, Priority 3, Priority 4
    sb_y = b4_y + 36
    draw.rounded_rectangle([PANEL_X+28, sb_y, PANEL_X+PANEL_W-28, sb_y+26], radius=5, fill=(18, 24, 38), outline=(50, 65, 88), width=1)

    draw.ellipse([PANEL_X+42-7, sb_y+13-7, PANEL_X+42+7, sb_y+13+7], outline=PRIO_YELLOW, width=2)
    draw.ellipse([PANEL_X+42-3, sb_y+13-3, PANEL_X+42+3, sb_y+13+3], fill=PRIO_YELLOW)
    draw.text((PANEL_X+55, sb_y+6), "Priority 1", fill=PRIO_YELLOW, font=F_TINY)

    draw.ellipse([PANEL_X+190, sb_y+8, PANEL_X+200, sb_y+18], fill=PRIO_PURPLE)
    draw.text((PANEL_X+206, sb_y+6), "Priority 2", fill=PRIO_PURPLE, font=F_TINY)

    draw.ellipse([PANEL_X+330, sb_y+8, PANEL_X+340, sb_y+18], fill=PRIO_BLUE)
    draw.text((PANEL_X+346, sb_y+6), "Priority 3", fill=PRIO_BLUE, font=F_TINY)

    draw.ellipse([PANEL_X+470, sb_y+8, PANEL_X+480, sb_y+18], fill=PRIO_GREEN)
    draw.text((PANEL_X+486, sb_y+6), "Priority 4", fill=PRIO_GREEN, font=F_TINY)

    # Render Directory Rows:
    # Marker badge with color + outline + small item icon inside
    # Line 1: Container -> Item (clean, no quest info)
    # Line 2: Small text: Drop rate and spots directly underneath!
    dir_y = sb_y + 34
    dir_items = cfg.get("directory", [])
    row_count = len(dir_items)
    
    # Calculate row height to perfectly fit available space
    avail_rows_h = b4_h - 70
    row_h = min(62, int(avail_rows_h / max(1, row_count)))

    for itm in dir_items:
        # Left Badge: Shape with priority color, outline, and small item thumbnail!
        badge_cx = PANEL_X + 46
        badge_cy = dir_y + int(row_h / 2)
        core.draw_container_shape(draw, itm['shape'], badge_cx, badge_cy, 12, itm['color'], item_img_name=itm.get('i_ico'), canvas=canvas)

        # Line 1: Container -> Item (Bold, clear)
        label_text = f"{itm['cont']}  ->  {itm['item']}"
        draw.text((PANEL_X+72, dir_y+4), core.fit_text(draw, label_text, F_CARD_TITLE, PANEL_W - 110), fill=(255, 255, 255), font=F_CARD_TITLE)

        # Line 2: Drop rate and spot number directly underneath as small text!
        spots_str = itm.get('spots', '')
        rate_str = itm.get('rate', '')
        sub_info = f"Drop Rate: {rate_str}   •   {spots_str}" if spots_str else f"Drop Rate: {rate_str}"
        draw.text((PANEL_X+72, dir_y+26), core.fit_text(draw, sub_info, F_SMALL, PANEL_W - 110), fill=(160, 180, 205), font=F_SMALL)

        dir_y += row_h

    # ==========================================
    # CATEGORY 5: Quests (Never Clips Horizontally, Grammatically Correct)
    # ==========================================
    draw.text((PANEL_X+18, b5_y), "Quests", fill=(255, 255, 255), font=F_SECTION_TITLE)

    r_y = b5_y + 30
    roadmap_list = cfg.get("roadmap", [])
    card_h = 44 if len(roadmap_list) >= 4 else 52

    for r_card in roadmap_list:
        draw.rounded_rectangle([PANEL_X+18, r_y, PANEL_X+PANEL_W-18, r_y+card_h], radius=6, fill=(20, 26, 38), outline=(51, 65, 85), width=1)
        
        # Left: Quest Title
        draw.text((PANEL_X+26, r_y+int((card_h-18)/2)), core.fit_text(draw, r_card["quest"], F_BODY_BOLD, 210), fill=PRIO_YELLOW, font=F_BODY_BOLD)

        # Right: Items laid out as compact pills
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
    print("Generating all 7 perfect V20 briefings...")
    for raid in RAIDS_CONFIG:
        render_briefing(raid)
    print("All 7 briefings generated successfully!")
