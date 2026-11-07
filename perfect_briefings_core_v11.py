import os, sys, math
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 2400
CANVAS_H = 1400

# Map occupies left 68%
MAP_X = 20
MAP_Y = 82
MAP_W = 1630
MAP_H = 1298

# Right Briefing Panel occupies remaining 31%
PANEL_X = 1670
PANEL_Y = 82
PANEL_W = 710
PANEL_H = 1298

# Priority Palette: Yellow -> Purple -> Blue
COLOR_PRIO1 = (255, 234, 0)   # Vibrant Yellow
COLOR_PRIO2 = (168, 85, 247)  # Bright Purple
COLOR_PRIO3 = (56, 189, 248)  # Electric Blue

def load_font(name_list, size):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SANS_BOLD = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

F_HEADER_TITLE = load_font(SANS_BOLD, 28)
F_HEADER_TAG = load_font(SANS_BOLD, 16)
F_SECTION_TITLE = load_font(SANS_BOLD, 19)
F_CARD_TITLE = load_font(SANS_BOLD, 16)
F_BODY_BOLD = load_font(SANS_BOLD, 14)
F_BODY = load_font(SANS_REG, 13)
F_SMALL_BOLD = load_font(SANS_BOLD, 12)
F_SMALL = load_font(SANS_REG, 12)
F_TINY = load_font(SANS_REG, 11)
F_BADGE = load_font(SANS_BOLD, 11)

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")

CONTAINER_IMGS = {}
ITEM_IMGS = {}

def preload_assets():
    if os.path.exists(CONT_DIR):
        for f in os.listdir(CONT_DIR):
            if f.endswith(('.png', '.webp', '.jpg')):
                try:
                    p = os.path.join(CONT_DIR, f)
                    CONTAINER_IMGS[f] = Image.open(p).convert("RGBA")
                except Exception as e:
                    pass
    if os.path.exists(ITEM_DIR):
        for f in os.listdir(ITEM_DIR):
            if f.endswith(('.png', '.webp', '.jpg')):
                try:
                    p = os.path.join(ITEM_DIR, f)
                    ITEM_IMGS[f] = Image.open(p).convert("RGBA")
                except Exception as e:
                    pass

preload_assets()

def paste_icon_safe(target_img, icon_img, box, bg_color=None, border_color=None, border_w=1):
    x, y, w, h = box
    if bg_color:
        draw = ImageDraw.Draw(target_img)
        draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=bg_color, outline=border_color, width=border_w)
    
    if icon_img is None:
        return
        
    pad = 3
    iw, ih = w - (pad * 2), h - (pad * 2)
    ico_resized = icon_img.resize((iw, ih), Image.Resampling.LANCZOS)
    target_img.paste(ico_resized, (x+pad, y+pad), ico_resized)

def get_rate_color(rate_str):
    try:
        val = float(rate_str.replace('%', '').strip())
        if val < 20.0:
            return (239, 68, 68)   # Red (<20%)
        elif val < 50.0:
            return (249, 115, 22)  # Orange (20-49%)
        else:
            return (34, 197, 94)   # Green (50-100%)
    except:
        return (255, 255, 255)

