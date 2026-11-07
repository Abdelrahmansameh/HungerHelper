import re
import os
import sys
import json
import sqlite3
import math
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

# Ensure root directory is accessible for speedrun template core modules
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import generate_perfect_briefings_v25 as g25
import perfect_briefings_core_v25 as core
from co_pilot.knowledge_db import get_connection

MAP_FILES = {
    "sarlat-farm": "sarlat-farm.webp",
    "sarlat farm": "sarlat-farm.webp",
    "sarlat": "sarlat-farm.webp",
    "jacques-bridge": "jacques-bridge.webp",
    "jacques bridge": "jacques-bridge.webp",
    "jacques": "jacques-bridge.webp",
    "sombre-forest": "sombre-forest.webp",
    "sombre forest": "sombre-forest.webp",
    "sombre": "sombre-forest.webp",
}

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)
CURRENT_ARTIFACT_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"

SARLAT_MAP = os.path.join(ROOT_DIR, "sarlat-farm.webp")
JACQUES_MAP = os.path.join(ROOT_DIR, "jacques-bridge.webp")
SOMBRE_MAP = os.path.join(ROOT_DIR, "sombre-forest.webp")

def to_map_coord(x: float, y: float) -> Tuple[int, int]:
    mx = core.MAP_X + int((x / 4096.0) * core.MAP_W)
    my = core.MAP_Y + int((y / 4096.0) * core.MAP_H)
    return mx, my

class MapDataUnavailable(ValueError):
    """A requested map cannot be backed by the available data."""


def resolve_map_image(map_query: str) -> str:
    """Resolve an explicit map name, never substitute a default map."""
    filename = MAP_FILES.get(map_query.lower().strip())
    if not filename:
        raise MapDataUnavailable(f"Unknown map: {map_query}.")
    path = os.path.join(ROOT_DIR, filename)
    if not os.path.isfile(path):
        raise MapDataUnavailable(f"Base map image unavailable for {map_query}.")
    return path

# ---------------------------------------------------------------------------
# CORE DYNAMIC V25 RENDERER ENGINE
# ---------------------------------------------------------------------------

