import os, sys, io, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v13 as core

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
        "tactical_vector": [(650, 1500), (1259, 1065), (1850, 2100), (2368, 1475), (3400, 2100)],
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
            "title": "⭐ CHECK EVERY RAID (MR SWEET'S CONTRABAND)",
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
            "Head East and extract via designated gate to Château."
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
        "tactical_vector": [(1050, 3000), (1500, 2100), (1479, 313), (1400, 150)],
        "story_pois": [
            {"x": 1479, "y": 313, "label": "Gavroche Family Camp", "offset_dir": "bottom"}
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
            "title": "⭐ CHECK EVERY RAID (MR SWEET'S CONTRABAND)",
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
            "Navigate North and extract safely via open bridge gate."
        ],
        "roadmap": [
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]},
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 3: Sarlat Farm (Last Embers - Charcoal)
    {
        "id": 3,
        "phase": "RAID 3 OF 7  —  HEARTH & RESOURCE FORAGING",
        "map_name": "Sarlat Farm",
        "map_img": SARLAT_MAP,
        "quest_name": "Quest 4: Last Embers (Charcoal)",
        "grouped_turnin_label": "ACTIVE: Q4 LAST EMBERS (15x CHARCOAL)",
        "tactical_vector": [(950, 750), (1259, 1065), (1850, 2100), (2100, 2600), (3500, 2700)],
        "story_pois": [],
        "active_objectives": [
            {
                "title": "Quest 4: Gather 15x Charcoal",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Pile of Ash / Fireplace Hearths",
                "cont_img": "pile_of_ash.webp",
                "item_img": "charcoal.png",
                "drop_rate": "52.6%",
                "density": "14 ash piles in village & farmhouse hearths",
                "desc": "Check every stove, hearth, and burned fireplace in houses for 15x Charcoal."
            }
        ],
        "contraband_sweep": {
            "title": "⭐ CHECK EVERY RAID (MR SWEET'S CONTRABAND)",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Desks & Nightstands (40 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Living Quarters Walls (4 spots)"}
        },
        "directory": [
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "15x Charcoal", "i_ico": "charcoal.png", "loc": "HEARTHS: Living Quarters Stoves & Hearths — 14 Spots", "rate": "52.6%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "CENTER: Farmhouse Bedroom Desks — 22 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "WALLS: Farmhouse & Church Walls — 4 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "SOUTH-EAST: Military Battery Workshops — 13 Spots", "rate": "18.9%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "Surplus Flour", "i_ico": "flour.png", "loc": "WEST MAP: Master Granary — 18 Spots", "rate": "47.6%"}
        ],
        "steps": [
            "Check stoves and hearths across central farmhouses for Piles of Ash (Orange ◎).",
            "Secure 15x Charcoal (52.6% drop rate) in backpack.",
            "Sweep bedroom Bullion Boxes (Purple ◆) and Wall Cabinets (Blue ■) for Contraband.",
            "Rotate along South-East path to River Road extraction gate."
        ],
        "roadmap": [
            {"quest": "Quest 6: Medical Necessities", "items": [("20x Saltpetre", "saltpetre.png"), ("5x Damp Rag", "damp_rag.png"), ("10x Tallow Balm", "tallow_balm.png")]},
            {"quest": "Quest 8: Shadows Sanctuary", "items": [("1x Red Votive Candle", "votive_candle.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 4: Jacques Bridge (Red Votive Candle & Contraband Finale)
    {
        "id": 4,
        "phase": "RAID 4 OF 7  —  SANCTUARY RAID & CONTRABAND FINALE",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "quest_name": "Quest 8: Red Candle  &  Bribery Turn-In",
        "grouped_turnin_label": "GROUPED: Q8 CANDLE + MR SWEET BRIBERY",
        "tactical_vector": [(1700, 600), (2100, 1800), (3048, 2488), (3650, 2200)],
        "story_pois": [
            {"x": 3048, "y": 2488, "label": "Chapel Of Weeping Virgins Altar", "offset_dir": "top"}
        ],
        "active_objectives": [
            {
                "title": "Quest 8: 1x Red Votive Candle",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Chapel Of Weeping Virgins (Altar)",
                "cont_img": "master_chest.webp",
                "item_img": "votive_candle.png",
                "drop_rate": "100%",
                "density": "Guaranteed spawn on Chapel Altar (X: 3048, Y: 2488)",
                "desc": "Cross to Chapel of Weeping Virgins and grab the Red Candle from the stone altar."
            },
            {
                "title": "Bribery Finale: 1x Opium Pipe & 1x China Bowl",
                "npc": "Turn in to: Mr Sweet (Artificer) at Ramparts Hub",
                "cont_name": "Bullion Box / Wall Cabinet",
                "cont_img": "bullion_box.webp",
                "item_img": "opium_pipe.png",
                "drop_rate": "13.7% / 16.1%",
                "density": "Finalize collection before Mount Sinai",
                "desc": "Turn in Opium Pipe & China Bowl to Mr Sweet to acquire the Sinai Map!"
            }
        ],
        "contraband_sweep": {
            "title": "⭐ CONTRABAND FINALE (TURNS IN TO MR SWEET)",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Guardhouse Desks on Bridge Road (28 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Tollhouse & Tower Walls (3 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Chapel Altar", "c_ico": "master_chest.webp", "item": "Red Votive Candle", "i_ico": "votive_candle.png", "loc": "SOUTH-EAST: Chapel of Weeping Virgins Altar (X: 3048, Y: 2488)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe ⭐", "i_ico": "opium_pipe.png", "loc": "ROAD DESKS: Fortress Guardhouse Desks — 28 Spots", "rate": "13.7%"},
            {"shape": "square", "color": COLOR_CABINET, "cont": "Wall Cabinet", "c_ico": "wall_cabinet.webp", "item": "China Bowl ⭐", "i_ico": "china_bowl.png", "loc": "TOLLHOUSES: Tower Living Quarters Walls — 3 Spots", "rate": "16.1%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "20x Saltpetre", "i_ico": "saltpetre.png", "loc": "WORKSHOPS: Fortress Battery Corners — 24 Spots", "rate": "18.9%"},
            {"shape": "circle", "color": COLOR_SACK, "cont": "Flour Sack", "c_ico": "flour_sack.webp", "item": "Flour / Rations", "i_ico": "flour.png", "loc": "NORTH TOWERS: Bridge Storerooms & Sacks — 12 Spots", "rate": "47.6%"}
        ],
        "steps": [
            "Spawn on North Bridge approach and advance south along the bridge road.",
            "Sweep tollhouse Bullion Boxes (Purple ◆) and Wall Cabinets (Blue ■) for Contraband.",
            "Infiltrate Chapel of Weeping Virgins (X: 3048, Y: 2488) and take the Red Votive Candle from altar.",
            "Advance East and extract via Riverbed Gate."
        ],
        "roadmap": [
            {"quest": "Quest 9: Bribery", "items": [("1x Opium Pipe", "opium_pipe.png"), ("1x China Bowl", "china_bowl.png")]},
            {"quest": "Quest 10: Mount Sinai", "items": [("7x Mount Sinai Books", "book_rozier.png")]}
        ]
    },

    # RAID 5: Sombre Forest (Down From Mount Sinai - Books 1, 2, 3)
    {
        "id": 5,
        "phase": "RAID 5 OF 7  —  EXPEDITION CLIMB (BOOKS 1, 2, 3)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Part 1)",
        "grouped_turnin_label": "ACTIVE: Q10 SOMBRE FOREST (BOOKS 1, 2, 3)",
        "tactical_vector": [(1500, 500), (1729, 729), (1817, 2280), (1968, 3349), (2100, 3800)],
        "story_pois": [
            {"x": 1729, "y": 729, "label": "Book 3: Rondelet", "offset_dir": "bottom"},
            {"x": 1817, "y": 2280, "label": "Book 2: Catéchisme", "offset_dir": "right"},
            {"x": 1968, "y": 3349, "label": "Book 1: Rozier", "offset_dir": "bottom"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10: Recover Books 1, 2, and 3",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Forest Shrines & Mountain Caches",
                "cont_img": "master_chest.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "3 Guaranteed Book Spawns",
                "desc": "Collect Rozier (1968, 3349), Catéchisme (1817, 2280), and Rondelet (1729, 729)."
            }
        ],
        "contraband_sweep": {
            "title": "⭐ OPTIONAL SOMBRE CONTRABAND SWEEP",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Hunter Lodge Desks (15 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Lumber Camp Living Walls (3 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 1: Rozier", "i_ico": "book_rozier.png", "loc": "SOUTH RIDGE: Mountain Shrine (X: 1968, Y: 3349)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 2: Catéchisme", "i_ico": "book_rozier.png", "loc": "CENTRAL GROVE: Hermit Hollow (X: 1817, Y: 2280)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 3: Rondelet", "i_ico": "book_rozier.png", "loc": "NORTH GLEN: Ruined Outlook (X: 1729, Y: 729)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "loc": "LODGES: Forester & Hunter Cabins — 15 Spots", "rate": "13.7%"},
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "Charcoal", "i_ico": "charcoal.png", "loc": "CAMPFIRES: Logging Camps & Fireplaces — 18 Spots", "rate": "52.6%"},
            {"shape": "triangle", "color": COLOR_TOOLING, "cont": "Tooling Bin", "c_ico": "tooling_bin.webp", "item": "Saltpetre", "i_ico": "saltpetre.png", "loc": "SAWMILL: Timber Mill Workshops — 12 Spots", "rate": "18.9%"}
        ],
        "steps": [
            "Spawn on North Timber Ridge and navigate south toward North Glen for Book 3 (Rondelet).",
            "Move south through Central Grove to recover Book 2 (Catéchisme).",
            "Climb South Ridge to recover Book 1 (Rozier) from the Mountain Shrine.",
            "Head South and extract safely via South Gully Gate."
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Part 2)", "items": [("Book 4: Montesquieu", "book_rozier.png"), ("Book 5: Buffon", "book_rozier.png")]},
            {"quest": "Quest 10: Mount Sinai (Finale)", "items": [("Book 6: Census", "book_rozier.png"), ("Book 7: Paracelsus", "book_rozier.png")]}
        ]
    },

    # RAID 6: Sombre Forest (Down From Mount Sinai - Books 4, 5)
    {
        "id": 6,
        "phase": "RAID 6 OF 7  —  EXPEDITION MID-RIDGE (BOOKS 4, 5)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Part 2)",
        "grouped_turnin_label": "ACTIVE: Q10 SOMBRE FOREST (BOOKS 4, 5)",
        "tactical_vector": [(1400, 600), (2094, 1346), (1391, 1535), (950, 3200)],
        "story_pois": [
            {"x": 2094, "y": 1346, "label": "Book 5: Buffon", "offset_dir": "right"},
            {"x": 1391, "y": 1535, "label": "Book 4: Montesquieu", "offset_dir": "left"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10: Recover Books 4 and 5",
                "npc": "Turn in to: Eloise at Château",
                "cont_name": "Forest Shrines & Mountain Caches",
                "cont_img": "master_chest.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "2 Guaranteed Book Spawns",
                "desc": "Collect Montesquieu (1391, 1535) and Buffon (2094, 1346)."
            }
        ],
        "contraband_sweep": {
            "title": "⭐ OPTIONAL SOMBRE CONTRABAND SWEEP",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Forester Bunkhouse (12 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "Watchpost Living Quarters (2 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 4: Montesquieu", "i_ico": "book_rozier.png", "loc": "WEST CRAG: Rocky Outcropping (X: 1391, Y: 1535)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 5: Buffon", "i_ico": "book_rozier.png", "loc": "EAST LEDGE: Cliffside Altar (X: 2094, Y: 1346)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "loc": "BUNKHOUSES: Timber Cabins — 12 Spots", "rate": "13.7%"},
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "Charcoal", "i_ico": "charcoal.png", "loc": "HEARTHS: Forester Hearths — 15 Spots", "rate": "52.6%"}
        ],
        "steps": [
            "Spawn in North Pines and proceed south-east toward East Ledge for Book 5 (Buffon).",
            "Traverse across central plateau west toward Rocky Outcropping for Book 4 (Montesquieu).",
            "Check nearby timber cabins for any needed supplies.",
            "Head South-West to West River extraction gate."
        ],
        "roadmap": [
            {"quest": "Quest 10: Mount Sinai (Finale)", "items": [("Book 6: Census", "book_rozier.png"), ("Book 7: Paracelsus", "book_rozier.png")]}
        ]
    },

    # RAID 7: Sombre Forest (Down From Mount Sinai - Books 6, 7 FINALE)
    {
        "id": 7,
        "phase": "RAID 7 OF 7  —  EXPEDITION FINALE (BOOKS 6, 7 & CROSSING)",
        "map_name": "Sombre Forest",
        "map_img": SOMBRE_MAP,
        "quest_name": "Quest 10: Down From Mount Sinai (Finale)",
        "grouped_turnin_label": "ACTIVE: Q10 FINALE (BOOKS 6, 7) + Q11 CROSSING",
        "tactical_vector": [(1200, 2100), (1888, 2244), (2755, 2314), (3600, 2100)],
        "story_pois": [
            {"x": 1888, "y": 2244, "label": "Book 6: Census", "offset_dir": "left"},
            {"x": 2755, "y": 2314, "label": "Book 7: Paracelsus", "offset_dir": "right"}
        ],
        "active_objectives": [
            {
                "title": "Quest 10 Finale: Recover Books 6 and 7",
                "npc": "Turn in to: Eloise at Château (Completes Questline!)",
                "cont_name": "Forest Shrines & Mountain Caches",
                "cont_img": "master_chest.webp",
                "item_img": "book_rozier.png",
                "drop_rate": "100%",
                "density": "2 Guaranteed Book Spawns",
                "desc": "Collect Census (1888, 2244) and Paracelsus (2755, 2314). Unlocks Quest 11: The Crossing!"
            }
        ],
        "contraband_sweep": {
            "title": "⭐ OPTIONAL SOMBRE CONTRABAND SWEEP",
            "bullion": {"item": "Opium Pipe", "i_ico": "opium_pipe.png", "rate": "13.7%", "loc": "Millhouse Desks (10 spots)"},
            "cabinet": {"item": "China Bowl", "i_ico": "china_bowl.png", "rate": "16.1%", "loc": "East Guard Cabin Walls (2 spots)"}
        },
        "directory": [
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 6: Census", "i_ico": "book_rozier.png", "loc": "CENTRAL VALLEY: Hidden Crevice (X: 1888, Y: 2244)", "rate": "100%"},
            {"shape": "star", "color": COLOR_STORY, "cont": "Forest Cache", "c_ico": "master_chest.webp", "item": "Book 7: Paracelsus", "i_ico": "book_rozier.png", "loc": "EAST SLOPE: Ancient Cairn (X: 2755, Y: 2314)", "rate": "100%"},
            {"shape": "diamond", "color": COLOR_BULLION, "cont": "Bullion Box", "c_ico": "bullion_box.webp", "item": "Opium Pipe", "i_ico": "opium_pipe.png", "loc": "MILLHOUSES: Riverbank Cabins — 10 Spots", "rate": "13.7%"},
            {"shape": "ring", "color": COLOR_ASH, "cont": "Pile of Ash", "c_ico": "pile_of_ash.webp", "item": "Charcoal", "i_ico": "charcoal.png", "loc": "FIREPLACES: Mill Hearths — 12 Spots", "rate": "52.6%"}
        ],
        "steps": [
            "Spawn in Old Mill Clearing and move east toward Central Valley for Book 6 (Census).",
            "Advance up East Slope to ancient stone cairn for Book 7 (Paracelsus).",
            "Verify all 7 Mount Sinai books are secured in inventory.",
            "Advance East and extract via East Road Gate to trigger Quest 11 Finale!"
        ],
        "roadmap": [
            {"quest": "Quest 11: The Crossing (Finale)", "items": [("Expedition Complete ✓", "book_rozier.png")]}
        ]
    }
]

def render_briefing(cfg):
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (10, 14, 22, 255))
    draw = ImageDraw.Draw(canvas)
    
    # 1. TOP HEADER (Canvas W: 2400)
    draw.rounded_rectangle([20, 16, CANVAS_W-20, 68], radius=8, fill=(16, 22, 34), outline=(51, 65, 85), width=2)
    draw.text((36, 26), "HUNGER HELPER  —  EXPEDITION FAST-TRACK RAID BRIEFING", fill=COLOR_SACK, font=F_HEADER_TITLE)
    draw.text((1050, 32), f"PHASE: {cfg['phase']}", fill=(240, 245, 255), font=F_HEADER_TAG)
    draw.text((CANVAS_W-420, 32), f"TERRAIN: {cfg['map_name'].upper()}", fill=(160, 185, 220), font=F_HEADER_TAG)

    # 2. LEFT MAP VIEWPORT (MAP_X: 20, MAP_Y: 82, MAP_W: 1630, MAP_H: 1298)
    draw.rounded_rectangle([MAP_X, MAP_Y, MAP_X+MAP_W, MAP_Y+MAP_H], radius=12, fill=(8, 12, 18), outline=(51, 65, 85), width=2)
    
    if os.path.exists(cfg["map_img"]):
        raw_map = Image.open(cfg["map_img"]).convert("RGBA")
        map_crop = raw_map.resize((MAP_W-4, MAP_H-4), Image.Resampling.LANCZOS)
        canvas.paste(map_crop, (MAP_X+2, MAP_Y+2), map_crop)
    
    # 2a. RENDER REAL DATABASE CONTAINER LOOT POINTS
    db_points = core.get_map_loot_from_db(cfg["map_name"])
    for pt in db_points:
        mx, my = to_map_coord(pt['x'], pt['y'])
        r = 7 if pt.get('is_prio') else 6
        core.draw_container_shape(draw, pt['shape'], mx, my, r, pt['color'], outline=(15, 20, 30), width=2)
        
    # 2b. SUGGESTION A: PROMINENT STORY OBJECTIVE POI MARKERS (Radiant Gold Star + Callout Pill)
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'))

    # 2c. QUESTLINE PROGRESSION HUD BAR (ON MAP TOP)
    core.render_questline_progression_bar(draw, cfg["id"], cfg.get("grouped_turnin_label"))

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
    
    # Render Directory Rows (Big 38x38 Icons, Clear Shapes)
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
    canvas.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_name} successfully ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating all 7 perfect V13 briefings (with Suggestion A & Suggestion D)...")
    for cfg in RAIDS_CONFIG:
        render_briefing(cfg)
    print("All 7 V13 briefings generated successfully!")
