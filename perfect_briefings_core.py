import os, math, sqlite3
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
CANVAS_W = 2400
CANVAS_H = 1400

MAP_X = 30
MAP_Y = 100
MAP_W = 1320
MAP_H = 1270

PANEL_X = 1380
PANEL_Y = 100
PANEL_W = 990
PANEL_H = 1270

BASE_DIR = r"C:\Users\PC\Documents\HungerHelper"
ARTIFACT_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
ITEM_DIR = os.path.join(BASE_DIR, "assets", "items")
CONTAINER_DIR = os.path.join(BASE_DIR, "assets", "containers")

conn = sqlite3.connect(os.path.join(BASE_DIR, "hunger_helper.db"))
cur = conn.cursor()

def get_font(size, bold=False):
    names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for n in names:
        p = os.path.join(r"C:\Windows\Fonts", n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

F_HEADER_TITLE = get_font(34, bold=True)
F_HEADER_TAG = get_font(20, bold=True)
F_CARD_TITLE = get_font(24, bold=True)
F_SECTION_TITLE = get_font(21, bold=True)
F_BODY = get_font(18, bold=False)
F_BODY_BOLD = get_font(18, bold=True)
F_SMALL = get_font(15, bold=False)
F_SMALL_BOLD = get_font(15, bold=True)
F_TINY = get_font(13, bold=False)
F_MAP_LABEL = get_font(15, bold=True)
F_PIN_NUM = get_font(15, bold=True)

# Dungeon exclusion zones (remove all containers requiring dungeon keys)
DUNGEON_ZONES = {
    'Sarlat Farm': [(3444, 3473, 200)],     # The Undercroft
    'Jacques Bridge': [(962, 2658, 250)],    # Fort Sang Rouge Dungeon
    'Sombre Forest': [(2655, 1990, 220)]    # The Pit
}

def is_in_dungeon(map_name, x, y):
    zones = DUNGEON_ZONES.get(map_name, [])
    for dx, dy, radius in zones:
        dist = math.hypot(x - dx, y - dy)
        if dist <= radius:
            return True
    return False

# Fetch open-world loot coordinates (filtering out dungeons)
def get_map_loot(map_name):
    cur.execute("SELECT id, title, x, y FROM map_points WHERE map_name = ?", (map_name,))
    rows = cur.fetchall()
    
    loot = {
        'bullion': [],      # Opium Pipe (13.7%) - Bright Electric Yellow (Large)
        'wall_cabinet': [], # China Bowl (16.1%) - Bright Electric Magenta (Large)
        'tooling_bin': [],  # Saltpetre (18.9%) - Bright Electric Lime (Medium)
        'stone_grave': [],  # Damp Rag (23.8%) - Bright Electric Cyan (Medium)
        'ash_pile': [],     # Charcoal (52.6%) - Bright Neon Orange (Small)
        'flour_sack': [],   # Flour (47.6%) - Pure White (Small)
    }
    
    seen = set()
    for pid, title, x, y in rows:
        # Exclude dungeon-locked loot
        if is_in_dungeon(map_name, x, y):
            continue
            
        t = title.lower()
        ck = (round(x, 1), round(y, 1))
        
        # Explicitly skip Jacque's Medicinals since it is inside Fort Sang Rouge dungeon
        if 'jacque' in t and 'medicinal' in t:
            continue
        elif 'bullion' in t or 'jeweller' in t:
            if ck not in seen:
                loot['bullion'].append((x, y, title)); seen.add(ck)
        elif 'wall cabinet' in t:
            if ck not in seen:
                loot['wall_cabinet'].append((x, y, title)); seen.add(ck)
        elif 'tooling bin' in t:
            if ck not in seen:
                loot['tooling_bin'].append((x, y, title)); seen.add(ck)
        elif 'stone grave' in t:
            if ck not in seen:
                loot['stone_grave'].append((x, y, title)); seen.add(ck)
        elif 'pile of ash' in t:
            if ck not in seen:
                loot['ash_pile'].append((x, y, title)); seen.add(ck)
        elif 'flour sack' in t:
            if ck not in seen:
                loot['flour_sack'].append((x, y, title)); seen.add(ck)
                
    return loot

def draw_round_rect(draw, bbox, fill, outline=None, width=1, radius=8):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def paste_icon_safe(canvas, img_path, box, bg_color=None):
    if not os.path.exists(img_path):
        return
    try:
        icon = Image.open(img_path).convert("RGBA")
        x, y, w, h = box
        icon = icon.resize((w, h), Image.Resampling.LANCZOS)
        if bg_color:
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([x-2, y-2, x+w+2, y+h+2], radius=6, fill=bg_color, outline=(70, 85, 110), width=1)
        canvas.paste(icon, (x, y), icon)
    except Exception as e:
        print(f"Error pasting icon {img_path}: {e}")

# Draw an arrow pointing from (x1, y1) to (x2, y2)
def draw_arrow(draw, x1, y1, x2, y2, color=(255, 255, 255), width=2):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrow head at (x2, y2)
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 10
    head_angle = math.pi / 6
    p1 = (x2 - head_len * math.cos(angle - head_angle), y2 - head_len * math.sin(angle - head_angle))
    p2 = (x2 - head_len * math.cos(angle + head_angle), y2 - head_len * math.sin(angle + head_angle))
    draw.polygon([(x2, y2), p1, p2], fill=color)

# Render map terrain with high-visibility colors and unblocked indicators
def render_terrain_map(draw, canvas, map_img_path, map_name, objectives, show_all_loot=True):
    raw_map = Image.open(map_img_path).convert("RGB")
    map_resized = raw_map.resize((MAP_W, MAP_H), Image.Resampling.LANCZOS)
    canvas.paste(map_resized, (MAP_X, MAP_Y))
    
    # Outer border
    draw.rectangle([MAP_X-2, MAP_Y-2, MAP_X+MAP_W+2, MAP_Y+MAP_H+2], outline=(90, 110, 140), width=3)
    
    loot_points = get_map_loot(map_name) if show_all_loot else {}
    
    def to_map_coord(x, y):
        mx = MAP_X + int((x / 4096.0) * MAP_W)
        my = MAP_Y + int((y / 4096.0) * MAP_H)
        return mx, my

    # 1. COMMON ITEMS: Small indicators with black high-contrast borders
    # Flour Sacks (Small Pure White)
    for x, y, _ in loot_points.get('flour_sack', []):
        mx, my = to_map_coord(x, y)
        r = 4
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
    # Piles of Ash (Small Neon Orange)
    for x, y, _ in loot_points.get('ash_pile', []):
        mx, my = to_map_coord(x, y)
        r = 5
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=(255, 102, 0), outline=(0, 0, 0), width=1)

    # 2. MEDIUM ITEMS: Medium square indicators with black borders
    # Stone Graves - Damp Rag 23.8% (Medium Electric Cyan)
    for x, y, _ in loot_points.get('stone_grave', []):
        mx, my = to_map_coord(x, y)
        r = 6
        draw.rectangle([mx-r, my-r, mx+r, my+r], fill=(0, 229, 255), outline=(0, 0, 0), width=2)

    # Tooling Bins - Saltpetre 18.9% (Medium Electric Lime)
    for x, y, _ in loot_points.get('tooling_bin', []):
        mx, my = to_map_coord(x, y)
        r = 6
        draw.rectangle([mx-r, my-r, mx+r, my+r], fill=(57, 255, 20), outline=(0, 0, 0), width=2)

    # 3. HARD TO FIND ITEMS: Large glowing indicators with black borders
    # Bullion Boxes & Jewellery Boxes - Opium Pipe 13.7% (Large Bright Electric Yellow)
    for x, y, _ in loot_points.get('bullion', []):
        mx, my = to_map_coord(x, y)
        r = 10
        # Outer glow
        draw.ellipse([mx-r-3, my-r-3, mx+r+3, my+r+3], fill=(255, 230, 0, 100))
        # Solid core with solid black outline
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=(255, 230, 0), outline=(0, 0, 0), width=2)
        # Inner white eye
        draw.ellipse([mx-3, my-3, mx+3, my+3], fill=(255, 255, 255))

    # Wall Cabinets - China Bowl 16.1% (Large Bright Electric Magenta Diamond)
    for x, y, _ in loot_points.get('wall_cabinet', []):
        mx, my = to_map_coord(x, y)
        r = 11
        # Glow diamond
        diamond_glow = [(mx, my-r-3), (mx+r+3, my), (mx, my+r+3), (mx-r-3, my)]
        draw.polygon(diamond_glow, fill=(255, 0, 127, 100))
        # Solid diamond with black outline
        diamond_core = [(mx, my-r), (mx+r, my), (mx, my+r), (mx-r, my)]
        draw.polygon(diamond_core, fill=(255, 0, 127), outline=(0, 0, 0), width=2)
        draw.ellipse([mx-3, my-3, mx+3, my+3], fill=(255, 255, 255))

    # 4. MAIN RAID OBJECTIVES: Pins with offset labels & arrows (DO NOT COVER INDICATORS)
    for idx, obj in enumerate(objectives):
        ox, oy = to_map_coord(obj['x'], obj['y'])
        col = obj.get('color', (255, 50, 50))
        
        # Draw pulsing pinpoint on terrain
        draw.ellipse([ox-14, oy-14, ox+14, oy+14], fill=(*col, 80))
        draw.ellipse([ox-10, oy-10, ox+10, oy+10], fill=col, outline=(0, 0, 0), width=2)
        draw.text((ox-5, oy-8), str(idx+1), fill=(255, 255, 255), font=F_PIN_NUM)
        
        # Calculate offset label box position (place outside crowded area)
        label = obj['name']
        sub = obj.get('sub', '')
        t_w = max(int(draw.textlength(label, font=F_MAP_LABEL)), int(draw.textlength(sub, font=F_TINY)))
        box_w = t_w + 24
        box_h = 42 if sub else 28
        
        # Custom label offset if provided, else intelligent offset away from center
        if 'label_x' in obj and 'label_y' in obj:
            bx, by = obj['label_x'], obj['label_y']
        else:
            offset_x = 90 if ox < MAP_X + MAP_W / 2 else -box_w - 90
            offset_y = -50 if oy > MAP_Y + 120 else 50
            bx = min(max(ox + offset_x, MAP_X + 15), MAP_X + MAP_W - box_w - 15)
            by = min(max(oy + offset_y, MAP_Y + 15), MAP_Y + MAP_H - box_h - 15)
            
        # Draw label box
        draw.rounded_rectangle([bx, by, bx+box_w, by+box_h], radius=6, fill=(10, 14, 22, 240), outline=col, width=2)
        draw.text((bx+12, by+4), label, fill=(255, 255, 255), font=F_MAP_LABEL)
        if sub:
            draw.text((bx+12, by+23), sub, fill=(203, 213, 225), font=F_TINY)
            
        # Draw clear connecting arrow from label edge to pin center (ox, oy)
        target_edge_x = bx if ox < bx else (bx + box_w if ox > bx + box_w else ox)
        target_edge_y = by if oy < by else (by + box_h if oy > by + box_h else oy)
        draw_arrow(draw, target_edge_x, target_edge_y, ox, oy, color=col, width=2)

    # 5. HIGH-CONTRAST MAP LEGEND (Top-Left Corner)
    lx = MAP_X + 16
    ly = MAP_Y + 16
    lw = 450
    lh = 205 if show_all_loot else 95
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(5, 9, 16, 245), outline=(90, 110, 140), width=2)
    
    draw.text((lx+14, ly+10), "MAP CONTAINER & OBJECTIVE KEY", fill=(255, 230, 0), font=F_SMALL_BOLD)
    
    if show_all_loot:
        items_legend = [
            ("★", (255, 230, 0), "Bullion / Jewellery Box", "Opium Pipe 13.7% · Hard to find"),
            ("◆", (255, 0, 127), "Wall Cabinet", "China Bowl 16.1% · Hard to find"),
            ("■", (57, 255, 20), "Tooling Bin", "Saltpetre 18.9% (Q6) · High density"),
            ("■", (0, 229, 255), "Stone Grave", "Damp Rag 23.8% (Q6) · High density"),
            ("●", (255, 102, 0), "Pile of Ash", "Charcoal 52.6% (Q4) · Common"),
            ("●", (255, 255, 255), "Flour Sack / Oak Barrel", "Flour 47.6% (Q2) · Common"),
        ]
        curr_y = ly + 36
        for sym, col, title, desc in items_legend:
            draw.text((lx+14, curr_y), sym, fill=col, font=F_SMALL_BOLD)
            draw.text((lx+32, curr_y), title, fill=(255, 255, 255), font=F_SMALL_BOLD)
            draw.text((lx+220, curr_y+1), desc, fill=(148, 163, 184), font=F_TINY)
            curr_y += 27
    else:
        draw.text((lx+14, ly+40), "Targeting specific quest items for this match.", fill=(203, 213, 225), font=F_SMALL)

print("Updated perfect_briefings_core ready.")
