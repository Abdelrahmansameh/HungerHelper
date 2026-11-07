import os, math, sqlite3
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 2400
CANVAS_H = 1400

# Map takes 70% width: 1640 x 1300
MAP_X = 20
MAP_Y = 80
MAP_W = 1640
MAP_H = 1300

# Sidebar takes 29% width: 700 x 1300
PANEL_X = 1680
PANEL_Y = 80
PANEL_W = 700
PANEL_H = 1300

BASE_DIR = r"C:\Users\PC\Documents\HungerHelper"
ARTIFACT_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
ITEM_DIR = os.path.join(BASE_DIR, "assets", "items")
CONT_DIR = os.path.join(BASE_DIR, "assets", "containers")

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

F_HEADER_TITLE = get_font(28, bold=True)
F_HEADER_TAG = get_font(17, bold=True)
F_SECTION_TITLE = get_font(16, bold=True)
F_BODY = get_font(15, bold=False)
F_BODY_BOLD = get_font(15, bold=True)
F_SMALL = get_font(13, bold=False)
F_SMALL_BOLD = get_font(13, bold=True)
F_TINY = get_font(11, bold=False)
F_MAP_LABEL = get_font(15, bold=True)
F_PIN_NUM = get_font(16, bold=True)

# Pre-cache container images for rapid compositing
CONTAINER_IMGS = {}
for fname in os.listdir(CONT_DIR):
    if fname.endswith(('.webp', '.png')):
        p = os.path.join(CONT_DIR, fname)
        try:
            CONTAINER_IMGS[fname] = Image.open(p).convert("RGBA")
        except:
            pass

# Dungeon filter
def is_in_dungeon(map_name, x, y):
    if map_name == 'Sarlat Farm':
        # Subterranean Undercroft complex
        if x > 3100 and y > 2900:
            return True
    elif map_name == 'Jacques Bridge':
        # Fort Sang Rouge
        if x < 1200 and y > 2400:
            return True
    elif map_name == 'Sombre Forest':
        # The Pit
        if 2400 <= x <= 2900 and 1800 <= y <= 2200:
            return True
    return False

def get_raw_loot(map_name):
    cur.execute("SELECT id, title, x, y FROM map_points WHERE map_name = ?", (map_name,))
    rows = cur.fetchall()
    
    loot_list = []
    seen = set()
    for pid, title, x, y in rows:
        if is_in_dungeon(map_name, x, y):
            continue
            
        t = title.lower()
        ck = (round(x, 1), round(y, 1))
        
        if 'jacque' in t and 'medicinal' in t:
            continue
            
        item_info = None
        if 'bullion' in t or 'jeweller' in t:
            if ck not in seen:
                # Priority 2: Hardest drop (13.7%) -> Gold accent, chance spawn
                item_info = {
                    'name': 'Bullion / Jewellery Box', 'x': x, 'y': y,
                    'img': 'bullion_box.webp', 'prio': 2,
                    'color': (255, 234, 0), 'is_100': False, 'rate': '13.7%'
                }
                seen.add(ck)
        elif 'wall cabinet' in t:
            if ck not in seen:
                # Priority 2: Hardest drop (16.1%) -> Gold/Magenta accent, chance spawn
                item_info = {
                    'name': 'Wall Cabinet', 'x': x, 'y': y,
                    'img': 'wall_cabinet.webp', 'prio': 2,
                    'color': (255, 234, 0), 'is_100': False, 'rate': '16.1%'
                }
                seen.add(ck)
        elif 'tooling bin' in t:
            if ck not in seen:
                # Priority 3: Upcoming Q6 (18.9%) -> Emerald accent, chance spawn
                item_info = {
                    'name': 'Tooling Bin', 'x': x, 'y': y,
                    'img': 'tooling_bin.webp', 'prio': 3,
                    'color': (16, 185, 129), 'is_100': False, 'rate': '18.9%'
                }
                seen.add(ck)
        elif 'stone grave' in t:
            if ck not in seen:
                # Priority 3: Upcoming Q6 (23.8%) -> Emerald accent, chance spawn
                item_info = {
                    'name': 'Stone Grave', 'x': x, 'y': y,
                    'img': 'stone_grave.webp', 'prio': 3,
                    'color': (16, 185, 129), 'is_100': False, 'rate': '23.8%'
                }
                seen.add(ck)
        elif 'pile of ash' in t:
            if ck not in seen:
                # Priority 3: Upcoming Q4 (52.6%) -> Emerald accent, chance spawn
                item_info = {
                    'name': 'Pile of Ash', 'x': x, 'y': y,
                    'img': 'pile_of_ash.webp', 'prio': 3,
                    'color': (16, 185, 129), 'is_100': False, 'rate': '52.6%'
                }
                seen.add(ck)
        elif 'flour sack' in t:
            if ck not in seen:
                # Priority 1: Common food sack (47.6%) -> White/Cyan accent, chance spawn
                item_info = {
                    'name': 'Flour Sack', 'x': x, 'y': y,
                    'img': 'flour_sack.webp', 'prio': 1,
                    'color': (255, 255, 255), 'is_100': False, 'rate': '47.6%'
                }
                seen.add(ck)
                
        if item_info:
            loot_list.append(item_info)
            
    return loot_list

