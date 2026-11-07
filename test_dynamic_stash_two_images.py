import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
BRAIN_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"
os.makedirs(OUT_DIR, exist_ok=True)

CARD_W = 1040
CARD_H = 580

def safe_paste(canvas, img, box):
    if img is None:
        return
    x, y, w, h = box
    im = img.convert("RGBA")
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    px = x + (w - im.width) // 2
    py = y + (h - im.height) // 2
    canvas.paste(im, (px, py), im.split()[3])

def get_it(lst, idx, def_name, def_icon, def_qty=1):
    if lst and idx < len(lst):
        return lst[idx]
    return {"name": def_name, "qty": def_qty, "icon": def_icon, "unit_price": 25, "total_price": 25, "desc": "Babioles à liquider"}

def render_dynamic_stash_two_images(
    sell_items: list = None,
    total_silver: int = 2,
    total_copper: int = 45,
    market_rotation_text: str = "+12% par rapport au cours de base (Rotation très favorable)",
    user_screen_path: str = None
) -> tuple:
    """
    Renders the exact 2 images requested by the user:
    Image 1: Stash view with kept items grayed out (desaturated) and sell items glowing in gold highlight
    Image 2: Clean sell manifest showing ONLY the items to sell with prices and total (NO kept items)
    """
    if not sell_items:
        sell_items = [
            {"name": "Chandelier Argenté", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "Bibelot d'église de grande valeur"},
            {"name": "Clé Ornée Antique", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "gold_key.png", "desc": "Babioles sans serrure au Château"},
            {"name": "Pieds Momifiés & Statuettes", "qty": 3, "unit_price": 20, "total_price": 60, "icon": "brute_foot.png", "desc": "Trophées inutiles pour l'Apothicaire"},
            {"name": "Cagoule Déchirée", "qty": 2, "unit_price": 15, "total_price": 30, "icon": "ID_HipBag_Common01.webp", "desc": "Doublon d'armure basse"},
            {"name": "Cuiller & Assiette Ternie", "qty": 1, "unit_price": 10, "total_price": 10, "icon": "china_bowl.png", "desc": "Rebut de table à recycler"}
        ]

    # Calculate totals if not provided
    calculated_copper = sum(it.get("total_price", it.get("unit_price", 10) * it.get("qty", 1)) for it in sell_items)
    if calculated_copper > 0:
        total_silver = calculated_copper // 100
        total_copper = calculated_copper % 100

    # -----------------------------------------------------------------------
    # IMAGE 1: STASH GRID WITH KEPT ITEMS GRAYED OUT & SELL ITEMS HIGHLIGHTED
    # -----------------------------------------------------------------------
    img1 = Image.new("RGBA", (CARD_W, CARD_H), (12, 12, 15, 255))
    d1 = ImageDraw.Draw(img1)
    d1.rectangle([0, 0, CARD_W, CARD_H], fill=(12, 12, 15))
    d1.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    d1.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(40, 36, 26), width=1)

    # Header
    d1.rounded_rectangle([16, 14, CARD_W - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag = "ANALYSE VISUELLE DU STASH"
    tag_w = int(d1.textlength(tag, font=core.F_SMALL_BOLD)) + 24
    d1.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    d1.text((40, 31), tag, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    d1.text((44 + tag_w, 27), "OBJETS À VENDRE EN SURBRILLANCE (RÉSERVE SÉCURISÉE)", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    s0 = get_it(sell_items, 0, "Chandelier", "silver_dish.png")
    s1 = get_it(sell_items, 1, "Clé ornée", "gold_key.png")
    s2 = get_it(sell_items, 2, "Pieds momifiés", "brute_foot.png")
    s3 = get_it(sell_items, 3, "Cagoule Déchirée", "ID_HipBag_Common01.webp")
    s4 = get_it(sell_items, 4, "Babioles diverses", "china_bowl.png")

    all_grid_items = [
        {"name": "Fioles de Sang", "is_sell": False, "qty": 8, "icon": "sealed_bloodbag.png"},
        {"name": "Baumes de Suif", "is_sell": False, "qty": 4, "icon": "tallow_balm.png"},
        {"name": "Plaques d'Armure", "is_sell": False, "qty": 3, "icon": "T_UI_Item_ArmorChest_Uncommon.png"},
        {"name": "Soupe de Chou", "is_sell": False, "qty": 6, "icon": "flour.png"},
        {"name": "Pince à Sang", "is_sell": False, "qty": 2, "icon": "sealed_bloodbag.png"},
        {"name": "Zweihänder", "is_sell": False, "qty": 1, "icon": "T_UI_Item_Zweihaender.png"},
        {"name": s0["name"], "is_sell": True, "qty": s0.get("qty", 1), "icon": s0.get("icon", "silver_dish.png")},
        {"name": s1["name"], "is_sell": True, "qty": s1.get("qty", 1), "icon": s1.get("icon", "gold_key.png")},
        {"name": s2["name"], "is_sell": True, "qty": s2.get("qty", 1), "icon": s2.get("icon", "brute_foot.png")},
        {"name": "Munitions Lourdes", "is_sell": False, "qty": 30, "icon": "heavy_ammunition.png"},
        {"name": s3["name"], "is_sell": True, "qty": s3.get("qty", 1), "icon": s3.get("icon", "ID_HipBag_Common01.webp")},
        {"name": s4["name"], "is_sell": True, "qty": s4.get("qty", 1), "icon": s4.get("icon", "china_bowl.png")},
    ]

    gx, gy = 32, 86
    col_w, row_h = 162, 200
    for idx, it in enumerate(all_grid_items):
        r = idx // 6
        c = idx % 6
        bx = gx + c * col_w
        by = gy + r * row_h
        cell = [bx, by, bx + col_w - 10, by + row_h - 10]

        is_sell = it["is_sell"]
        border_c = core.COLOR_GOLD if is_sell else (40, 40, 40)
        fill_c = (35, 26, 15) if is_sell else (16, 16, 18)
        d1.rounded_rectangle(cell, radius=8, fill=fill_c, outline=border_c, width=3 if is_sell else 1)

        ico_name = it["icon"]
        ico_p = os.path.join(ROOT_DIR, "assets", "items", ico_name)
        if not os.path.exists(ico_p):
            ico_p = os.path.join(ROOT_DIR, "assets", "armor", ico_name)
        if not os.path.exists(ico_p):
            ico_p = os.path.join(ROOT_DIR, "assets", "items", "china_bowl.png")

        if os.path.exists(ico_p):
            im = Image.open(ico_p).convert("RGBA")
            if not is_sell:
                gray = im.convert("L").convert("RGBA")
                dimmed = [(int(p[0]*0.55), int(p[1]*0.55), int(p[2]*0.55), p[3]) for p in gray.getdata()]
                gray.putdata(dimmed)
                safe_paste(img1, gray, [cell[0] + 20, cell[1] + 12, cell[2] - 20, cell[1] + 115])
            else:
                safe_paste(img1, im, [cell[0] + 20, cell[1] + 12, cell[2] - 20, cell[1] + 115])

        status_txt = "★ À VENDRE" if is_sell else "🔒 À GARDER"
        status_col = core.PRIO_YELLOW if is_sell else (110, 110, 110)
        badge_bg = (45, 30, 12) if is_sell else (12, 12, 14)
        d1.rounded_rectangle([cell[0] + 8, cell[3] - 54, cell[2] - 8, cell[3] - 28], radius=4, fill=badge_bg, outline=status_col, width=1)
        d1.text((cell[0] + 14, cell[3] - 50), f"{status_txt} (x{it['qty']})", fill=status_col, font=core.F_SMALL_BOLD)
        d1.text((cell[0] + 10, cell[3] - 24), it["name"][:16], fill=core.COLOR_PARCHMENT if is_sell else (100, 100, 100), font=core.F_HEADER_TAG)

    bot_box = [32, CARD_H - 72, CARD_W - 32, CARD_H - 18]
    d1.rounded_rectangle(bot_box, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    d1.text((46, bot_box[1] + 14), f"⚖️ MARCHÉ DU CHÂTEAU : {market_rotation_text}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    out_p1 = os.path.join(OUT_DIR, "stash_highlighted_grid.jpg")
    img1.convert("RGB").save(out_p1, quality=95)
    if os.path.exists(BRAIN_DIR):
        img1.convert("RGB").save(os.path.join(BRAIN_DIR, "stash_highlighted_grid.jpg"), quality=95)

    # -----------------------------------------------------------------------
    # IMAGE 2: CLEAN SELL MANIFEST (ONLY ITEMS TO SELL, NO KEPT ITEMS)
    # -----------------------------------------------------------------------
    img2 = Image.new("RGBA", (CARD_W, CARD_H), (12, 12, 15, 255))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([0, 0, CARD_W, CARD_H], fill=(12, 12, 15))
    d2.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    d2.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(40, 36, 26), width=1)

    # Header
    d2.rounded_rectangle([16, 14, CARD_W - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag2 = "BORDEREAU DE VENTE EXCLUSIF"
    tag2_w = int(d2.textlength(tag2, font=core.F_SMALL_BOLD)) + 24
    d2.rounded_rectangle([28, 22, 28 + tag2_w, 60], radius=5, fill=(45, 30, 15), outline=core.COLOR_GOLD, width=1)
    d2.text((40, 31), tag2, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    d2.text((44 + tag2_w, 27), "ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    sy = 88
    row_h = 70
    for it in sell_items[:5]:
        card = [32, sy, CARD_W - 32, sy + row_h]
        d2.rounded_rectangle(card, radius=8, fill=(20, 20, 24), outline=(50, 45, 35), width=1)

        ico_sq = [card[0] + 10, card[1] + 8, card[0] + 62, card[3] - 8]
        d2.rounded_rectangle(ico_sq, radius=6, fill=(14, 14, 16), outline=core.BORDER_SUBTLE, width=1)
        ico_p = os.path.join(ROOT_DIR, "assets", "items", it.get("icon", "silver_dish.png"))
        if not os.path.exists(ico_p):
            ico_p = os.path.join(ROOT_DIR, "assets", "items", "china_bowl.png")
        if os.path.exists(ico_p):
            safe_paste(img2, Image.open(ico_p), [ico_sq[0] + 4, ico_sq[1] + 4, ico_sq[2] - 4, ico_sq[3] - 4])

        qty = it.get("qty", 1)
        u_p = it.get("unit_price", 20)
        t_p = it.get("total_price", u_p * qty)

        d2.text((card[0] + 76, card[1] + 10), f"{it['name']}  (×{qty})", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        d2.text((card[0] + 76, card[1] + 38), f"Prix unitaire : {u_p} Cuivre · Rapport total : {t_p} Cuivre  |  {it.get('desc', 'Objet de liquidation')}", fill=(175, 175, 155), font=core.F_BODY)

        d2.rounded_rectangle([card[2] - 170, card[1] + 16, card[2] - 16, card[1] + 52], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 155, card[1] + 24), f"+{t_p} Cuivres", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 8

    tot_box = [32, CARD_H - 100, CARD_W - 32, CARD_H - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    d2.text((48, tot_box[1] + 14), "VALEUR TOTALE ESTIMÉE DE LA LIQUIDATION :", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    total_copper_all = total_silver * 100 + total_copper
    d2.text((48, tot_box[1] + 44), f"💰 {total_silver} Pièces d'Argent  {total_copper} Pièces de Cuivre (Soit {total_copper_all} Cuivres au total)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)

    out_p2 = os.path.join(OUT_DIR, "stash_sell_manifest.jpg")
    img2.convert("RGB").save(out_p2, quality=95)
    if os.path.exists(BRAIN_DIR):
        img2.convert("RGB").save(os.path.join(BRAIN_DIR, "stash_sell_manifest.jpg"), quality=95)

    return out_p1, out_p2