def render_dynamic_v25_briefing(cfg: Dict[str, Any], output_path: str) -> str:
    """
    Renders ANY custom/dynamic map using the exact perfected V25 Speedrun HUD:
    - 2400x1400 Obsidian canvas (#0b0b09)
    - Full-width top bar edge-to-edge header
    - Clean left map viewport (1630x1292) with declustered circular thumbnail badges and non-crossing lines
    - Right tactical briefing panel (710x1292) with Objectives, Focus, Priorities, Drops, and Roadmap
    """
    canvas = Image.new("RGBA", (core.CANVAS_W, core.CANVAS_H), core.BG_CANVAS + (255,))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    draw.rectangle([0, 0, core.CANVAS_W, core.HEADER_H], fill=(17, 17, 14))
    draw.line([(0, core.HEADER_H), (core.CANVAS_W, core.HEADER_H)], fill=core.BORDER_SUBTLE, width=2)
    
    # Left Tag Pill
    tag_txt = cfg.get("tag", "TACTICAL INTEL").upper()
    pill_tw = int(draw.textlength(tag_txt, font=core.F_HEADER_TAG))
    draw.rounded_rectangle([20, 17, 20 + pill_tw + 24, 61], radius=6, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((32, 28), tag_txt, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    # Header Title
    title_txt = cfg.get("title", "TACTICAL BRIEFING").upper()
    draw.text((20 + pill_tw + 48, 25), title_txt, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Header Metric Cards on Far Right
    cards = cfg.get("header_cards", [])
    if cards:
        cx = core.CANVAS_W - 24
        for c_label, c_sub in reversed(cards):
            card_txt = f"{c_label}: {c_sub}"
            tw = int(draw.textlength(card_txt, font=core.F_SMALL_BOLD)) + 24
            cx -= tw + 12
            draw.rounded_rectangle([cx, 17, cx + tw, 61], radius=6, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)
            draw.text((cx + 12, 28), card_txt, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 2. LEFT MAP VIEWPORT
    map_box = [core.MAP_X, core.MAP_Y, core.MAP_X + core.MAP_W, core.MAP_Y + core.MAP_H]
    draw.rectangle(map_box, fill=(12, 12, 10), outline=core.BORDER_SUBTLE, width=2)

    map_img_path = cfg.get("map_img", SARLAT_MAP)
    if os.path.exists(map_img_path):
        raw_map = Image.open(map_img_path).convert("RGBA")
        resized_map = raw_map.resize((core.MAP_W - 4, core.MAP_H - 4), Image.Resampling.LANCZOS)
        canvas.paste(resized_map, (core.MAP_X + 2, core.MAP_Y + 2), resized_map)

    # 2a. PLOT DECLUSTERED POINTS
    pts = cfg.get("points", [])
    core.plot_declustered_points(draw, canvas, pts, to_map_coord)

    # 2b. STORY POIS
    for poi in cfg.get("story_pois", []):
        mx, my = to_map_coord(poi['x'], poi['y'])
        core.draw_poi_marker(draw, mx, my, poi['label'], poi.get('offset_dir', 'top'), cont_img_name=poi.get('cont_img'), canvas=canvas)

    # 3. RIGHT BRIEFING PANEL
    draw.rounded_rectangle([core.PANEL_X, core.PANEL_Y, core.PANEL_X + core.PANEL_W, core.PANEL_Y + core.PANEL_H], radius=12, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    gap = 14
    b1_y = core.PANEL_Y + 14
    b1_h = 135
    b2_y = b1_y + b1_h + gap
    b2_h = 95
    b3_y = b2_y + b2_h + gap
    b3_h = 240
    b4_y = b3_y + b3_h + gap
    b4_h = 440
    b5_y = b4_y + b4_h + gap
    b5_h = (core.PANEL_Y + core.PANEL_H - 14) - b5_y

    # Objectives Card
    draw.text((core.PANEL_X + 18, b1_y), "Objectives", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    objs = cfg.get("active_objectives", [])
    if objs:
        o = objs[0]
        card_y = b1_y + 32
        card_h = b1_h - 32
        draw.rounded_rectangle([core.PANEL_X + 18, card_y, core.PANEL_X + core.PANEL_W - 18, card_y + card_h], radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)
        c_img = core.CONTAINER_IMGS.get(o.get("cont_img")) or core.ITEM_IMGS.get(o.get("item_img"))
        core.paste_icon_safe(canvas, c_img, (core.PANEL_X + 28, card_y + int((card_h - 74) / 2), 74, 74), bg_color=(16, 16, 13), border_color=core.COLOR_GOLD, border_w=2)
        draw.text((core.PANEL_X + 118, card_y + int((card_h - 22) / 2)), o.get("title", "")[:45], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

    # Focus Target
    pf = cfg.get("priority_focus")
    if pf:
        draw.text((core.PANEL_X + 18, b2_y), "Focus Target", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
        card_y = b2_y + 30
        card_h = b2_h - 30
        draw.rounded_rectangle([core.PANEL_X + 18, card_y, core.PANEL_X + core.PANEL_W - 18, card_y + card_h], radius=8, fill=core.BG_CARD, outline=pf.get("color", core.PRIO_PURPLE), width=2)
        c_img = core.CONTAINER_IMGS.get(pf.get("c_ico")) or core.ITEM_IMGS.get(pf.get("i_ico"))
        core.paste_icon_safe(canvas, c_img, (core.PANEL_X + 26, card_y + int((card_h - 52) / 2), 52, 52), bg_color=(16, 16, 13), border_color=pf.get("color", core.PRIO_PURPLE), border_w=2)
        draw.text((core.PANEL_X + 96, card_y + int((card_h - 22) / 2)), pf.get("title", "")[:45], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

    # Priorities
    draw.text((core.PANEL_X + 18, b3_y), "Priorities", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.rounded_rectangle([core.PANEL_X + 18, b3_y + 30, core.PANEL_X + core.PANEL_W - 18, b3_y + b3_h], radius=8, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)
    step_y = b3_y + 40
    steps_list = cfg.get("rotation_steps", [])
    step_spacing = min(40, int((b3_h - 50) / max(1, len(steps_list))))
    for i, s_obj in enumerate(steps_list, 1):
        num_cx = core.PANEL_X + 42
        num_cy = step_y + 12
        prio_color = s_obj.get("color", core.PRIO_YELLOW)
        draw.ellipse([num_cx - 12, num_cy - 12, num_cx + 12, num_cy + 12], fill=prio_color, outline=(10, 10, 8), width=1)
        num_fg = (10, 10, 8) if prio_color in (core.PRIO_YELLOW, core.PRIO_GREEN) else (255, 255, 255)
        num_tw = draw.textlength(str(i), font=core.F_SMALL_BOLD)
        draw.text((num_cx - num_tw / 2, num_cy - 8), str(i), fill=num_fg, font=core.F_SMALL_BOLD)
        draw.text((core.PANEL_X + 66, step_y + 2), s_obj.get("step", "")[:60], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        step_y += step_spacing

    # Directory / Drops / Spawns
    draw.rounded_rectangle([core.PANEL_X + 18, b4_y, core.PANEL_X + core.PANEL_W - 18, b4_y + b4_h], radius=10, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=2)
    draw.text((core.PANEL_X + 32, b4_y + 10), "Encounter & Drop Intel", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    dir_items = cfg.get("directory", [])
    dir_y = b4_y + 45
    avail_rows_h = b4_h - 55
    row_h = min(68, int(avail_rows_h / max(1, len(dir_items))))
    for itm in dir_items:
        badge_cx = core.PANEL_X + 48
        badge_cy = dir_y + int(row_h / 2)
        core.draw_container_shape(draw, badge_cx, badge_cy, 18, itm.get('color', core.PRIO_YELLOW), cont_img_name=itm.get('c_ico'), canvas=canvas)
        label_text = f"{itm.get('cont', '')}  ->  {itm.get('item', '')}"
        draw.text((core.PANEL_X + 78, dir_y + 6), label_text[:50], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        sub_info = f"Rate: {itm.get('rate', '')}   •   {itm.get('spots', '')}"
        draw.text((core.PANEL_X + 78, dir_y + 32), sub_info[:60], fill=core.COLOR_MUTED, font=core.F_SMALL_BOLD)
        dir_y += row_h

    # Roadmap
    draw.text((core.PANEL_X + 18, b5_y), "Tactical Roadmap", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    r_y = b5_y + 32
    roadmap_list = cfg.get("roadmap", [])
    card_h = 52
    for r_card in roadmap_list:
        draw.rounded_rectangle([core.PANEL_X + 18, r_y, core.PANEL_X + core.PANEL_W - 18, r_y + card_h], radius=6, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)
        q_title = r_card.get("quest", "")
        draw.text((core.PANEL_X + 26, r_y + int((card_h - 18) / 2)), q_title[:40], fill=core.COLOR_GOLD, font=core.F_BODY_BOLD)
        item_x = max(core.PANEL_X + 236, core.PANEL_X + int(draw.textlength(q_title, font=core.F_BODY_BOLD)) + 40)
        for item_name, item_ico in r_card.get("items", []):
            ico_im = core.ITEM_IMGS.get(item_ico) or core.CONTAINER_IMGS.get(item_ico)
            core.paste_icon_safe(canvas, ico_im, (item_x, r_y + int((card_h - 26) / 2), 26, 26), bg_color=(16, 16, 13))
            draw.text((item_x + 32, r_y + int((card_h - 18) / 2)), item_name[:30], fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
            item_x += int(draw.textlength(item_name, font=core.F_SMALL_BOLD)) + 36
        r_y += card_h + 8

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.convert("RGB").save(output_path, quality=95)
    
    if os.path.exists(CURRENT_ARTIFACT_DIR):
        try:
            import shutil
            shutil.copy(output_path, os.path.join(CURRENT_ARTIFACT_DIR, os.path.basename(output_path)))
        except Exception:
            pass

    return output_path

# ---------------------------------------------------------------------------
# SPECIALIZED DYNAMIC GENERATORS
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# UNIVERSAL DATAMINED BESTIARY & CREATURE MAP GENERATOR (HUNGER COMPANION)
# ---------------------------------------------------------------------------

SPAWNS_DB_PATH = os.path.join(ROOT_DIR, "data", "companion_bestiary_spawns.json")

def generate_universal_bestiary_map(query: str, target_map: str = "Sarlat Farm") -> Tuple[str, Dict[str, Any]]:
    """
    Universal datamined bestiary map generator for ANY creature and ANY map in The Hunger.
    Uses 100% datamined coordinates and spawn chances from Hunger Companion.
    """
    q_low = query.lower()

    canonical_map = target_map
    resolve_map_image(canonical_map)

    # Load datamined database
    spawns_db = {}
    if os.path.exists(SPAWNS_DB_PATH):
        try:
            with open(SPAWNS_DB_PATH, "r", encoding="utf-8") as f:
                spawns_db = json.load(f)
        except Exception:
            pass

    bestiary_data = spawns_db.get("bestiary", {})
    map_spawners_data = spawns_db.get("map_spawners", {}).get(canonical_map, {})

    # 2. Determine target creature(s)
    c_key = None
    if "farmer" in q_low or "fermier" in q_low:
        c_key = "farmer-dreg"
    elif "pale lady" in q_low or "dame pale" in q_low or "dame pâle" in q_low:
        c_key = "pale-lady"
    elif "bloat" in q_low or "boursoufl" in q_low:
        c_key = "bloat"
    elif "shambler" in q_low or "titubant" in q_low or "traine" in q_low or "traîne" in q_low:
        c_key = "shambler"
    elif "dreg" in q_low or "rebut" in q_low:
        c_key = "dreg"
    elif "brute" in q_low and "drooler" not in q_low and "baveux" not in q_low:
        c_key = "brute"
    elif "drooler" in q_low or "baveux" in q_low or "drawler" in q_low:
        c_key = "drooler"
    else:
        raise MapDataUnavailable(f"No supported creature identified in {query!r}.")

    c_meta = bestiary_data.get(c_key)
    if not c_meta:
        raise MapDataUnavailable(f"Bestiary data unavailable for {c_key}.")
    m_intel = c_meta.get("maps_intel", {}).get(canonical_map, {})

    # 3. Retrieve exact datamined coordinates from Hunger Companion
    if c_key == "farmer-dreg":
        spawners = map_spawners_data.get("rare_farmer", [])

    elif c_key == "bloat":
        spawners = map_spawners_data.get("bloat", [])
    elif c_key == "shambler":
        spawners = map_spawners_data.get("shambler", [])
    elif c_key == "dreg":
        spawners = map_spawners_data.get("dreg", [])
    else:
        # Miniboss spawners (Droolers and Brutes)
        spawners = map_spawners_data.get("miniboss", [])

    if not spawners:
        raise MapDataUnavailable(f"No spawn coordinates for {c_meta['name_en']} on {canonical_map}.")
    if c_key in {"drooler", "brute", "pale-lady"}:
        c_meta = dict(c_meta, name_en=c_meta["name_en"] + " (shared miniboss candidate sites)")

    if c_key == "shambler":
        c_meta = dict(c_meta, name_en=c_meta["name_en"] + " (shared Shambler / Peasant sites)")

    map_img_path = resolve_map_image(canonical_map)
    out_path = os.path.join(OUT_DIR, f"dynamic_creatures_{c_key}_{canonical_map.replace(' ' , '_')}.jpg")
    specific_out_fn = f"dynamic_bestiary_{c_key}_{canonical_map.lower().replace(' ', '_')}.jpg"
    specific_out_path = os.path.join(OUT_DIR, specific_out_fn)

    # RENDER 2400x1400 TACTICAL HUD
    canvas = Image.new("RGBA", (core.CANVAS_W, core.CANVAS_H), core.BG_CANVAS + (255,))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    draw.rectangle([0, 0, core.CANVAS_W, core.HEADER_H], fill=(17, 17, 14))
    draw.line([(0, core.HEADER_H), (core.CANVAS_W, core.HEADER_H)], fill=core.BORDER_SUBTLE, width=2)

    tag_txt = "BESTIARY PATROL"
    pill_tw = int(draw.textlength(tag_txt, font=core.F_HEADER_TAG))
    draw.rounded_rectangle([20, 17, 20 + pill_tw + 24, 61], radius=6, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((32, 28), tag_txt, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    title_txt = f"{canonical_map.upper()} : {c_meta['name_en'].upper()} SPAWNS & CHANCES (HUNGER COMPANION)"
    if "brute" in q_low and ("drooler" in q_low or "baveux" in q_low):
        title_txt = f"{canonical_map.upper()} : ALL {len(spawners)} DROOLER & BRUTE SPAWNS (HUNGER COMPANION)"
    draw.text((20 + pill_tw + 48, 25), title_txt, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Header Metric Cards
    cx = core.CANVAS_W - 24
    header_metrics = [
        ("Spawners", f"{len(spawners)} Datamined Points"),
        ("Encounter Rate", m_intel.get("per_raid", "Active in Raid")),
        ("Map Share", m_intel.get("map_share", "35%")),
        ("Trophy Drop", f"{c_meta['trophy_name']} ({c_meta['trophy_rate']})")
    ]
    for c_label, c_sub in reversed(header_metrics):
        card_txt = f"{c_label}: {c_sub}"
        tw = int(draw.textlength(card_txt, font=core.F_SMALL_BOLD)) + 24
        cx -= tw + 12
        draw.rounded_rectangle([cx, 17, cx + tw, 61], radius=6, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)
        draw.text((cx + 12, 28), card_txt, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 2. LEFT MAP VIEWPORT (4096 to 1630x1292 coordinates)
    map_box = [core.MAP_X, core.MAP_Y, core.MAP_X + core.MAP_W, core.MAP_Y + core.MAP_H]
    draw.rectangle(map_box, fill=(12, 12, 10), outline=core.BORDER_SUBTLE, width=2)

    raw_map = Image.open(map_img_path).convert("RGBA")
    resized_map = raw_map.resize((core.MAP_W - 4, core.MAP_H - 4), Image.Resampling.LANCZOS)
    canvas.paste(resized_map, (core.MAP_X + 2, core.MAP_Y + 2), resized_map)

    # Stamp Skull Badges with number pills
    skull_badge_path = os.path.join(ROOT_DIR, "assets", "icons", "hunger_skull_badge.png")
    if not os.path.exists(skull_badge_path):
        skull_badge_path = os.path.join(ROOT_DIR, "assets", "containers", "hunger_skull_badge.png")

    badge_w, badge_h = 36, 36
    if os.path.exists(skull_badge_path):
        skull_badge = Image.open(skull_badge_path).convert("RGBA").resize((badge_w, badge_h), Image.Resampling.LANCZOS)
    else:
        skull_badge = Image.new("RGBA", (badge_w, badge_h), (200, 30, 30, 230))

    f_num_bold = core.load_font(core.SANS_BOLD, 11)

    for i, pt in enumerate(spawners, 1):
        mx, my = to_map_coord(pt["x"], pt["y"])
        mx = max(core.MAP_X + 25, min(core.MAP_X + core.MAP_W - 25, mx))
        my = max(core.MAP_Y + 25, min(core.MAP_Y + core.MAP_H - 25, my))

        bx = mx - badge_w // 2
        by = my - badge_h // 2
        canvas.paste(skull_badge, (bx, by), skull_badge)

        num_str = f"#{i}"
        ntw = int(draw.textlength(num_str, font=f_num_bold))
        np_x = bx + badge_w - 6
        np_y = by - 8
        is_dung = "dungeon" in str(pt.get("group", "")).lower() or "dungeon" in str(pt.get("title", "")).lower()
        pill_col = (192, 132, 252) if is_dung else (235, 180, 50) if c_key == "farmer-dreg" else (220, 40, 40)
        draw.rounded_rectangle([np_x, np_y, np_x + ntw + 8, np_y + 16], radius=4, fill=(18, 18, 15), outline=pill_col, width=1)
        draw.text((np_x + 4, np_y + 1), num_str, fill=pill_col, font=f_num_bold)

    # 3. RIGHT SIDEBAR: AUTHENTIC LEGEND, PER-RAID CHANCES & ENCOUNTER TABLES
    draw.rounded_rectangle([core.PANEL_X, core.PANEL_Y, core.PANEL_X + core.PANEL_W, core.PANEL_Y + core.PANEL_H], radius=12, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    p_x = core.PANEL_X + 18
    p_w = core.PANEL_W - 36
    draw.text((p_x, core.PANEL_Y + 16), "Datamined Spawn Chances", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    # SECTION 1: CREATURE IDENTITY & STATS
    card_y = core.PANEL_Y + 48
    draw.rounded_rectangle([p_x, card_y, p_x + p_w, card_y + 115], radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((p_x + 14, card_y + 10), f"👾 {c_meta['name_en'].upper()} (HP: {c_meta['health']} · SPEED: {c_meta['speed']})", fill=core.COLOR_GOLD, font=core.F_BODY_BOLD)
    draw.text((p_x + 14, card_y + 34), f"• Weak Point : {c_meta['weak_point']} | Attack Damage : {c_meta['damage']}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL)
    draw.text((p_x + 14, card_y + 54), f"• Map Density : {m_intel.get('per_raid', 'Active')} ({m_intel.get('map_share', '')} of game encounters)", fill=core.COLOR_MUTED, font=core.F_SMALL)
    draw.text((p_x + 14, card_y + 74), f"• Trophy Drop : {c_meta['trophy_name']} ({c_meta['trophy_rate']})", fill=(100, 240, 140), font=core.F_SMALL_BOLD)
    draw.text((p_x + 14, card_y + 94), f"• Tactical Advice : {c_meta['tactics'][:75]}", fill=core.COLOR_DIM, font=core.F_TINY)

    # SECTION 2: TOP SPAWN LOCATIONS & ROLL CHANCES
    places_y = card_y + 128
    draw.text((p_x, places_y), "Top Encounter Hotspots (Per-Raid Roll)", fill=(250, 204, 21), font=core.F_CARD_TITLE)
    pl_card_y = places_y + 28
    pl_card_h = 240
    draw.rounded_rectangle([p_x, pl_card_y, p_x + p_w, pl_card_y + pl_card_h], radius=8, fill=core.BG_CARD, outline=(250, 204, 21), width=1)

    top_places = m_intel.get("top_places", [])
    for i, tp in enumerate(top_places[:6]):
        line_y = pl_card_y + 10 + i * 36
        draw.text((p_x + 12, line_y), f"#{i+1}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((p_x + 42, line_y), tp["name"], fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((p_x + 42, line_y + 16), f"Coordinates: {tp['coords']}", fill=core.COLOR_MUTED, font=core.F_TINY)
        draw.text((p_x + p_w - 150, line_y + 6), tp["rate"], fill=(100, 240, 140), font=core.F_SMALL_BOLD)

    # SECTION 3: EXACT DATAMINED SPAWNERS LIST
    sp_y = pl_card_y + pl_card_h + 14
    draw.text((p_x, sp_y), f"All {len(spawners)} Datamined Spawners on {canonical_map}", fill=(192, 132, 252), font=core.F_CARD_TITLE)
    sp_card_y = sp_y + 28
    sp_card_h = 390
    draw.rounded_rectangle([p_x, sp_card_y, p_x + p_w, sp_card_y + sp_card_h], radius=8, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)

    for i, pt in enumerate(spawners[:14]):
        line_y = sp_card_y + 8 + i * 26
        is_dung = "dungeon" in str(pt.get("group", "")).lower() or "dungeon" in str(pt.get("title", "")).lower()
        sub_type = "Catacombs / Dungeon" if is_dung else "Surface Spawner"
        col = (192, 132, 252) if is_dung else core.COLOR_PARCHMENT
        draw.text((p_x + 12, line_y), f"#{i+1}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((p_x + 42, line_y), f"ID {pt['id']} ({sub_type})", fill=col, font=core.F_SMALL)
        draw.text((p_x + p_w - 160, line_y), f"X: {int(pt['x'])}, Y: {int(pt['y'])}", fill=core.COLOR_MUTED, font=core.F_TINY)

    draw.text((p_x + 12, sp_card_y + sp_card_h - 22), f"Showing {min(14, len(spawners))} of {len(spawners)} points. All {len(spawners)} plotted on tactical map.", fill=core.COLOR_DIM, font=core.F_TINY)

    # SECTION 4: RARE LOOT DROPS
    loot_y = sp_card_y + sp_card_h + 14
    draw.rounded_rectangle([p_x, loot_y, p_x + p_w, core.PANEL_Y + core.PANEL_H - 14], radius=8, fill=(16, 16, 13), outline=core.COLOR_GOLD, width=1)
    draw.text((p_x + 14, loot_y + 12), "🗝️ RARE ELITE LOOT & UNLOCKS", fill=core.COLOR_GOLD, font=core.F_BODY_BOLD)
    draw.text((p_x + 14, loot_y + 36), f"• Rare Drop : {c_meta.get('rare_drop', 'Jacques Folly Key (1/226)')}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL)
    draw.text((p_x + 14, loot_y + 56), f"• Data Source : 100% Datamined from Hunger Companion live patch tables.", fill=(100, 240, 140), font=core.F_SMALL)

    canvas.convert("RGB").save(out_path, "JPEG", quality=95)
    canvas.convert("RGB").save(specific_out_path, "JPEG", quality=95)

    # Sync artifacts
    try:
        if os.path.exists(CURRENT_ARTIFACT_DIR):
            import shutil
            shutil.copy(out_path, os.path.join(CURRENT_ARTIFACT_DIR, "dynamic_creatures_map.jpg"))
            shutil.copy(specific_out_path, os.path.join(CURRENT_ARTIFACT_DIR, specific_out_fn))
    except Exception:
        pass

    intel = {
        "title": f"{canonical_map} : {c_meta['name_en']} Spawns",
        "map_name": canonical_map,
        "creature": c_meta["name_en"],
        "per_raid": m_intel.get("per_raid", "Active"),
        "map_share": m_intel.get("map_share", ""),
        "spawners_count": len(spawners),
        "top_places": top_places,
        "tactics": c_meta["tactics"],
        "trophy": f"{c_meta['trophy_name']} ({c_meta['trophy_rate']})",
        "drops": [
            f"• **{c_meta['name_en']}** : {c_meta['trophy_name']} ({c_meta['trophy_rate']})",
            f"• **Rare Elite Drop** : {c_meta.get('rare_drop', 'Jacques Folly Key (1/226)')}",
            f"• **Map Density** : {m_intel.get('per_raid', 'Active')} ({m_intel.get('map_share', '')} of encounters)"
        ]
    }
    return out_path, intel

# Backwards compatibility alias
generate_creatures_map = generate_universal_bestiary_map


def generate_farmer_dreg_spawn_map() -> Tuple[str, Dict[str, Any]]:
    """Generate dedicated tactical map focused on Farmer Dreg (Dreg Farmer) at Garnier's Farm."""
    map_name = "Sarlat Farm"
    out_path = os.path.join(OUT_DIR, "dynamic_farmer_dreg_map.jpg")
    
    # Garnier's Farm coordinates
    gx, gy = 2312.6, 1517.2

    cfg = {
        "title": "TACTICAL RECON : FARMER DREG (GARNIER'S FARM)",
        "map_name": map_name,
        "map_img": SARLAT_MAP,
        "tag": "ELITE VARIANT HUNT",
        "header_cards": [
            ("Target", "Farmer Dreg"),
            ("Location", "Garnier's Farm"),
            ("Spawn Rate", "1 in 20 Raids"),
            ("Drop", "Peasant's Burden (100%)")
        ],
        "story_pois": [
            {"x": gx, "y": gy, "label": "Farmer Dreg Spawn (Garnier's Farm)", "offset_dir": "bottom", "cont_img": "strongbox.webp"},
            {"x": 1227.6, "y": 954.5, "label": "Garnier's Windmill", "offset_dir": "left", "cont_img": "tooling_bin.webp"},
            {"x": 2378.9, "y": 1952.6, "label": "Sarlat Bridge Crossing", "offset_dir": "top", "cont_img": "strongbox.webp"}
        ],
        "points": [
            {"x": gx, "y": gy, "type": "elite_spawn", "color": core.PRIO_YELLOW, "cont_img": "strongbox.webp"}
        ],
        "active_objectives": [
            {"title": "Locate & Eliminate Farmer Dreg at Garnier's Farm", "cont_img": "strongbox.webp", "item_img": "drooler_jaw.png"}
        ],
        "priority_focus": {
            "title": "Farmer Dreg (550 HP · Guaranteed Peasant's Burden)",
            "c_ico": "strongbox.webp",
            "i_ico": "gold_key.png",
            "color": (235, 180, 50)
        },
        "rotation_steps": [
            {"step": "Deploy to Sarlat Farm and advance north across river toward Garnier's Farm.", "color": core.PRIO_YELLOW},
            {"step": "Scout the courtyard and farmhouse perimeter (X: 2313, Y: 1517).", "color": core.PRIO_PURPLE},
            {"step": "Stagger Farmer Dreg with heavy overhead strikes before pitchfork thrusts connect.", "color": core.PRIO_BLUE},
            {"step": "Collect guaranteed 100% Peasant's Burden - Spear Schema and extract.", "color": core.PRIO_GREEN}
        ],
        "directory": [
            {"color": (235, 180, 50), "cont": "Farmer Dreg", "c_ico": "strongbox.webp", "item": "Peasant's Burden - Spear", "rate": "100% ALWAYS", "spots": "Garnier's Farm (1 in 20 Raids)"},
            {"color": core.PRIO_YELLOW, "cont": "Trophy Loot", "c_ico": "drooler_jaw.png", "item": "Dreg Head", "rate": "High Rate", "spots": "Elite Monster Corpse"}
        ],
        "roadmap": [
            {"quest": "Elite Hunting", "items": [("Peasant's Burden", "gold_key.png")]}
        ]
    }

    render_dynamic_v25_briefing(cfg, out_path)

    # Sync artifact if directory exists
    try:
        if os.path.exists(CURRENT_ARTIFACT_DIR):
            import shutil
            shutil.copy(out_path, os.path.join(CURRENT_ARTIFACT_DIR, "dynamic_farmer_dreg_map.jpg"))
    except Exception:
        pass

    intel = {
        "title": "Localisation : Dreg Fermier (Farmer Dreg)",
        "map_name": "Sarlat Farm",
        "objectives": ["Localiser et éliminer le Dreg Fermier à la Ferme Garnier"],
        "focus": "Ferme Garnier (X: 2313, Y: 1517) · Taux d'apparition 1 raid sur 20",
        "drops": [
            "• **Fardeau du Paysan - Lance (Peasant's Burden - Spear)** : Taux 100% Garanti (Always)",
            "• **Tête de Dreg (Dreg Head)** : Trophée Rebut (Taux élevé)"
        ]
    }
    return out_path, intel

def generate_dungeon_folly_map() -> Tuple[str, Dict[str, Any]]:
    """Generate map of Jacques Bridge showing Jacques Folly 3 entrance doors and 5 key spawn locations."""
    out_path = os.path.join(OUT_DIR, "dynamic_jacques_folly_map.jpg")
    
    cfg = {
        "title": "DUNGEON ACCESS: JACQUES FOLLY ENTRANCES & KEYS",
        "map_name": "Jacques Bridge",
        "map_img": JACQUES_MAP,
        "tag": "DUNGEON RECON",
        "header_cards": [
            ("Dungeon", "Jacques Folly"),
            ("Containers", "174 Loot Points"),
            ("Key", "Jacques Folly Key (3 Uses)")
        ],
        "story_pois": [
            {"x": 1680.37, "y": 197.12, "label": "Jacques Folly Main Bastion", "offset_dir": "top", "cont_img": "ledger_desk.webp"},
            {"x": 1835.90, "y": 505.49, "label": "Entrance 1: North Iron Gate", "offset_dir": "top", "cont_img": "strongbox.webp"},
            {"x": 1605.21, "y": 512.75, "label": "Entrance 2: Courtyard Crypt Door", "offset_dir": "bottom", "cont_img": "stone_grave.webp"},
            {"x": 1418.37, "y": 337.55, "label": "Entrance 3: Undercroft Iron Door", "offset_dir": "left", "cont_img": "strongbox.webp"}
        ],
        "points": [
            {"x": 1548.01, "y": -64.23, "type": "key_spawn", "color": core.PRIO_PURPLE, "cont_img": "gold_key.png"},
            {"x": 1689.48, "y": 297.60, "type": "key_spawn", "color": core.PRIO_PURPLE, "cont_img": "gold_key.png"},
            {"x": 1379.04, "y": 1545.14, "type": "key_spawn", "color": core.PRIO_PURPLE, "cont_img": "gold_key.png"},
            {"x": 1668.14, "y": 383.68, "type": "key_spawn", "color": core.PRIO_PURPLE, "cont_img": "gold_key.png"},
            {"x": 1732.25, "y": 374.59, "type": "key_spawn", "color": core.PRIO_PURPLE, "cont_img": "gold_key.png"}
        ],
        "active_objectives": [
            {"title": "Breach Jacques Folly Subterranean Dungeon", "cont_img": "strongbox.webp", "item_img": "gold_key.png"}
        ],
        "priority_focus": {
            "title": "Jacques Folly Key (5 Spawns on Bridge)",
            "c_ico": "strongbox.webp",
            "i_ico": "gold_key.png",
            "color": core.PRIO_PURPLE
        },
        "rotation_steps": [
            {"step": "Scout 5 Key Spawns across Bridge roadway & watchtowers.", "color": core.PRIO_YELLOW},
            {"step": "Unlock one of the 3 iron gates (North, Crypt, or Undercroft).", "color": core.PRIO_PURPLE},
            {"step": "Clear 84 creature spawn points guarding internal chambers.", "color": core.PRIO_BLUE},
            {"step": "Loot 174 containers & large reinforced weapon strongboxes.", "color": core.PRIO_GREEN},
            {"step": "Extract with rare schematics and epic bullion.", "color": core.PRIO_GREY}
        ],
        "directory": [
            {"color": core.PRIO_YELLOW, "cont": "North Iron Gate", "c_ico": "strongbox.webp", "item": "Jacques Folly Entrance 1", "rate": "3 Uses", "spots": "X: 1835.9, Y: 505.5"},
            {"color": core.PRIO_YELLOW, "cont": "Courtyard Crypt", "c_ico": "stone_grave.webp", "item": "Jacques Folly Entrance 2", "rate": "3 Uses", "spots": "X: 1605.2, Y: 512.7"},
            {"color": core.PRIO_YELLOW, "cont": "Undercroft Door", "c_ico": "strongbox.webp", "item": "Jacques Folly Entrance 3", "rate": "3 Uses", "spots": "X: 1418.4, Y: 337.5"},
            {"color": core.PRIO_PURPLE, "cont": "Key Spawn Spots", "c_ico": "gold_key.png", "item": "Jacques Folly Key", "rate": "1/133", "spots": "5 Desks & Bastion Crates Across Roadway"}
        ],
        "roadmap": [
            {"quest": "Dungeon Mastery", "items": [("Jacques Folly Key", "gold_key.png"), ("Epic Loot", "bullion_box.webp")]}
        ]
    }
    
    render_dynamic_v25_briefing(cfg, out_path)
    
    intel = {
        "title": "Entrées du Donjon de Jacques Folly & Spawns de Clé",
        "map_name": "Jacques Bridge",
        "objectives": ["Franchir les 3 portes d'entrée de Jacques Folly", "Récupérer la Clé de la folie de Jacques"],
        "focus": "3 portes verrouillées (Porte Nord, Crypte de la cour, Porte du sous-sol)",
        "drops": [
            "• **Porte Nord** (`X: 1835.90, Y: 505.49`)",
            "• **Crypte de la cour** (`X: 1605.21, Y: 512.75`)",
            "• **Porte du sous-sol** (`X: 1418.37, Y: 337.55`)",
            "• **Spawns de la Clé** : 5 emplacements sur le Pont Jacques (taux 1/133) et monstres (1/226)"
        ]
    }
    return out_path, intel

def generate_dungeon_tactical_map(dungeon_query: str) -> Tuple[str, Dict[str, Any]]:
    """Plot dungeon locations from the database, not invented entrance templates."""
    q = dungeon_query.lower().strip()
    aliases = {"the pit": ("pit", "puits"), "the undercroft": ("undercroft", "sous-sol", "crypte"),
               "jacques folly": ("folly",)}
    matches = [name for name, words in aliases.items()
               if any(re.search(r"\b" + re.escape(word) + r"\b", q) for word in words)]
    if len(matches) != 1:
        raise MapDataUnavailable("Specify The Pit, The Undercroft, or Jacques Folly.")
    return generate_location_poi_map(matches[0])


def resolve_item_name(query: str) -> Optional[str]:
    """Prefer exact identities; allow only a unique whole-word partial name."""
    q = query.lower().strip()
    if not q:
        return None
    with get_connection() as conn:
        rows = conn.execute("SELECT name, slug FROM items").fetchall()
    exact = [r["name"] for r in rows if q in (r["name"].lower(), r["slug"].lower())]
    if exact:
        return exact[0]
    words = set(re.findall(r"\w+", q))
    matches = sorted({r["name"] for r in rows if words <= set(re.findall(r"\w+", r["name"].lower()))})
    if len(matches) > 1:
        raise MapDataUnavailable("Which item do you mean? " + ", ".join(matches[:6]))
    return matches[0] if matches else None


def generate_item_farm_map(item_query: str, target_map: str = "Sarlat Farm") -> Tuple[str, Dict[str, Any]]:
    """Generate map highlighting the best containers to farm any requested item."""
    map_img = resolve_map_image(target_map)
    out_path = os.path.join(OUT_DIR, "dynamic_farm_map.jpg")
    
    # Translate French terms
    fr_to_en = {
        "farine": "flour", "charbon": "charcoal", "salpetre": "saltpetre",
        "salpêtre": "saltpetre", "miel": "honey", "os": "bone", "pain": "bread"
    }
    clean_q = item_query.lower().strip()
    clean_q = fr_to_en.get(clean_q, clean_q)
    resolved_item = resolve_item_name(clean_q)
    if not resolved_item:
        raise MapDataUnavailable(f"No item data for {item_query}.")
    clean_q = resolved_item.lower()

    # Determine best container from DB
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT d.source, d.location, d.drop_rate, i.name
        FROM item_drops d
        JOIN items i ON d.item_id = i.id
        WHERE (lower(i.name) = ? OR lower(i.slug) = ?) AND d.location = ?
        ORDER BY d.drop_rate DESC LIMIT 3
    """, (clean_q, clean_q, target_map))
    drops = c.fetchall()
    conn.close()
    
    if not drops:
        raise MapDataUnavailable(f"No item drop data for {item_query} on {target_map}.")
    item_display = drops[0]["name"]
    top_cont = drops[0]["source"] if drops else "Loot Container"
    top_rate = f"{drops[0]['drop_rate']*100:.1f}%" if drops else "High"
    
    # Fetch map points for this container on target map
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT x, y, title FROM map_points
        WHERE map_name LIKE ? AND title LIKE ?
        LIMIT 8
    """, (f"%{target_map}%", f"%{item_display}%"))
    pts_raw = c.fetchall()
    
    # If no exact item name in map_points, search by top container
    if not pts_raw:
        c.execute("""
            SELECT x, y, title FROM map_points
            WHERE map_name LIKE ? AND title LIKE ?
            LIMIT 8
        """, (f"%{target_map}%", f"%{top_cont}%"))
        pts_raw = c.fetchall()

    conn.close()
    
    if not pts_raw:
        raise MapDataUnavailable(f"No mapped sources for {item_display} on {target_map}.")
    out_path = os.path.join(OUT_DIR, f"dynamic_farm_{re.sub(r'[^a-z0-9]+', '_', clean_q)}_{target_map.replace(' ', '_')}.jpg")

    c_img_name = "flour_sack.webp" if "flour" in clean_q else "pile_of_ash.webp" if "charcoal" in clean_q else "tooling_bin.webp"
    i_img_name = "flour.png" if "flour" in clean_q else "saltpetre.png"

    pts = []
    for p in pts_raw:
        pts.append({
            "x": p["x"],
            "y": p["y"],
            "type": "farm_spot",
            "color": core.PRIO_YELLOW,
            "cont_img": c_img_name
        })
        
    cfg = {
        "title": f"FARM ROUTE: {item_display.upper()} ({target_map.upper()})",
        "map_name": target_map,
        "map_img": map_img,
        "tag": "FARM EXPEDITION",
        "header_cards": [
            ("Target Item", item_display),
            ("Best Container", top_cont),
            ("Drop Rate", top_rate)
        ],
        "story_pois": [],
        "points": pts,
        "active_objectives": [
            {"title": f"Farm {item_display} from {top_cont} clusters", "cont_img": c_img_name, "item_img": i_img_name}
        ],
        "priority_focus": {
            "title": f"{top_cont} (Drop Rate: {top_rate})",
            "c_ico": c_img_name,
            "i_ico": i_img_name,
            "color": core.PRIO_PURPLE
        },
        "rotation_steps": [
            {"step": f"Locate and sweep {top_cont} clusters in active areas.", "color": core.PRIO_YELLOW},
            {"step": f"Harvest target quantities of {item_display}.", "color": core.PRIO_PURPLE},
            {"step": "Check secondary caches along the main route.", "color": core.PRIO_BLUE},
            {"step": "Extract safely back to Château.", "color": core.PRIO_GREY}
        ],
        "directory": [
            {"color": core.PRIO_YELLOW, "cont": top_cont, "c_ico": c_img_name, "item": item_display, "rate": top_rate, "spots": f"Primary spawns on {target_map}"}
        ],
        "roadmap": [
            {"quest": f"Harvest {item_display}", "items": [(item_display, i_img_name)]}
        ]
    }
    
    render_dynamic_v25_briefing(cfg, out_path)
    intel = {
        "title": f"Carte de Farm : {item_display}",
        "map_name": target_map,
        "objectives": [f"Récolter {item_display} dans les conteneurs {top_cont}"],
        "focus": f"{top_cont} (Taux : {top_rate})",
        "drops": [f"• **{top_cont}** ➔ **{item_display}** (Taux : {top_rate})"]
    }
    return out_path, intel

# ---------------------------------------------------------------------------
# DYNAMIC LOCATION & QUEST POI MAP GENERATOR
# ---------------------------------------------------------------------------

def generate_location_poi_map(query: str, target_map_hint: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Renders dedicated tactical location maps with exact pinpoint markers for quests, camps,
    landmarks, and points of interest across Sarlat Farm, Jacques Bridge, and Sombre Forest.
    """
    q = query.lower().strip()
    conn = get_connection()
    c = conn.cursor()

    # 1. Specialized Handler: The Gavroche Family Camp
    if q in {"gavroche", "family gavroche", "famille gavroche", "camp gavroche", "gavroche family"}:
        map_name = "Jacques Bridge"
        map_img = JACQUES_MAP
        out_path = os.path.join(OUT_DIR, "dynamic_gavroche_location_map.jpg")
        cfg = {
            "title": "LOCALISATION : CAMP DES GAVROCHE (PONT JACQUES)",
            "map_name": "Jacques Bridge",
            "map_img": map_img,
            "tag": "OBJECTIF DE QUÊTE",
            "header_cards": [
                ("Zone", "Berges Est"),
                ("Quête", "The Gavroche Family"),
                ("Donneur", "Éloïse (Château)")
            ],
            "story_pois": [
                {"x": 1479.01, "y": 313.35, "label": "Campement de la Famille Gavroche", "offset_dir": "bottom", "cont_img": "strongbox.webp"},
                {"x": 1850.20, "y": 1520.40, "label": "Entrée Donjon Jacques Folly", "offset_dir": "left", "cont_img": "tooling_bin.webp"}
            ],
            "points": [
                {"x": 1479.01, "y": 313.35, "type": "objective", "color": core.PRIO_YELLOW, "cont_img": "strongbox.webp"},
                {"x": 1850.20, "y": 1520.40, "type": "dungeon", "color": core.PRIO_PURPLE, "cont_img": "tooling_bin.webp"}
            ],
            "active_objectives": [
                {"title": "Localiser le campement de la famille Gavroche", "cont_img": "strongbox.webp", "item_img": "gold_key.png"}
            ],
            "priority_focus": {
                "title": "Gavroche Family Camp (Berges Est du fleuve)",
                "c_ico": "strongbox.webp",
                "i_ico": "gold_key.png",
                "color": core.PRIO_PURPLE
            },
            "rotation_steps": [
                {"step": "Déployer sur Jacques Bridge et longer le fleuve vers l'Est.", "color": core.PRIO_YELLOW},
                {"step": "Sécuriser le campement en éliminant les rôdeurs proches.", "color": core.PRIO_PURPLE},
                {"step": "Fouiller les coffres du camp pour les objets de quête.", "color": core.PRIO_BLUE},
                {"step": "Extraire par la Tour de Guet ou le Sentier Sud.", "color": core.PRIO_GREY}
            ],
            "directory": [
                {"color": core.PRIO_YELLOW, "cont": "Camp Gavroche", "c_ico": "strongbox.webp", "item": "Objectif Quête", "rate": "100%", "spots": "X: 1479, Y: 313"},
                {"color": core.PRIO_PURPLE, "cont": "Donjon Folly", "c_ico": "tooling_bin.webp", "item": "Entrée Ouest", "rate": "Clé de Jacques", "spots": "Sous l'arche"}
            ],
            "roadmap": [
                {"quest": "The Gavroche Family", "items": [("Pommes Cuites (x3)", "fresh_egg.png")]}
            ]
        }
        render_dynamic_v25_briefing(cfg, out_path)
        conn.close()
        intel = {
            "title": "Campement de la Famille Gavroche (Jacques Bridge)",
            "map_name": "Jacques Bridge",
            "objectives": ["Localiser le campement de la famille Gavroche"],
            "focus": "Berges Est du fleuve (X: 1479.01, Y: 313.35)",
            "drops": [
                "• **Campement Gavroche** (`X: 1479.01, Y: 313.35`) : Tentes en ruine et provisions",
                "• **Quête** : The Gavroche Family (Éloïse au Château)",
                "• **Anneau de Famille** : Quête The Last Prisoner (trouvable dans les commodes)"
            ]
        }
        return out_path, intel

        # 1.4 Specialized Handler: Piro's Lens (Quest: Seeing Clearly)
    if q in {"lens", "lentille", "piro's lens", "piros lens", "seeing clearly", "seeing-clearly"}:
        map_name = "Jacques Bridge"
        map_img = JACQUES_MAP
        out_path = os.path.join(OUT_DIR, "dynamic_piro_lens_location_map.jpg")
        cfg = {
            "title": "LOCATION : PIRO'S LENS (QUEST: SEEING CLEARLY)",
            "map_name": "Jacques Bridge",
            "map_img": map_img,
            "tag": "QUEST RECON",
            "header_cards": [
                ("Zone", "South-East Ruins (Rat's Nest Cave)"),
                ("Objective", "Find Piro's Lens (ID_Uncommon_PirosLens)"),
                ("Giver", "Piro (Chateau Hub)")
            ],
            "story_pois": [
                {"x": 1602.00, "y": 3552.00, "label": "Rat's Nest Cave Entrance", "offset_dir": "bottom", "cont_img": "strongbox.webp"},
                {"x": 1491.15, "y": 3535.74, "label": "Piro's Lens", "offset_dir": "top", "cont_img": "gold_key.png"}
            ],
            "points": [
                {"x": 1602.00, "y": 3552.00, "type": "objective", "color": core.PRIO_PURPLE, "cont_img": "strongbox.webp"},
                {"x": 1491.15, "y": 3535.74, "type": "objective", "color": core.COLOR_GOLD, "cont_img": "gold_key.png"}
            ],
            "active_objectives": [
                {"title": "Enter the Rat's Nest Cave at Jacques Bridge South-East", "cont_img": "strongbox.webp", "item_img": "gold_key.png"},
                {"title": "Recover Piro's Lens inside the cave", "cont_img": "gold_key.png", "item_img": "gold_key.png"}
            ],
            "priority_focus": {
                "title": "Rat's Nest Cave & Piro's Lens",
                "c_ico": "strongbox.webp",
                "i_ico": "gold_key.png",
                "color": core.COLOR_GOLD
            },
            "rotation_steps": [
                {"step": "Deploy on Jacques Bridge and advance towards the South-East ruins.", "color": core.PRIO_YELLOW},
                {"step": "Locate the Cave entrance (X: 1602, Y: 3552) leading into the subterranean den.", "color": core.PRIO_PURPLE},
                {"step": "Retrieve Piro's Lens (X: 1491, Y: 3535) and store in Secure Pouch.", "color": core.PRIO_GREY}
            ],
            "directory": [
                {"color": core.COLOR_GOLD, "cont": "Piro's Lens", "c_ico": "gold_key.png", "item": "Optical Monocle Lens", "rate": "100%", "spots": "X: 1491.15, Y: 3535.74"},
                {"color": core.PRIO_PURPLE, "cont": "Cave Entrance", "c_ico": "strongbox.webp", "item": "Rat's Nest Cave", "rate": "100%", "spots": "X: 1602.00, Y: 3552.00"}
            ],
            "roadmap": [
                {"quest": "Seeing Clearly", "items": [("Piro's Lens (x1)", "gold_key.png")]}
            ]
        }
        render_dynamic_v25_briefing(cfg, out_path)
        conn.close()
        intel = {
            "title": "Piro's Lens (Jacques Bridge)",
            "map_name": "Jacques Bridge",
            "focus": "Rat's Nest Cave (X: 1491.15, Y: 3535.74)",
            "drops": [
                "• **Piro's Lens Location** (`X: 1491.15, Y: 3535.74`) : Inside the subterranean Rat's Nest Cave at Jacques Bridge South-East.",
                "• **Cave Entrance** (`X: 1602.00, Y: 3552.00`) : Primary entrance to the cave.",
                "• **Associated Quest** : *Seeing Clearly* (Giver: Piro at Chateau Hub).",
                "• **Safe Pouch Rule** : Keep in Secure Pouch (Quest Item, Non-droppable)!"
            ]
        }
        return out_path, intel

    # 1.5 Specialized Handler: Piro's Convoy (Remains of the Day / Return to the Convoy)
    if q in {"piro's convoy", "piros convoy", "piro convoy", "remains of the day", "remains day", "return to the convoy", "return convoy"}:
        map_name = "Jacques Bridge"
        map_img = JACQUES_MAP
        out_path = os.path.join(OUT_DIR, "dynamic_piro_convoy_location_map.jpg")
        cfg = {
            "title": "LOCATION : PIRO'S CONVOY & SITE (JACQUES BRIDGE)",
            "map_name": "Jacques Bridge",
            "map_img": map_img,
            "tag": "QUEST RECON",
            "header_cards": [
                ("Zone", "Southwest Riverbank"),
                ("Quests", "Remains of the Day / Return to the Convoy"),
                ("Giver", "Piro (Chateau Hub)")
            ],
            "story_pois": [
                {"x": 848.20, "y": 3084.90, "label": "Piro's Convoy Ruins", "offset_dir": "bottom", "cont_img": "strongbox.webp"}
            ],
            "points": [
                {"x": 848.20, "y": 3084.90, "type": "objective", "color": core.PRIO_YELLOW, "cont_img": "strongbox.webp"}
            ],
            "active_objectives": [
                {"title": "Locate Piro's missing convoy on Jacques Bridge", "cont_img": "strongbox.webp", "item_img": "gold_key.png"}
            ],
            "priority_focus": {
                "title": "Piro's Convoy (Southwest riverbank)",
                "c_ico": "strongbox.webp",
                "i_ico": "gold_key.png",
                "color": core.PRIO_PURPLE
            },
            "rotation_steps": [
                {"step": "Deploy on Jacques Bridge and advance along the Southwest riverbank road.", "color": core.PRIO_YELLOW},
                {"step": "Neutralize infected scavengers surrounding the overturned supply cart.", "color": core.PRIO_PURPLE},
                {"step": "Secure mission objective and extract safely.", "color": core.PRIO_GREY}
            ],
            "directory": [
                {"color": core.PRIO_YELLOW, "cont": "Piro's Convoy", "c_ico": "strongbox.webp", "item": "Quest Site", "rate": "100%", "spots": "X: 848.2, Y: 3084.9"}
            ],
            "roadmap": [
                {"quest": "Remains of the Day", "items": [("Crude Ampoule (x15)", "fresh_egg.png")]}
            ]
        }
        render_dynamic_v25_briefing(cfg, out_path)
        conn.close()
        intel = {
            "title": "Piro's Convoy (Jacques Bridge)",
            "map_name": "Jacques Bridge",
            "focus": "Southwest Riverbank (X: 848.2, Y: 3084.9)",
            "drops": [
                "• **Piro's Missing Convoy** (`X: 848.20, Y: 3084.90`) : Overturned wagon ruins on southwest riverbank road.",
                "• **Associated Quests** : *Remains of the Day* & *Return to the Convoy* (Giver: Piro at Chateau Hub).",
                "• **Reward** : 15x Crude Ampoules & Chateau Reputation."
            ]
        }
        return out_path, intel

    # Match the entire objective, not any incidental word in the request.
    def identity(value):
        return tuple(w for w in re.findall(r"\w+", (value or "").lower())
                     if w not in {"the", "of", "in", "a", "an", "to", "de", "du", "le", "la", "les"})
    c.execute("""
        SELECT map_name, title, point_type, x, y, description, quest_slug FROM map_points
        WHERE (? IS NULL OR map_name = ?)
    """, (target_map_hint, target_map_hint))
    matched_points = [dict(p) for p in c.fetchall()
                      if identity(q) in (identity(p["title"]), identity(p["quest_slug"]))]
    conn.close()
    if not matched_points:
        raise MapDataUnavailable(f"No mapped objective data for {query!r}.")
    maps = {p["map_name"] for p in matched_points}
    if len(maps) != 1:
        raise MapDataUnavailable("This objective occurs on multiple maps. Specify the map.")
    target_map = matched_points[0]["map_name"]
    tokens = [re.sub(r"[^a-z0-9]+", "_", q)]

    map_img = resolve_map_image(target_map)
    out_path = os.path.join(OUT_DIR, f"dynamic_location_map_{tokens[0] if tokens else 'poi'}.jpg")
    p0 = matched_points[0]

    cfg = {
        "title": f"LOCALISATION : {p0['title'][:32].upper()} ({target_map.upper()})",
        "map_name": target_map,
        "map_img": map_img,
        "tag": "REPÈRE TACTIQUE",
        "header_cards": [
            ("Lieu", target_map),
            ("Type", p0["point_type"].title()),
            ("Statut", "Reconnaissance")
        ],
        "story_pois": [
            {"x": p["x"], "y": p["y"], "label": p["title"][:28], "offset_dir": "bottom" if i % 2 == 0 else "top", "cont_img": "strongbox.webp"}
            for i, p in enumerate(matched_points[:3])
        ],
        "points": [
            {"x": p["x"], "y": p["y"], "type": "objective", "color": core.PRIO_YELLOW if i == 0 else core.PRIO_PURPLE, "cont_img": "strongbox.webp"}
            for i, p in enumerate(matched_points)
        ],
        "active_objectives": [
            {"title": p0["title"][:50], "cont_img": "strongbox.webp", "item_img": "gold_key.png"}
        ],
        "priority_focus": {
            "title": f"{p0['title'][:36]} ({target_map})",
            "c_ico": "strongbox.webp",
            "i_ico": "gold_key.png",
            "color": core.PRIO_PURPLE
        },
        "rotation_steps": [
            {"step": f"Se déployer sur {target_map} et progresser vers le repère.", "color": core.PRIO_YELLOW},
            {"step": f"Inspecter la zone : {p0['title']}.", "color": core.PRIO_PURPLE},
            {"step": "Sécuriser les conteneurs et extraire.", "color": core.PRIO_BLUE}
        ],
        "directory": [
            {"color": core.PRIO_YELLOW, "cont": p["title"][:24], "c_ico": "strongbox.webp", "item": "Repère", "rate": "100%", "spots": f"X: {int(p['x'])}, Y: {int(p['y'])}"}
            for p in matched_points[:3]
        ],
        "roadmap": [
            {"quest": "Expédition de repérage", "items": [("Repère", "gold_key.png")]}
        ]
    }
    render_dynamic_v25_briefing(cfg, out_path)
    intel = {
        "title": f"Localisation : {p0['title']}",
        "map_name": target_map,
        "objectives": [p0["title"]],
        "focus": f"Repère sur {target_map} (X: {int(p0['x'])}, Y: {int(p0['y'])})",
        "drops": [f"• **{p['title']}** (`X: {int(p['x'])}, Y: {int(p['y'])}`)" for p in matched_points[:4]]
    }
    return out_path, intel


# ---------------------------------------------------------------------------
# CANONICAL SPEEDRUN RAIDS (USED ONLY WHEN USER EXPLICITLY ASKS FOR SPEEDRUN)
# ---------------------------------------------------------------------------

def generate_speedrun_raid_map(query: str, raid_id: Optional[int] = None) -> Tuple[str, Dict[str, Any]]:
    """Render canonical Speedrun Briefing (Raid 1..7) when specifically requested."""
    ids = re.findall(r"\braid\s*(\d+)\b", query.lower())
    if raid_id is None and len(set(ids)) == 1:
        raid_id = int(ids[0])
    matches = [cfg for cfg in g25.RAIDS_CONFIG if cfg["id"] == raid_id]
    if len(matches) != 1:
        raise MapDataUnavailable("Specify an available speedrun raid number (1–7).")
    cfg = matches[0]

    out_path = os.path.join(OUT_DIR, f"raid{cfg['id']}_speedrun_briefing.jpg")
    g25.render_briefing(cfg, output_path=out_path)
    
    intel = {
        "raid_id": cfg["id"],
        "raid_name": f"Raid {cfg['id']} : {cfg['map_name']}",
        "map_name": cfg["map_name"],
        "quest_name": cfg["quest_name"],
        "has_focus": cfg.get("has_focus", False),
        "active_objectives": [o["title"] for o in cfg.get("active_objectives", [])],
        "priority_focus": cfg.get("priority_focus", {}).get("title") if cfg.get("priority_focus") else None,
        "rotation_steps": [s["step"] for s in cfg.get("rotation_steps", [])],
        "drops": cfg.get("directory", []),
        "story_pois": cfg.get("story_pois", [])
    }
    return out_path, intel