def decluster_points(points, threshold=38):
    clusters = []
    for p in points:
        placed = False
        for c in clusters:
            cx = sum(item['raw_mx'] for item in c) / len(c)
            cy = sum(item['raw_my'] for item in c) / len(c)
            if math.hypot(p['raw_mx'] - cx, p['raw_my'] - cy) < threshold:
                c.append(p)
                placed = True
                break
        if not placed:
            clusters.append([p])
            
    result = []
    for c in clusters:
        n = len(c)
        if n == 1:
            c[0]['mx'] = c[0]['raw_mx']
            c[0]['my'] = c[0]['raw_my']
            result.append(c[0])
        else:
            cx = sum(item['raw_mx'] for item in c) / n
            cy = sum(item['raw_my'] for item in c) / n
            rad = 22 if n <= 3 else (28 if n <= 5 else 34)
            for i, item in enumerate(c):
                angle = (2 * math.pi * i) / n
                item['mx'] = int(cx + rad * math.cos(angle))
                item['my'] = int(cy + rad * math.sin(angle))
                result.append(item)
    return result

def draw_arrow(draw, x1, y1, x2, y2, color=(255, 255, 255), width=3):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 14
    head_angle = math.pi / 6
    p1 = (x2 - head_len * math.cos(angle - head_angle), y2 - head_len * math.sin(angle - head_angle))
    p2 = (x2 - head_len * math.cos(angle + head_angle), y2 - head_len * math.sin(angle + head_angle))
    draw.polygon([(x2, y2), p1, p2], fill=color)

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

