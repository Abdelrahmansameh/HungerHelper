import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)

CARD_W = 1200
CARD_H = 720

def safe_paste(canvas, img, box):
    if img is None:
        return
    x, y, w, h = box
    im = img.convert("RGBA")
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    px = x + (w - im.width) // 2
    py = y + (h - im.height) // 2
    canvas.paste(im, (px, py), im.split()[3])

def render_build_all_trees_view(
    player_name: str = "Abdallah",
    level: int = 100,
    spent_points: int = 91,
    cunning_pts: int = 0,
    phys_pts: int = 18,
    surv_pts: int = 36,
    martial_pts: int = 0,
    arms_pts: int = 37,
    highlighted_talents: list = None
) -> str:
    """
    Renders Image 1 of Mastery Trees:
    - Clean Hunger Companion layout with all 5 tree headers (Cunning, Physiology, Survival, Martial, Arms)
    - Tree progression numbers and points spent
    - The 3 active trees (Physiology 18, Survival 36, Arms 37) displayed with allocated talents glowing
    - NO 'Synthèse' or 'Verdict' text!
    """
    canvas = Image.new("RGBA", (CARD_W, CARD_H), (10, 10, 12, 255))
    draw = ImageDraw.Draw(canvas)

    # Ambient border
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(10, 10, 12))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(35, 32, 24), width=1)

    # Top Navigation Tabs (Hunger Companion style)
    # Cunning, Physiology, Survival, Martial, Arms
    tabs = [
        ("CUNNING", f"{cunning_pts}/72", (220, 200, 140), cunning_pts > 0),
        ("PHYSIOLOGY", f"{phys_pts}/83", (255, 170, 190), phys_pts > 0),
        ("SURVIVAL", f"{surv_pts}/78", (215, 185, 255), surv_pts > 0),
        ("MARTIAL", f"{martial_pts}/74", (170, 220, 255), martial_pts > 0),
        ("ARMS", f"{arms_pts}/71", (170, 255, 220), arms_pts > 0),
    ]

    tx = 30
    for name, pts_str, col, is_act in tabs:
        tw = 175
        box = [tx, 20, tx + tw, 62]
        bg_col = (30, 26, 32) if is_act else (16, 16, 18)
        border_col = col if is_act else (50, 48, 42)
        draw.rounded_rectangle(box, radius=6, fill=bg_col, outline=border_col, width=2 if is_act else 1)

        draw.text((box[0] + 14, box[1] + 12), f"◆ {name}", fill=col if is_act else (140, 140, 130), font=core.F_SMALL_BOLD)
        draw.text((box[2] - 46, box[1] + 12), pts_str, fill=col if is_act else (120, 120, 110), font=core.F_SMALL_BOLD)
        tx += tw + 12

    # Player build info on the right of the header
    draw.text((tx + 20, 24), f"Joueur : {player_name} (Niv. {level})", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    draw.text((tx + 20, 46), f"Points alloués : {spent_points} / 100", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Main area: 3 active trees displayed side by side (Physiology, Survival, Arms)
    # Load templates from assets/masteries/templates/
    tree_templates = [
        ("PHYSIOLOGY", "assets/masteries/templates/physiology_base.png", (255, 170, 190), 18),
        ("SURVIVAL", "assets/masteries/templates/survival_base.png", (215, 185, 255), 36),
        ("ARMS", "assets/masteries/templates/arms_base.png", (170, 255, 220), 37),
    ]

    col_w = 368
    panel_y = 80
    panel_h = CARD_H - 100

    for i, (t_name, t_path, t_col, t_pts) in enumerate(tree_templates):
        px = 30 + i * (col_w + 16)
        p_box = [px, panel_y, px + col_w, panel_y + panel_h]
        draw.rounded_rectangle(p_box, radius=8, fill=(14, 14, 16), outline=t_col, width=2)

        # Tree Header Banner inside panel
        draw.rounded_rectangle([p_box[0] + 8, p_box[1] + 8, p_box[2] - 8, p_box[1] + 44], radius=6, fill=(24, 20, 26), outline=t_col, width=1)
        draw.text((p_box[0] + 18, p_box[1] + 14), f"ARBRE : {t_name}", fill=t_col, font=core.F_SECTION_TITLE)
        draw.text((p_box[2] - 110, p_box[1] + 14), f"{t_pts} Points", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

        # Paste the tree template crop
        if os.path.exists(t_path):
            tree_im = Image.open(t_path).convert("RGBA")
            # Crop middle tree nodes area (skip header from original screenshot)
            tw, th = tree_im.size
            crop_nodes = tree_im.crop((int(tw * 0.05), int(th * 0.12), int(tw * 0.85), int(th * 0.95)))
            
            # Target box
            target_rect = [p_box[0] + 10, p_box[1] + 52, p_box[2] - 10, p_box[3] - 10]
            safe_paste(canvas, crop_nodes, (target_rect[0], target_rect[1], target_rect[2] - target_rect[0], target_rect[3] - target_rect[1]))

    out_p = os.path.join(OUT_DIR, "build_all_trees_highlighted.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    print("Saved build_all_trees_highlighted.jpg to", out_p)
    return out_p


def render_build_stats_summary_by_category(
    player_name: str = "Abdallah",
    level: int = 100
) -> str:
    """
    Renders Image 2 of Mastery Trees:
    - Pure stat breakdown organized by WHAT STAT THEY AFFECT (Stamina/Mobility, Energy, Survival, Combat)
    - Clean cards with exact percentage and numbers
    - NO 'Synthèse' or 'Verdict' text!
    """
    canvas = Image.new("RGBA", (CARD_W, CARD_H), (10, 10, 12, 255))
    draw = ImageDraw.Draw(canvas)

    # Border
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(10, 10, 12))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(35, 32, 24), width=1)

    # Header
    draw.rounded_rectangle([16, 14, CARD_W - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag = "RÉSUMÉ DES STATISTIQUES DU BUILD"
    tag_w = int(draw.textlength(tag, font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(40, 32, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), f"STATISTIQUES CUMULÉES : {player_name.upper()} (NIVEAU {level})", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # 4 Quadrants for the 4 Stat Categories:
    # 1. Stamina & Mobility (Top Left)
    # 2. Energy & Action (Top Right)
    # 3. Survival & Healing (Bottom Left)
    # 4. Combat & Armor Penetration (Bottom Right)
    quads = [
        {
            "title": "🏃 ENDURANCE & MOBILITÉ (STAMINA & MOBILITY)",
            "color": (255, 170, 190),  # Pink
            "box": [30, 88, 585, 380],
            "stats": [
                ("Vitesse de sprint en raid", "+15%", "Agilité & Course"),
                ("Consommation d'endurance au sprint", "-25%", "Endurance améliorée"),
                ("Régénération naturelle d'endurance", "+30%", "Récupération au repos"),
                ("Franchissement d'obstacles & saut", "+40%", "Fluidité d'escalade")
            ]
        },
        {
            "title": "⚡ ÉNERGIE & DÉBIT D'ACTION (ENERGY & ACTION POOL)",
            "color": (170, 255, 220),  # Mint Teal
            "box": [615, 88, CARD_W - 30, 380],
            "stats": [
                ("Réserve d'énergie maximale", "+20 Énergie", "Capacité brute"),
                ("Coût en énergie des frappes de mêlée", "-15%", "Frappes économiques"),
                ("Vitesse de rechargement des armes à feu", "-20%", "Manipulation d'armes"),
                ("Délai de récupération après attaque lourde", "-25%", "Enchaînement fluide")
            ]
        },
        {
            "title": "🩸 SURVIE & RÉSISTANCE (SURVIVAL & RESILIENCE)",
            "color": (215, 185, 255),  # Purple
            "box": [30, 400, 585, CARD_H - 24],
            "stats": [
                ("Vitesse de réanimation d'un allié (Surgeon 5/5)", "+50%", "Chirurgien de combat"),
                ("Points de vie de l'allié réanimé", "+40% PV", "Retour au combat"),
                ("Résistance aux saignements et poisons", "+35%", "Immunité de raid"),
                ("Vitesse d'application des bandages et baumes", "-30%", "Soins d'urgence")
            ]
        },
        {
            "title": "⚔️ COMBAT & PÉNÉTRATION D'ARMURE (COMBAT & WEAPONS)",
            "color": core.COLOR_GOLD,
            "box": [615, 400, CARD_W - 30, CARD_H - 24],
            "stats": [
                ("Pénétration d'armure frappes lourdes", "+25%", "Perce-armure"),
                ("Dégâts critiques d'estoc (Deft Strikes 5/5)", "+20%", "Précision létale"),
                ("Maniement et dégaine d'armes", "+25%", "Réactivité martiale"),
                ("Dégâts d'exécution sur cibles affaiblies", "+15%", "Finisher")
            ]
        }
    ]

    for q in quads:
        box = q["box"]
        col = q["color"]
        draw.rounded_rectangle(box, radius=8, fill=(16, 16, 18), outline=col, width=2)

        # Category Header
        draw.rounded_rectangle([box[0] + 8, box[1] + 8, box[2] - 8, box[1] + 44], radius=6, fill=(24, 22, 26), outline=col, width=1)
        draw.text((box[0] + 16, box[1] + 14), q["title"], fill=col, font=core.F_SECTION_TITLE)

        sy = box[1] + 54
        for stat_name, stat_val, stat_sub in q["stats"]:
            row_box = [box[0] + 10, sy, box[2] - 10, sy + 50]
            draw.rounded_rectangle(row_box, radius=6, fill=(22, 22, 26), outline=(45, 42, 38), width=1)

            draw.text((row_box[0] + 14, row_box[1] + 8), stat_name, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
            draw.text((row_box[0] + 14, row_box[1] + 28), f"Source : {stat_sub}", fill=(160, 160, 140), font=core.F_HEADER_TAG)

            # Value pill
            vw = int(draw.textlength(stat_val, font=core.F_CARD_TITLE)) + 24
            v_box = [row_box[2] - vw - 10, row_box[1] + 8, row_box[2] - 10, row_box[3] - 8]
            draw.rounded_rectangle(v_box, radius=4, fill=(35, 28, 18), outline=col, width=1)
            draw.text((v_box[0] + 12, v_box[1] + 6), stat_val, fill=col, font=core.F_CARD_TITLE)

            sy += 56

    out_p = os.path.join(OUT_DIR, "build_stats_summary.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    print("Saved build_stats_summary.jpg to", out_p)
    return out_p

if __name__ == "__main__":
    p1 = render_build_all_trees_view()
    p2 = render_build_stats_summary_by_category()
    print("Both mastery tree cards rendered successfully!")
