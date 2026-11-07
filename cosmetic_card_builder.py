import os
import sys
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, "assets", "items"), exist_ok=True)
os.makedirs(os.path.join(ROOT_DIR, "assets", "skins"), exist_ok=True)

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

def get_or_download_asset(rel_url, local_path):
    if os.path.exists(local_path):
        return local_path
    if not rel_url:
        return None
    full_url = rel_url if rel_url.startswith("http") else f"https://hunger-companion.com{rel_url}"
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            with open(local_path, "wb") as f:
                f.write(data)
            return local_path
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
        return None

def render_cosmetic_craft_card_dynamic(skin_info: dict, requested_ingredient: str = "") -> str:
    skin_name = skin_info.get("name", "Cosmetic Skin")
    target_name = skin_info.get("target", "Arme / Héros")
    rarity = skin_info.get("rarity", "Epic")
    lore_text = skin_info.get("lore") or f"Pièce d'apparence confectionnée à l'Atelier du Château pour {target_name}."
    schema_info = skin_info.get("fee", "Atelier du Château")
    if "schema" not in schema_info.lower() and "cuivre" not in schema_info.lower():
        schema_info = f"Atelier du Tailleur · {schema_info}"

    # Download skin preview if needed
    skin_img_rel = skin_info.get("img_url", "")
    skin_local_fn = os.path.basename(skin_img_rel.split("?")[0]) if skin_img_rel else "skin_default.webp"
    skin_local_p = os.path.join(ROOT_DIR, "assets", "skins", skin_local_fn)
    get_or_download_asset(skin_img_rel, skin_local_p)

    # Process materials (up to 5)
    materials = skin_info.get("materials", [])
    processed_mats = []
    for m in materials[:5]:
        mat_name = m.get("name", "Matériau")
        mat_qty = m.get("qty", "1")
        mat_img_rel = m.get("img_url", "")
        mat_fn = os.path.basename(mat_img_rel.split("?")[0]) if mat_img_rel else f"{mat_name.lower().replace(' ', '_')}.png"
        mat_local_p = os.path.join(ROOT_DIR, "assets", "items", mat_fn)
        get_or_download_asset(mat_img_rel, mat_local_p)

        is_highlight = bool(requested_ingredient and requested_ingredient.lower() in mat_name.lower())
        processed_mats.append({
            "name": mat_name,
            "qty": mat_qty,
            "icon_p": mat_local_p,
            "highlight": is_highlight
        })

    canvas = Image.new("RGBA", (CARD_W, CARD_H), (12, 12, 15))
    draw = ImageDraw.Draw(canvas)

    # Border
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(12, 12, 15))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(40, 36, 26), width=1)

    # Header Banner
    header_box = [16, 14, CARD_W - 16, 68]
    draw.rounded_rectangle(header_box, radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)

    tag = "ATELIER D'ARTISANAT & TAILLEUR"
    tag_w = int(draw.textlength(tag, font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(45, 20, 50), outline=core.PRIO_PURPLE, width=1)
    draw.text((40, 31), tag, fill=(240, 190, 255), font=core.F_SMALL_BOLD)

    title = f"COSMÉTIQUE : {skin_name.upper()} ({target_name.upper()})"
    draw.text((44 + tag_w, 27), title, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    wm = "HUNGER COMPANION x ELOISE"
    draw.text((CARD_W - int(draw.textlength(wm, font=core.F_SMALL_BOLD)) - 28, 31), wm, fill=(120, 110, 80), font=core.F_SMALL_BOLD)

    # LEFT PANEL: Skin Identity & 3D Render
    left_box = [28, 86, 390, CARD_H - 24]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.PRIO_PURPLE, width=2)

    # 3D Skin preview pedestal
    img_box = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(img_box, radius=8, fill=(18, 16, 22), outline=core.BORDER_SUBTLE, width=1)

    if os.path.exists(skin_local_p):
        try:
            skin_img = Image.open(skin_local_p)
            safe_paste(canvas, skin_img, (img_box[0] + 10, img_box[1] + 10, img_box[2] - img_box[0] - 20, img_box[3] - img_box[1] - 20))
        except Exception:
            pass

    # Rarity badge
    r_lower = rarity.lower()
    r_color = (
        core.COLOR_GOLD if "legend" in r_lower else
        core.PRIO_PURPLE if "epic" in r_lower else
        (70, 140, 240) if "rare" in r_lower else
        core.PRIO_YELLOW if "uncommon" in r_lower else
        (160, 160, 160)
    )
    draw.rounded_rectangle([img_box[0] + 10, img_box[1] + 10, img_box[0] + 95, img_box[1] + 34], radius=4, fill=(25, 10, 30), outline=r_color, width=1)
    draw.text((img_box[0] + 16, img_box[1] + 14), rarity.upper(), fill=r_color, font=core.F_SMALL_BOLD)

    # Meshswap tag
    draw.rounded_rectangle([img_box[2] - 120, img_box[1] + 10, img_box[2] - 10, img_box[1] + 34], radius=4, fill=(15, 20, 25), outline=(60, 90, 140), width=1)
    draw.text((img_box[2] - 114, img_box[1] + 14), "NOUVEAU MODÈLE", fill=(160, 200, 255), font=core.F_HEADER_TAG)

    # Details below image
    ty = img_box[3] + 14
    draw.text((left_box[0] + 16, ty), skin_name[:26], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    ty += 28
    draw.text((left_box[0] + 16, ty), f"Objet support : {target_name}", fill=(180, 180, 160), font=core.F_BODY)
    ty += 24
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 32], radius=6, fill=(25, 22, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 24, ty + 6), f"⚙️ {schema_info[:32]}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    ty += 42

    # Lore text quote
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, left_box[3] - 14], radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    draw.text((left_box[0] + 20, ty + 8), f"« {lore_text[:110]} »", fill=(190, 185, 170), font=core.F_HEADER_TAG)

    # RIGHT PANEL: Ingredients & Visual Cards
    right_box = [408, 86, CARD_W - 28, CARD_H - 24]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 16), "INGRÉDIENTS DE FABRICATION COSMÉTIQUE (RECETTE OFFICIELLE)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((right_box[0] + 20, right_box[1] + 42), "Tous ces composants doivent être réunis dans votre Stash pour assembler le skin.", fill=(160, 160, 140), font=core.F_BODY)

    start_y = right_box[1] + 74
    row_h = 66
    for i, ing in enumerate(processed_mats):
        iy = start_y + i * (row_h + 8)
        ibox = [right_box[0] + 18, iy, right_box[2] - 18, iy + row_h]

        is_hl = ing["highlight"]
        bg_col = (35, 20, 40) if is_hl else (20, 20, 24)
        border_col = core.COLOR_GOLD if is_hl else (45, 45, 40)
        draw.rounded_rectangle(ibox, radius=8, fill=bg_col, outline=border_col, width=2 if is_hl else 1)

        # Icon square
        icon_sq = [ibox[0] + 8, ibox[1] + 6, ibox[0] + 58, ibox[3] - 6]
        draw.rounded_rectangle(icon_sq, radius=6, fill=(14, 14, 16), outline=core.BORDER_SUBTLE, width=1)
        if os.path.exists(ing["icon_p"]):
            try:
                ico = Image.open(ing["icon_p"])
                safe_paste(canvas, ico, (icon_sq[0] + 3, icon_sq[1] + 3, 44, 44))
            except Exception:
                pass

        # Quantity badge
        qty_w = int(draw.textlength(f"×{ing['qty']}", font=core.F_SMALL_BOLD)) + 6
        draw.rounded_rectangle([icon_sq[2] - qty_w, icon_sq[3] - 16, icon_sq[2], icon_sq[3]], radius=2, fill=(10, 10, 10), outline=core.COLOR_GOLD, width=1)
        draw.text((icon_sq[2] - qty_w + 3, icon_sq[3] - 15), f"×{ing['qty']}", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

        # Text
        draw.text((ibox[0] + 70, ibox[1] + 10), ing["name"], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        draw.text((ibox[0] + 70, ibox[1] + 34), "Composant de pillage & artisanat de raid", fill=(170, 170, 150), font=core.F_BODY)

        if is_hl:
            draw.rounded_rectangle([ibox[2] - 170, ibox[1] + 16, ibox[2] - 14, ibox[1] + 48], radius=5, fill=(50, 30, 60), outline=core.COLOR_GOLD, width=1)
            draw.text((ibox[2] - 160, ibox[1] + 24), "★ OBJET RECHERCHÉ", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        else:
            draw.text((ibox[2] - 130, ibox[1] + 24), f"{ing['qty']}x Requis", fill=(140, 140, 130), font=core.F_SMALL_BOLD)

    # Bottom guidance
    note_box = [right_box[0] + 18, start_y + len(processed_mats) * (row_h + 8) + 4, right_box[2] - 18, right_box[3] - 14]
    draw.rounded_rectangle(note_box, radius=8, fill=(18, 18, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((note_box[0] + 16, note_box[1] + 8), "💡 Conseil Éloïse : Conservez impérativement ces composants dans votre Stash au Château.", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((note_box[0] + 16, note_box[1] + 28), "Ne les vendez jamais aux marchands ambulants avant d'avoir assemblé le skin !", fill=(180, 180, 160), font=core.F_BODY)

    slug = skin_name.lower().replace(" ", "_").replace("'", "")
    out_p = os.path.join(OUT_DIR, f"cosmetic_craft_{slug}.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    return out_p