# Render the terrain map with container images and spawn rate borders
def render_terrain_map(draw, canvas, map_img_path, map_name, objectives, show_all_loot=True):
    raw_map = Image.open(map_img_path).convert("RGB")
    map_resized = raw_map.resize((MAP_W, MAP_H), Image.Resampling.LANCZOS)
    canvas.paste(map_resized, (MAP_X, MAP_Y))
    
    draw.rectangle([MAP_X-2, MAP_Y-2, MAP_X+MAP_W+2, MAP_Y+MAP_H+2], outline=(90, 110, 140), width=3)
    
    def to_map_coord(x, y):
        mx = MAP_X + int((x / 4096.0) * MAP_W)
        my = MAP_Y + int((y / 4096.0) * MAP_H)
        return mx, my

    # 1. Fetch & De-cluster Points
    raw_points = get_raw_loot(map_name) if show_all_loot else []
    for p in raw_points:
        p['raw_mx'], p['raw_my'] = to_map_coord(p['x'], p['y'])
        
    declustered = decluster_points(raw_points, threshold=38)

    # 2. Draw Containers (Actual Images + Spawn Rate Borders)
    # Sort so Priority 2 (Hardest) and 100% are drawn on top
    declustered.sort(key=lambda p: (p['prio'] == 2, p['is_100']))
    
    for p in declustered:
        mx, my = p['mx'], p['my']
        is_prio2 = (p['prio'] == 2)
        
        # Badge size: 34x34 for Priority 2 (Hardest), 28x28 for others
        bw = 34 if is_prio2 else 28
        half = bw // 2
        bx, by = mx - half, my - half
        
        # Spawn rate border visual rule:
        # 100% = Solid bright vibrant color
        # < 100% = Grey / silver metallic border with color accent
        if p['is_100']:
            border_col = p['color'] # Solid vibrant color for 100%
            border_w = 3
        else:
            border_col = (140, 155, 175) # Grey / silver metallic for chance spawn
            border_w = 2

        # Outer background pill
        draw.rounded_rectangle([bx-1, by-1, bx+bw+1, by+bw+1], radius=6, fill=(10, 14, 22), outline=border_col, width=border_w)
        
        # Paste container icon image in center
        img_name = p['img']
        if img_name in CONTAINER_IMGS:
            c_icon = CONTAINER_IMGS[img_name]
            inner_size = bw - 4
            c_resized = c_icon.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
            canvas.paste(c_resized, (bx+2, by+2), c_resized)
            
        # Priority 2 subtle gold ring accent
        if is_prio2:
            draw.rounded_rectangle([bx-3, by-3, bx+bw+3, by+bw+3], radius=8, outline=(255, 234, 0, 120), width=1)

    # 3. Main Raid Objectives (100% Guaranteed Spawn -> Vibrant Solid Cyan/Amber Border)
    for idx, obj in enumerate(objectives):
        ox, oy = to_map_coord(obj['x'], obj['y'])
        col = obj.get('color', (0, 229, 255)) # Priority 1 Cyan
        
        # Double pulsing rings
        draw.ellipse([ox-26, oy-26, ox+26, oy+26], fill=(*col, 80))
        draw.ellipse([ox-18, oy-18, ox+18, oy+18], fill=(*col, 140))
        draw.ellipse([ox-14, oy-14, ox+14, oy+14], fill=col, outline=(0, 0, 0), width=3)
        draw.text((ox-6, oy-11), str(idx+1), fill=(255, 255, 255), font=F_PIN_NUM)
        
        label = obj['name']
        sub = obj.get('sub', '')
        t_w = max(int(draw.textlength(label, font=F_MAP_LABEL)), int(draw.textlength(sub, font=F_TINY)))
        box_w = t_w + 24
        box_h = 44 if sub else 30
        
        # Position label in open margins
        bx, by = obj.get('label_x', ox + 90), obj.get('label_y', oy - 30)
        
        # Keep inside map bounds and away from legend
        bx = max(min(bx, MAP_X + MAP_W - box_w - 20), MAP_X + 20)
        by = max(min(by, MAP_Y + MAP_H - box_h - 20), MAP_Y + 20)
        
        draw.rounded_rectangle([bx, by, bx+box_w, by+box_h], radius=8, fill=(8, 12, 20, 250), outline=col, width=3)
        draw.text((bx+12, by+4), label, fill=(255, 255, 255), font=F_MAP_LABEL)
        if sub:
            draw.text((bx+12, by+24), sub, fill=(203, 213, 225), font=F_TINY)
            
        target_edge_x = bx if ox < bx else (bx + box_w if ox > bx + box_w else ox)
        target_edge_y = by if oy < by else (by + box_h if oy > by + box_h else oy)
        draw_arrow(draw, target_edge_x, target_edge_y, ox, oy, color=col, width=3)

    # 4. Map Container Key (Top-Left, Compact)
    lx = MAP_X + 16
    ly = MAP_Y + 16
    lw = 490
    lh = 210 if show_all_loot else 90
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(5, 9, 16, 248), outline=(90, 110, 140), width=2)
    draw.text((lx+16, ly+10), "MAP CONTAINER & SPAWN RATE KEY", fill=(255, 230, 0), font=F_SMALL_BOLD)
    
    if show_all_loot:
        draw.text((lx+16, ly+30), "• Solid Cyan / Amber Border = 100% Guaranteed Objective", fill=(0, 229, 255), font=F_TINY)
        draw.text((lx+16, ly+48), "• Grey / Metallic Border = Chance Spawn (< 100% spawn rate)", fill=(180, 195, 215), font=F_TINY)
        
        items_legend = [
            ("bullion_box.webp", (255, 234, 0), "Bullion / Jewellery Box", "Opium Pipe 13.7% · Hardest drop"),
            ("wall_cabinet.webp", (255, 234, 0), "Wall Cabinet", "China Bowl 16.1% · Hardest drop"),
            ("tooling_bin.webp", (16, 185, 129), "Tooling Bin", "Saltpetre 18.9% (Q6) · Upcoming"),
            ("stone_grave.webp", (16, 185, 129), "Stone Grave", "Damp Rag 23.8% (Q6) · Upcoming"),
            ("pile_of_ash.webp", (16, 185, 129), "Pile of Ash", "Charcoal 52.6% (Q4) · Upcoming"),
            ("flour_sack.webp", (255, 255, 255), "Flour Sack / Oak Barrel", "Flour 47.6% (Q2) · Primary")
        ]
        curr_y = ly + 72
        for img_name, col, title, desc in items_legend:
            # Container thumbnail 20x20
            if img_name in CONTAINER_IMGS:
                c_icon = CONTAINER_IMGS[img_name]
                c_r = c_icon.resize((20, 20), Image.Resampling.LANCZOS)
                canvas.paste(c_r, (lx+16, curr_y-2), c_r)
            draw.text((lx+42, curr_y), title, fill=(255, 255, 255), font=F_SMALL_BOLD)
            draw.text((lx+240, curr_y+1), desc, fill=(148, 163, 184), font=F_TINY)
            curr_y += 23
    else:
        draw.text((lx+16, ly+40), "Targeting specific quest items for this match.", fill=(203, 213, 225), font=F_SMALL)

print("V5 core ready.")
