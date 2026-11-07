import os, sys, io
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v6 as core

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

def get_map_loot(map_name):
    # Returns raw points for dots
    points = []
    
    # 1. Flour Sacks / Barrels on Sarlat
    if map_name == "Sarlat Farm":
        # Master Granary Cluster (X: 1200-1400, Y: 1000-1200) -> 18 points
        granary_pts = [
            (1259, 1065), (1240, 1080), (1280, 1050), (1220, 1100), (1310, 1040),
            (1265, 1120), (1295, 1090), (1235, 1060), (1275, 1140), (1250, 1030),
            (1330, 1070), (1300, 1115), (1220, 1045), (1285, 1160), (1340, 1095),
            (1210, 1085), (1270, 1015), (1315, 1135)
        ]
        for x, y in granary_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (0, 229, 255), 'is_100': True, 'type': 'Flour Sack'})
            
        # Sarlat Village Granaries (X: 2300-2450, Y: 1400-1550) -> 14 points
        village_pts = [
            (2368, 1475), (2340, 1450), (2390, 1500), (2320, 1480), (2410, 1460),
            (2355, 1520), (2385, 1430), (2330, 1510), (2420, 1490), (2370, 1410),
            (2400, 1530), (2310, 1440), (2430, 1470), (2360, 1540)
        ]
        for x, y in village_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (0, 229, 255), 'is_100': True, 'type': 'Flour Sack'})

        # Priority 2: Bullion Boxes on Sarlat (Excluding Undercroft X>3100, Y>2900)
        bullion_pts = [
            (1280, 1100), (2380, 1450), (1750, 2100), (1920, 1850), (1450, 2600),
            (2100, 2500), (2800, 2100), (1600, 1400), (2650, 1750), (950, 2200),
            (2250, 1950), (1850, 2300)
        ]
        for x, y in bullion_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (255, 234, 0), 'is_100': True, 'type': 'Bullion Box'})

        # Priority 2: Wall Cabinets (China Bowl)
        cabinet_pts = [(1245, 1075), (2350, 1460), (1880, 1820), (2750, 2080)]
        for x, y in cabinet_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (255, 234, 0), 'is_100': True, 'type': 'Wall Cabinet'})

        # Priority 3: Piles of Ash (15x Charcoal)
        ash_pts = [
            (1230, 1050), (1270, 1110), (2330, 1470), (2400, 1440), (1720, 2080),
            (1950, 1830), (1420, 2580), (2120, 2480), (2780, 2120), (1580, 1380),
            (2220, 1970), (1830, 2280), (1050, 2150), (2550, 1700), (2850, 2050)
        ]
        for x, y in ash_pts:
            points.append({'x': x, 'y': y, 'prio': 3, 'color': (16, 185, 129), 'is_100': True, 'type': 'Pile of Ash'})

    elif map_name == "Jacques Bridge":
        # Guardhouse Bullion Boxes (Center Fortress)
        bullion_pts = [
            (2050, 2020), (2075, 2040), (2030, 2060), (2090, 2010),
            (1380, 1540), (2110, 1330), (1800, 2500), (2400, 1800)
        ]
        for x, y in bullion_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (255, 234, 0), 'is_100': True, 'type': 'Bullion Box'})

        # Tooling Bins & Cabinets (Saltpetre & Damp Rags)
        tool_pts = [
            (2040, 2030), (2060, 2050), (1390, 1520), (2100, 1350),
            (1780, 2480), (2420, 1820), (1950, 2200), (2200, 1900)
        ]
        for x, y in tool_pts:
            points.append({'x': x, 'y': y, 'prio': 3, 'color': (16, 185, 129), 'is_100': True, 'type': 'Tooling Bin'})

    elif map_name == "Sombre Forest":
        # Outer Ramparts Merchant Encampment (North)
        merch_pts = [(2100, 950), (2120, 970), (2080, 960), (2140, 940)]
        for x, y in merch_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (255, 234, 0), 'is_100': True, 'type': 'Merchant'})

        # Surface Sacks & Barrels
        sack_pts = [
            (1500, 1800), (1520, 1820), (1480, 1790), (2800, 2200),
            (2820, 2230), (1900, 2500), (2200, 1600), (2500, 2900)
        ]
        for x, y in sack_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (0, 229, 255), 'is_100': True, 'type': 'Sack'})

    return points

print("Loot points engine ready.")
