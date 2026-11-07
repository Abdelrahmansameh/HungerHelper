import os
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v25 as core

CARD_W = 1200
CARD_H = 750

OUT_DIR = r"C:\Users\PC\Documents\HungerHelper\output_maps"
DATA_DIR = r"C:\Users\PC\Documents\HungerHelper\data\talent_trees"
DESKTOP_DIR = r"C:\Users\PC\Desktop\Hunger_Helper"
ROOT_DIR = r"C:\Users\PC\Documents\HungerHelper"

def create_talent_tree_master_card():
    canvas = Image.new("RGBA", (CARD_W, CARD_H), (15, 14, 12, 255))
    draw = ImageDraw.Draw(canvas)

    # Subtle background vignette / grid
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(15, 14, 12))
    
    # Outer gold border
    draw.rounded_rectangle([10, 10, CARD_W - 10, CARD_H - 10], radius=12, outline=core.COLOR_GOLD, width=2)
    
    # -------------------------------------------------------------
    # 1. TOP TABS BAR (HUNGER COMPANION EXACT REPLICA)
    # -------------------------------------------------------------
    tab_y = 20
    draw.text((28, tab_y), "HUNGER COMPANION · ARBRE DE TALENTS (BUILD ACTUEL)", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
    draw.text((CARD_W - 220, tab_y + 4), "POINTS DÉPENSÉS : 91", fill=core.PRIO_YELLOW, font=core.F_HEADER_TAG)

    # 5 Discipline Tabs
    tabs = [
        ("◆ CUNNING 0/72", (180, 150, 60), (40, 35, 20), False),
        ("◆ PHYSIOLOGY 18/83", (224, 122, 158), (55, 25, 40), True),
        ("◆ SURVIVAL 36/78", (155, 114, 207), (45, 25, 60), True),
        ("◆ MARTIAL 0/74", (74, 144, 226), (20, 35, 55), False),
        ("◆ ARMS 37/71", (48, 209, 204), (20, 50, 50), True),
    ]

    tx = 28
    for name, text_col, bg_col, is_active in tabs:
        tw = 165 if "PHYSIOLOGY" in name else 150
        border_col = text_col if is_active else (60, 60, 55)
        fill_col = bg_col if is_active else (22, 20, 18)
        
        box = [tx, 56, tx + tw, 90]
        draw.rounded_rectangle(box, radius=6, fill=fill_col, outline=border_col, width=2 if is_active else 1)
        draw.text((tx + 12, 65), name, fill=text_col if is_active else (140, 140, 130), font=core.F_SMALL_BOLD)
        tx += tw + 12

    # Line separator
    draw.line([(28, 102), (CARD_W - 28, 102)], fill=core.BORDER_SUBTLE, width=1)

    # -------------------------------------------------------------
    # 2. LEFT & CENTER PANELS: CROPPED ACTUAL IN-GAME TREES
    # -------------------------------------------------------------
    # Crop Arms Tree
    arms_p = os.path.join(DATA_DIR, "arms_tree.jpg")
    surv_p = os.path.join(DATA_DIR, "survival_tree.jpg")
    phys_p = os.path.join(DATA_DIR, "physiology_tree.jpg")

    # Panel 1: ARMS (37 pts)
    box_arms = [28, 115, 255, CARD_H - 24]
    draw.rounded_rectangle(box_arms, radius=8, fill=(18, 24, 24), outline=(48, 209, 204), width=2)
    draw.text((box_arms[0] + 10, box_arms[1] + 8), "ARMS (37 / 71)", fill=(48, 209, 204), font=core.F_HEADER_TAG)
    draw.text((box_arms[0] + 10, box_arms[1] + 28), "Maîtrise Tier VIII Débloquée", fill=(180, 240, 240), font=core.F_BODY)

    if os.path.exists(arms_p):
        im_a = Image.open(arms_p)
        # Crop the tree column: x roughly 130 to 450, y from 130 to 700
        w, h = im_a.size
        crop_a = im_a.crop((140, 120, 390, h - 20))
        crop_a = crop_a.resize((box_arms[2] - box_arms[0] - 16, box_arms[3] - box_arms[1] - 65), Image.Resampling.LANCZOS)
        canvas.paste(crop_a, (box_arms[0] + 8, box_arms[1] + 55))

    # Panel 2: SURVIVAL (36 pts)
    box_surv = [270, 115, 497, CARD_H - 24]
    draw.rounded_rectangle(box_surv, radius=8, fill=(24, 18, 28), outline=(155, 114, 207), width=2)
    draw.text((box_surv[0] + 10, box_surv[1] + 8), "SURVIVAL (36 / 78)", fill=(155, 114, 207), font=core.F_HEADER_TAG)
    draw.text((box_surv[0] + 10, box_surv[1] + 28), "Maîtrise Tier VIII Débloquée", fill=(220, 200, 240), font=core.F_BODY)

    if os.path.exists(surv_p):
        im_s = Image.open(surv_p)
        w, h = im_s.size
        crop_s = im_s.crop((160, 120, 480, h - 20))
        crop_s = crop_s.resize((box_surv[2] - box_surv[0] - 16, box_surv[3] - box_surv[1] - 65), Image.Resampling.LANCZOS)
        canvas.paste(crop_s, (box_surv[0] + 8, box_surv[1] + 55))

    # Panel 3: PHYSIOLOGY (18 pts)
    box_phys = [512, 115, 739, CARD_H - 24]
    draw.rounded_rectangle(box_phys, radius=8, fill=(28, 18, 22), outline=(224, 122, 158), width=2)
    draw.text((box_phys[0] + 10, box_phys[1] + 8), "PHYSIOLOGY (18 / 83)", fill=(224, 122, 158), font=core.F_HEADER_TAG)
    draw.text((box_phys[0] + 10, box_phys[1] + 28), "Mobilité & Vitalité Tier IV", fill=(240, 200, 215), font=core.F_BODY)

    if os.path.exists(phys_p):
        im_p = Image.open(phys_p)
        w, h = im_p.size
        crop_p = im_p.crop((120, 120, 360, h - 20))
        crop_p = crop_p.resize((box_phys[2] - box_phys[0] - 16, box_phys[3] - box_phys[1] - 65), Image.Resampling.LANCZOS)
        canvas.paste(crop_p, (box_phys[0] + 8, box_phys[1] + 55))

    # -------------------------------------------------------------
    # 3. RIGHT PANEL: COMBAT SYNERGIES & TALENT DETAILS
    # -------------------------------------------------------------
    right_box = [754, 115, CARD_W - 28, CARD_H - 24]
    draw.rounded_rectangle(right_box, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((right_box[0] + 16, right_box[1] + 14), "ANALYSE TACTIQUE DU BUILD (91 PTS)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((right_box[0] + 16, right_box[1] + 44), "Archétype : Colosse d'Armes & Survie", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    synergies = [
        ("🗡️ DISCIPLINE D'ARMES : DEFT STRIKES (5/5)", 
         "Les attaques légères avec armes de mêlée à deux mains consomment 25% MOINS d'énergie.",
         "Synergie ultime avec Zweihänder (52 estoc) : enchaînements continus sans fatigue.",
         (48, 209, 204)),

        ("💉 SURVIE & SOUTIEN D'ESCOUADE : SURGEON (5/5)",
         "Relève un coéquipier au sol 25% PLUS VITE en plein combat de raid.",
         "Pilier d'équipe : sauvetage d'urgence sous pression et récupération au feu.",
         (155, 114, 207)),

        ("🏃 PHYSIOLOGIE & MOBILITÉ ACTIVE (18 PTS)",
         "Sprint prolongé (5/5), Vitalité max (5/5), Saut & Agilité (5/5), Coagulation (3/5).",
         "Annule la lenteur des armes lourdes par une endurance de course décuplée.",
         (224, 122, 158)),

        ("👑 DOUBLE MAÎTRISE TIER VIII DÉBLOQUÉE",
         "Points maxés dans ARMS et SURVIVAL pour débloquer les ultimes passifs de fin de jeu.",
         "Évite totalement Martial (tir) et Cunning pour un focus 100% mêlée/survie.",
         core.PRIO_YELLOW)
    ]

    sy_y = right_box[1] + 82
    for title, l1, l2, col in synergies:
        card_sub = [right_box[0] + 14, sy_y, right_box[2] - 14, sy_y + 92]
        draw.rounded_rectangle(card_sub, radius=6, fill=(24, 22, 18), outline=(45, 42, 35), width=1)
        draw.text((card_sub[0] + 12, card_sub[1] + 8), title, fill=col, font=core.F_SMALL_BOLD)
        draw.text((card_sub[0] + 12, card_sub[1] + 32), l1, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((card_sub[0] + 12, card_sub[1] + 54), l2, fill=(180, 180, 160), font=core.F_BODY)
        sy_y += 102

    # Bottom Tip Box
    tip_box = [right_box[0] + 14, sy_y + 4, right_box[2] - 14, right_box[3] - 12]
    draw.rounded_rectangle(tip_box, radius=6, fill=(28, 24, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_box[0] + 12, tip_box[1] + 10), "💡 VERDICT TACTIQUE D'ÉLOÏSE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((tip_box[0] + 12, tip_box[1] + 34), "Build d'assaut et de soutien exceptionnel. Parfaitement taillé pour dominer au Zweihänder.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Save to outputs
    out_file1 = os.path.join(OUT_DIR, "build_thrust-master.jpg")
    out_file2 = os.path.join(OUT_DIR, "build_official_tree.jpg")
    out_file3 = os.path.join(ROOT_DIR, "mastery_build_summary.png")
    out_file4 = os.path.join(DESKTOP_DIR, "mastery_build_summary.png")
    out_artifact = os.path.join(r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49", "build_official_tree.jpg")

    canvas.convert("RGB").save(out_file1, quality=95)
    canvas.convert("RGB").save(out_file2, quality=95)
    canvas.convert("RGB").save(out_file3, quality=95)
    canvas.convert("RGB").save(out_file4, quality=95)
    canvas.convert("RGB").save(out_artifact, quality=95)
    print("Master talent build card successfully created and saved in all locations!")
    return out_file1

if __name__ == "__main__":
    create_talent_tree_master_card()