def render_sidebar_legend(draw, canvas, lx, ly, lw, legend_data, max_bottom=None):
    """
    Renders the Tactical Directory & Map Points Key in the empty space DOWN RIGHT of the sidebar!
    Keeps map completely clear of overlay boxes, and creates a crystal-clear 1:1 visual link
    between the map dots and the directory items.
    """
    p1_items = legend_data.get('p1_items', [])
    p2_items = legend_data.get('p2_items', [])
    p3_items = legend_data.get('p3_items', [])
    total_rows = len(p1_items) + len(p2_items) + len(p3_items)
    
    row_h = 34
    scale_bar_h = 44
    header_h = 28
    min_lh = header_h + scale_bar_h + (total_rows * (row_h + 4)) + 16
    
    if max_bottom and (max_bottom - ly) > min_lh:
        lh = max_bottom - ly
    else:
        lh = min_lh
    
    # Outer box
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(12, 16, 26), outline=(70, 85, 110), width=2)
    
    # Header
    draw.text((lx+16, ly+8), f"MAP LOOT DIRECTORY & DROP ODDS  —  {legend_data.get('map_title', '')}", fill=COLOR_PRIO1, font=F_CARD_TITLE)
    
    # Legend Scale Bar
    sb_y = ly + 32
    draw.rounded_rectangle([lx+14, sb_y, lx+lw-14, sb_y+36], radius=6, fill=(18, 24, 38), outline=(50, 65, 88), width=1)
    
    # Priority Dot Key
    # P1 (Yellow)
    draw.ellipse([lx+22, sb_y+8, lx+32, sb_y+18], fill=COLOR_PRIO1, outline=(10, 15, 20), width=1)
    draw.text((lx+38, sb_y+6), "P1: Quest Objective (Yellow Dots)", fill=COLOR_PRIO1, font=F_TINY)
    
    # P2 (Purple)
    draw.ellipse([lx+240, sb_y+8, lx+250, sb_y+18], fill=COLOR_PRIO2, outline=(10, 15, 20), width=1)
    draw.text((lx+256, sb_y+6), "P2: Rare Loot (Purple Dots)", fill=COLOR_PRIO2, font=F_TINY)
    
    # P3 (Blue)
    draw.ellipse([lx+440, sb_y+8, lx+450, sb_y+18], fill=COLOR_PRIO3, outline=(10, 15, 20), width=1)
    draw.text((lx+456, sb_y+6), "P3: Prep (Blue Dots)", fill=COLOR_PRIO3, font=F_TINY)
    
    # Drop Rate Traffic Light row
    draw.text((lx+22, sb_y+21), "Drop Rates: ", fill=(160, 180, 205), font=F_TINY)
    draw.text((lx+90, sb_y+21), "■ <20% (Red: Rare)", fill=(239, 68, 68), font=F_TINY)
    draw.text((lx+240, sb_y+21), "■ 20-49% (Orange: Medium)", fill=(249, 115, 22), font=F_TINY)
    draw.text((lx+440, sb_y+21), "■ 50-100% (Green: High)", fill=(34, 197, 94), font=F_TINY)
    
    cur_y = sb_y + 42
    
    # Render all rows
    all_groups = [
        (p1_items, COLOR_PRIO1, "P1"),
        (p2_items, COLOR_PRIO2, "P2"),
        (p3_items, COLOR_PRIO3, "P3")
    ]
    
    for items, p_col, tag in all_groups:
        for itm in items:
            cur_y = render_legend_item_row(draw, canvas, lx, cur_y, lw, itm, p_col, tag)
            
    # If there is extra space at the bottom of the directory box, render the tactical protocol tip box
    remaining_h = (ly + lh) - cur_y
    if remaining_h >= 45:
        tip_y = cur_y + 4
        tip_h = remaining_h - 10
        draw.rounded_rectangle([lx+14, tip_y, lx+lw-14, tip_y+tip_h], radius=6, fill=(16, 22, 34), outline=(40, 55, 75), width=1)
        draw.text((lx+24, tip_y+6), "TACTICAL DOT NAVIGATION & CONTAINER DROP PROTOCOL", fill=(255, 215, 0), font=F_SMALL_BOLD)
        draw.text((lx+24, tip_y+22), "• Yellow dots indicate immediate quest turn-in / gathering routes — clear them first.", fill=(210, 225, 245), font=F_TINY)
        if tip_h >= 52:
            draw.text((lx+24, tip_y+36), "• Purple dots mark rare contraband containers; sweep them on your extraction path.", fill=(200, 215, 235), font=F_TINY)
            
    return lh

def render_legend_item_row(draw, canvas, lx, cur_y, lw, itm, prio_color, tag):
    row_h = 32
    
    # 1. Matching Map Dot Indicator (Creates 1:1 visual link between point on map and this row!)
    dot_x = lx + 22
    dot_y = cur_y + 11
    draw.ellipse([dot_x-6, dot_y-6, dot_x+6, dot_y+6], fill=prio_color, outline=(10, 15, 22), width=2)
    
    # 2. Container Icon
    c_img = CONTAINER_IMGS.get(itm.get('c_ico'))
    paste_icon_safe(canvas, c_img, (lx+38, cur_y+2, 28, 28), bg_color=(15, 20, 30), border_color=prio_color, border_w=2)
    
    # 3. Item Icon
    i_img = ITEM_IMGS.get(itm.get('i_ico'))
    paste_icon_safe(canvas, i_img, (lx+70, cur_y+2, 28, 28), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)
    
    # 4. Text Info (Container -> Item)
    draw.text((lx+106, cur_y+1), f"{itm['cont']} ➔ {itm['item']}", fill=(255, 255, 255), font=F_SMALL_BOLD)
    
    # 5. Location / Zone link
    draw.text((lx+106, cur_y+16), itm['loc'][:65], fill=(185, 200, 220), font=F_TINY)
    
    # 6. Drop Rate percentage
    rate_col = get_rate_color(itm['rate'])
    draw.text((lx+lw-75, cur_y+7), itm['rate'], fill=rate_col, font=F_BODY_BOLD)
    
    return cur_y + row_h + 3

print("V11 Core Ready.")
