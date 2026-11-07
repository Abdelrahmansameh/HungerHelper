import os

ENGINE_PATH = "universal_v8_engine.py"

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

lore_card_code = '''

# ===========================================================================
# 16. CANONICAL LORE & WORLDBUILDING ARCHIVE CARDS
# ===========================================================================
def render_lore_card(topic_slug: str) -> str:
    """Render high-resolution historical lore card for worldbuilding queries."""
    from co_pilot.lore_engine import LORE_DATABASE
    
    matched = None
    for k, v in LORE_DATABASE.items():
        if v["slug"] == topic_slug or k in topic_slug:
            matched = v
            break
            
    if not matched:
        matched = LORE_DATABASE["the_hunger"]

    title = matched["title_en"]
    category = matched["category"]
    body = matched["lore_en"]
    tactical = matched["tactical_en"]
    slug = matched["slug"]

    canvas, draw = create_base_canvas(f"LORE ARCHIVE : {title.upper()}", tag="HISTORICAL DOSSIER", border_col=core.COLOR_GOLD)
    CARD_W, CARD_H = canvas.size

    # Left: Portrait or Emblem
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    # Portrait detection
    portrait_p = None
    if "marie" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "marie.webp")
    elif "otto" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "otto.webp")
    elif "eva" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "eva.webp")
    elif "hugo" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "hugo.webp")
    elif "eloise" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "eloise_avatar_clean.png")
    elif "dreg" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "creatures", "dreg_farmer.png")
    else: portrait_p = os.path.join(ROOT_DIR, "assets", "eloise_avatar_clean.png")

    if portrait_p and os.path.exists(portrait_p):
        try:
            p_img = Image.open(portrait_p).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(p_img, (left_box[0] + 36, left_box[1] + 30), p_img)
        except Exception:
            pass

    draw.rounded_rectangle([left_box[0] + 20, left_box[3] - 110, left_box[2] - 20, left_box[3] - 68],
                           radius=6, fill=(24, 20, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 30, left_box[3] - 100), f"CLASS : {category.upper()}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 30, left_box[3] - 50), "CHATEAU OFFICIAL ARCHIVES", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    # Box 1: Canonical Chronicle
    b1 = [rx, 86, rx + rw, 360]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "CANONICAL WORLD CHRONICLE", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    
    # Word wrap body lines cleanly
    words = body.replace("**", "").split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 55:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))

    ly = b1[1] + 54
    for line in lines[:8]:
        draw.text((b1[0] + 20, ly), line, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ly += 26

    # Box 2: Tactical Relevance
    b2 = [rx, 376, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(24, 20, 16), outline=(90, 70, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TACTICAL GAMEPLAY CONNECTION", fill=(255, 215, 0), font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 52), tactical[:130], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"lore_card_{slug}.jpg")
'''

with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(text + lore_card_code)

print("Added render_lore_card to universal_v8_engine.py successfully.")
