import os, sys
from PIL import Image, ImageDraw, ImageFont

# Test legend rendering with full text fitting
CANVAS_W = 2400
CANVAS_H = 1400
MAP_X = 20
MAP_Y = 82
MAP_W = 1630
MAP_H = 1298

def load_font(name_list, size):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SANS_BOLD = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

F_TITLE = load_font(SANS_BOLD, 17)
F_SECTION = load_font(SANS_BOLD, 14)
F_ROW_TITLE = load_font(SANS_BOLD, 13)
F_ROW_SUB = load_font(SANS_REG, 12)
F_BADGE = load_font(SANS_BOLD, 11)
F_TINY = load_font(SANS_REG, 11)

COLOR_PRIO1 = (255, 234, 0)   # Yellow
COLOR_PRIO2 = (168, 85, 247)  # Purple
COLOR_PRIO3 = (56, 189, 248)  # Blue

def get_rate_color(rate_str):
    try:
        val = float(rate_str.replace('%', '').strip())
        if val >= 50.0:
            return (34, 197, 94)    # Green
        elif val >= 20.0:
            return (249, 115, 22)   # Orange
        else:
            return (239, 68, 68)    # Red
    except:
        return (34, 197, 94) if "100" in rate_str else (255, 255, 255)

print("Test script setup complete.")
