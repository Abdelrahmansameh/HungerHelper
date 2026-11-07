import os, sys, math
from PIL import Image, ImageDraw, ImageFont

# Canvas & Layout Constants
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

# Font Setup (Clean, highly legible system fonts)
def load_font(name_list, size, bold=False):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SANS_BOLD = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

F_HEADER_TITLE = load_font(SANS_BOLD, 30)
F_HEADER_TAG = load_font(SANS_BOLD, 17)
F_SECTION_TITLE = load_font(SANS_BOLD, 22)
F_CARD_TITLE = load_font(SANS_BOLD, 19)
F_BODY_BOLD = load_font(SANS_BOLD, 17)
F_BODY = load_font(SANS_REG, 16)
F_SMALL_BOLD = load_font(SANS_BOLD, 14)
F_SMALL = load_font(SANS_REG, 14)
F_TINY = load_font(SANS_REG, 12)
F_CALLOUT_TITLE = load_font(SANS_BOLD, 19)
F_CALLOUT_SUB = load_font(SANS_REG, 15)
F_BADGE = load_font(SANS_BOLD, 13)

# Container Icons Cache
DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")

CONTAINER_IMGS = {}
ITEM_IMGS = {}

def preload_assets():
    if os.path.exists(CONT_DIR):
        for f in os.listdir(CONT_DIR):
            if f.endswith(('.webp', '.png')):
                try:
                    p = os.path.join(CONT_DIR, f)
                    CONTAINER_IMGS[f] = Image.open(p).convert("RGBA")
                except:
                    pass
    if os.path.exists(ITEM_DIR):
        for f in os.listdir(ITEM_DIR):
            if f.endswith(('.webp', '.png')):
                try:
                    p = os.path.join(ITEM_DIR, f)
                    ITEM_IMGS[f] = Image.open(p).convert("RGBA")
                except:
                    pass

preload_assets()

def paste_icon_safe(canvas, img_obj, box, bg_color=(15, 23, 42)):
    x, y, w, h = box
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=bg_color, outline=(70, 85, 105), width=1)
    if img_obj:
        resized = img_obj.resize((w-6, h-6), Image.Resampling.LANCZOS)
        canvas.paste(resized, (x+3, y+3), resized)

# Draw an arrow from (x1, y1) to (x2, y2)
def draw_arrow(draw, start, end, color=(0, 229, 255), width=3):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    
    # Arrowhead at end
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 16
    arrow_angle = math.pi / 6
    
    ax1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    ay1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    ax2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    ay2 = y2 - arrow_len * math.sin(angle + arrow_angle)
    
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

# Render clean cluster summary callout
def render_summary_callout(draw, canvas, callout):
    """
    callout dict format:
    {
      'box_x': 250, 'box_y': 380, 'target_x': 520, 'target_y': 440,
      'color': (0, 229, 255),
      'title': "Master Granary Complex",
      'count_text': "18x Flour Sacks (20x Flour Goal)",
      'spawn_badge': "100% GUARANTEED SPAWN",
      'is_100': True,
      'cont_img': 'flour_sack.webp',
      'item_img': 'flour.png',
      'sub_text': "Sweep 1st & 2nd floors + exterior barrels"
    }
    """
    bx = callout['box_x']
    by = callout['box_y']
    tx = callout['target_x']
    ty = callout['target_y']
    color = callout.get('color', (0, 229, 255))
    
    cw = 380
    ch = 94
    
    # Draw callout box
    draw.rounded_rectangle([bx, by, bx+cw, by+ch], radius=8, fill=(11, 16, 26), outline=color, width=2)
    
    # Paste container icon
    c_img = CONTAINER_IMGS.get(callout.get('cont_img'))
    if c_img:
        paste_icon_safe(canvas, c_img, (bx+8, by+8, 76, 76), bg_color=(18, 25, 38))
        
    # Paste item icon if provided
    i_img = ITEM_IMGS.get(callout.get('item_img'))
    if i_img:
        paste_icon_safe(canvas, i_img, (bx+60, by+44, 40, 40), bg_color=(25, 35, 52))

    # Text details
    text_x = bx + 95
    draw.text((text_x, by+8), callout['title'], fill=(255, 255, 255), font=F_CALLOUT_TITLE)
    draw.text((text_x, by+32), callout['count_text'], fill=color, font=F_BODY_BOLD)
    
    # Spawn rate badge
    is_100 = callout.get('is_100', True)
    badge_text = callout.get('spawn_badge', "100% GUARANTEED SPAWN" if is_100 else "VARIABLE CHANCE")
    badge_bg = (16, 185, 129) if is_100 else (120, 135, 155)
    bw = int(draw.textlength(badge_text, font=F_BADGE)) + 14
    draw.rounded_rectangle([text_x, by+55, text_x+bw, by+72], radius=4, fill=badge_bg)
    draw.text((text_x+7, by+57), badge_text, fill=(255, 255, 255) if is_100 else (15, 23, 42), font=F_BADGE)
    
    if 'sub_text' in callout and callout['sub_text']:
        draw.text((text_x + bw + 10, by+56), callout['sub_text'], fill=(180, 195, 215), font=F_TINY)

    # Determine best start point on callout box edge for the arrow
    start_x = bx + cw if tx > bx + cw else (bx if tx < bx else bx + cw//2)
    start_y = by + ch//2
    draw_arrow(draw, (start_x, start_y), (tx, ty), color=color, width=2)

print("V6 core module initialized successfully.")
