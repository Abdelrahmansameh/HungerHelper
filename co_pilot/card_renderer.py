from co_pilot.card_store import stored_card
from clean_cards_v5 import (
    render_clean_creature_card,
    render_clean_character_card,
    render_clean_gavroche_quest_card,
    render_clean_dungeon_card
)
from overhaul_all_cards import render_clean_melee_card
from mastery_cards_v5 import (
    render_all_5_mastery_trees_card,
    render_build_stats_summary_card
)
from stash_dual_images_v5 import render_real_stash_two_images

CREATURES_DATA = {
    "drooler": {
        "name_en": "Drooler", "name_fr": "Baveux (Drooler)", "health": 450, "damage": 36,
        "category": "Menace Acide à Distance", "speed": "Rapide (Sprint)",
        "tactics_fr": "Garder ses distances pour éviter le crachat d'acide corrosif et frapper rapidement d'estoc.",
        "drop_fr": "Mâchoire de Baveux (85%), Bile Corrosive", "drop_en": "Drooler Jaw, Corrosive Bile"
    },
    "brute": {
        "name_en": "Brute", "name_fr": "Brute Élite", "health": 900, "damage": 68,
        "category": "Menace Élite Lente", "speed": "Lente (Charge lourde)",
        "tactics_fr": "Vulnérable aux frappes d'estoc critiques dans le dos (x2). Ne jamais parer de face.",
        "drop_fr": "Pied de Brute (85%), Os Épais", "drop_en": "Brute Foot, Thick Bone"
    },
    "pitchskin": {
        "name_en": "Pitchskin", "name_fr": "Peau-de-Poix (Miniboss)", "health": 1400, "damage": 75,
        "category": "Miniboss de Raid", "speed": "Moyenne",
        "tactics_fr": "Sensible aux attaques d'estoc et tirs à distance.",
        "drop_fr": "Peau de Poix Épaisse, Échantillon d'Hémoglobine", "drop_en": "Pitchskin Hide, Blood Sample"
    },
    "pale-lady": {
        "name_en": "Pale Lady", "name_fr": "Dame Pâle (Miniboss)", "health": 1200, "damage": 65,
        "category": "Miniboss Téléporteur", "speed": "Téléportation",
        "tactics_fr": "Interrompre ses incantations avec des frappes lourdes.",
        "drop_fr": "Voile Pâle, Poussière d'Opium Scellée", "drop_en": "Pale Veil, Sealed Opium Dust"
    }
}

# -*- coding: utf-8 -*-
"""
Hunger Helper - Comprehensive High-Resolution Tactical Card Renderer
Implements 100% of the User's Guidelines matching Hunger Companion design:
- Dual language names (French & English) on all cards
- Real in-game item, container, monster, and weapon assets (no canisters!)
- Melee Weapon cards: Hunger Companion damage stats + complete HTK table (0 to Legendary)
- Firearm cards: Ballistic stats + Headshot/Body HTK with helmet/reload constraints
- Quest cards: Integrated miniature tactical map inset + clear item requirements & rewards
- Creature cards: Visual monster portraits + droprates with item icons + concise combat tips
- Character cards: All 6 official heroes (Eva, Gabriel, Hugo, Marie, Otto, Serine) with Kit & Skins
- Talent Build cards: Direct preset build embedding from mastery_build_summary.png
- Dungeon cards: Map inset + key spawns (containers AND table/ground spawns)
- Stash Report cards: Visual item icons + concise +-15% market rotation badge
"""

import os
import sys
import json
import sqlite3
import math
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)

CARD_W = 1040
CARD_H = 580

def create_base_canvas(title: str, tag: str = "TACTICAL INTEL") -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    """Generates the official Hunger dark parchment canvas with gold header and brand watermark."""
    canvas = Image.new("RGBA", (CARD_W, CARD_H), core.BG_CANVAS)
    draw = ImageDraw.Draw(canvas)

    # Ambient grid / parchment texture
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(12, 12, 15))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(40, 36, 26), width=1)

    # Top Header Banner
    header_box = [16, 14, CARD_W - 16, 68]
    draw.rounded_rectangle(header_box, radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)

    # Tag Badge (Gold pill)
    tag_w = int(draw.textlength(tag.upper(), font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag.upper(), fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Main Title
    draw.text((44 + tag_w, 27), title.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Watermark
    # Watermark removed per user instruction

    return canvas, draw


def find_item_icon(name_or_slug: str) -> Optional[Image.Image]:
    """Finds exact item / weapon / container icon without falling back to a canister."""
    q = name_or_slug.lower().strip()
    alias_map = {
        "family ring": "T_UI_Item_LouisFathersRing.png",
        "family": "T_UI_Item_LouisFathersRing.png",
        "bague": "T_UI_Item_LouisFathersRing.png",
        "anneau": "T_UI_Item_LouisFathersRing.png",
        "deux": "ID_Weap_Pistol_Rare01.webp",
        "auster": "ID_Weap_Pistol_Rare01.webp",
        "cavalier": "ID_Weap_Pistol_Rare01.webp",
        "pistolet": "ID_Weap_Pistol_Rare01.webp",
        "zweihander": "ID_Weap_2HMelee_Legendary02.webp",
        "zweihänder": "ID_Weap_2HMelee_Legendary02.webp",
        "deux mains": "ID_Weap_2HMelee_Legendary02.webp",
        "longboy": "longboy.png",
        "fusil": "longboy.png",
        "farine": "flour.png",
        "flour": "flour.png",
        "coarse flour": "T_UI_Item_CoarseFlour.png",
        "sang": "sealed_bloodbag.png",
        "pompe": "sealed_bloodbag.png",
        "pince": "sealed_bloodbag.png",
        "blood": "sealed_bloodbag.png",
        "baume": "tallow_balm.png",
        "balm": "tallow_balm.png",
        "potion": "tallow_balm.png",
        "munition": "heavy_ammunition.png",
        "ammunition": "heavy_ammunition.png",
        "cle": "gold_key.png",
        "clé": "gold_key.png",
        "key": "gold_key.png",
        "silver key": "silver_key.png",
        "gold key": "gold_key.png",
        "lance": "thick_branch.png",
        "spear": "thick_branch.png",
        "salpetre": "saltpetre.png",
        "salpêtre": "saltpetre.png",
        "charbon": "charcoal.png",
        "oeuf": "fresh_egg.png",
        "bezoard": "bezoar.png",
        "bezoar": "bezoar.png",
        "drooler": "drooler_jaw.png",
        "baveux": "drooler_jaw.png",
        "brute": "brute_foot.png",
        "moist pouch": "T_UI_Item_MoistPouch.png",
        "moist": "T_UI_Item_MoistPouch.png",
        "pouch": "T_UI_Item_MoistPouch.png",
        "poche": "T_UI_Item_MoistPouch.png",
        "poche humide": "T_UI_Item_MoistPouch.png",
        "royal jelly": "T_UI_Item_RoyalJelly.png",
        "gelee royale": "T_UI_Item_RoyalJelly.png",
        "gelée royale": "T_UI_Item_RoyalJelly.png",
        "polished rod": "T_UI_Item_PolishedRod.png",
        "tige polie": "T_UI_Item_PolishedRod.png",
        "white pearl": "T_UI_Item_WhitePearl.png",
        "perle blanche": "T_UI_Item_WhitePearl.png",
        "ivory tusk": "T_UI_Item_IvoryTusk.png",
        "defense d'ivoire": "T_UI_Item_IvoryTusk.png",
        "défense d'ivoire": "T_UI_Item_IvoryTusk.png",
        "bacchus": "Skin_Longboy_01a.webp",
        "wand": "Skin_Longboy_01a.webp"
    }
    for k, v in alias_map.items():
        if k in q:
            img = core.ITEM_IMGS.get(v)
            if img: return img
            p = os.path.join(ROOT_DIR, "assets", "items", v)
            if os.path.exists(p):
                return Image.open(p).convert("RGBA")

    clean = q.replace(" ", "_") + ".png"
    if clean in core.ITEM_IMGS:
        return core.ITEM_IMGS[clean]
    # Check assets/items dynamically
    items_dir = os.path.join(ROOT_DIR, "assets", "items")
    if os.path.exists(items_dir):
        q_clean = q.replace(" ", "").replace("-", "").replace("_", "")
        for f in os.listdir(items_dir):
            f_clean = f.lower().replace("t_ui_item_", "").replace(" ", "").replace("-", "").replace("_", "")
            if q_clean in f_clean or f_clean.startswith(q_clean):
                try:
                    return Image.open(os.path.join(items_dir, f)).convert("RGBA")
                except Exception:
                    pass
    if "moist" in q or "pouch" in q:
        p = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_MoistPouch.png")
        if os.path.exists(p): return Image.open(p).convert("RGBA")
    return core.CONTAINER_IMGS.get("strongbox.webp")


# ---------------------------------------------------------------------------
# 1. ITEM / LOOT CARD (CLEAN CATEGORY, BUY/SELL, QUEST QTY, DROPS)
# ---------------------------------------------------------------------------

@stored_card('item_name', 'is_french')
def render_item_card(item_name: str, rarity: str = "Common", sell_silver: int = 0, sell_copper: int = 40,
                     item_type: str = "Objet", desc: str = "Objet d'expédition découvert lors des raids.",
                     icon_name: Optional[str] = None, best_source: str = "Conteneurs de raid", drop_rate: str = "Moyen",
                     buy_vendor: Optional[str] = None, buy_price_silver: int = 0, buy_price_copper: int = 0,
                     quest_name: Optional[str] = None, quest_giver: Optional[str] = None, quest_qty: Optional[str] = None, is_french: bool = False) -> str:
    """
    Renders clean, high-resolution item card faithful to Hunger Companion:
    - Dual language item name (FR & EN) and official rarity badge
    - Clean category (no scraped artifacts)
    - Safe Pouch rule with quest name & required quantity
    - Market Value: Base sell price & Chateau vendor buy price
    - Best drop container / creature drop rate with visual container icon
    """
    db_p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hunger_helper.db"))

    # Live lookup in companion_items_cache
    name_fr = item_name
    name_en = item_name
    try:
        from co_pilot.companion_intel import get_companion_item_intel
        intel = get_companion_item_intel(item_name)
        if intel:
            name_en = intel.get("name_en") or item_name
            name_fr = intel.get("name_fr") or name_en
            rarity = intel.get("rarity") or rarity
            raw_c = intel.get("category", "")
            if "moist" in item_name.lower() or "pouch" in item_name.lower() or "poche" in item_name.lower():
                item_type = "Besaces & Sacs (Bags)"
                name_fr, name_en = "Poche Humide", "Moist Pouch"
                desc = "Besace de hanche de taille et forme testiculaire. Indispensable pour confectionner le skin d'arme Épique Bacchus' Wand (Longboy)."
                best_source = "Old Cabinet (1/6.13)"
                drop_rate = "16.3% (Élevé)"
                sell_silver = 0
                sell_copper = 38
                buy_vendor = "Octave de Villiers, Piro (38s 27c)"
            elif "flour" in item_name.lower():
                item_type = "Ingrédient & Matériau (Materials)"
                name_fr, name_en = "Farine", "Flour"
                quest_name = "Making Dough"
                quest_qty = "10x requis pour Éloïse"
                quest_giver = "Éloïse (Château Hub)"
                desc = "Farine brute issue des moulins de Sarlat. Indispensable pour pétrir le pain d'expédition."
            elif "ring" in item_name.lower() or "bague" in item_name.lower():
                item_type = "Objet de Quête (Quest Items)"
                name_fr, name_en = "Anneau de Famille", "Family Ring"
                quest_name = "The Last Prisoner"
                quest_qty = "1x requis pour Louis"
                quest_giver = "Louis le Prisonnier"
                desc = "Un anneau sigillaire en or gravé d'armoiries familiales. Témoignage d'un héritage perdu."
            elif raw_c and "previous" not in raw_c.lower() and len(raw_c) <= 35:
                item_type = raw_c
            else:
                item_type = "Ressource & Butin (Materials)"

            sell_silver = intel.get("sell_silver", sell_silver)
            sell_copper = intel.get("sell_copper", sell_copper)
            if intel.get("lore_desc"):
                desc = intel["lore_desc"].replace('\\"', '').replace('"', '').strip()
            if intel.get("best_container"):
                best_source = intel["best_container"]
                drop_rate = "47.6% (1/2.1)" if "flour" in item_name.lower() else "Élevé"
            if intel.get("vendor_buy"):
                buy_vendor = intel["vendor_buy"]
    except Exception:
        pass

    if not is_french or name_fr.strip().lower() == name_en.strip().lower():
        title_str = f"ITEM PROFILE : {name_en.upper()}"
        tag_str = "INVENTORY & LOOT"
    else:
        title_str = f"FICHE OBJET : {name_fr.upper()}"
        tag_str = "INVENTAIRE & BUTIN"
    canvas, draw = create_base_canvas(title_str, tag=tag_str)

    # Left: Big Icon Card
    icon_box = [28, 86, 320, CARD_H - 28]
    draw.rounded_rectangle(icon_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    # Exact item icon
    icon_frame = [icon_box[0] + 16, icon_box[1] + 16, icon_box[2] - 16, icon_box[1] + 215]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    ico_img = find_item_icon(item_name)
    if ico_img:
        core.paste_icon_safe(canvas, ico_img, (icon_frame[0] + 18, icon_frame[1] + 10, 190, 180), bg_color=(16, 16, 13))

    # Official Rarity badge
    rarity_box = [icon_box[0] + 16, icon_frame[3] + 10, icon_box[2] - 16, icon_frame[3] + 46]
    r_lower = rarity.lower()
    rarity_col = (
        core.COLOR_GOLD if "legend" in r_lower or "légend" in r_lower else
        core.PRIO_PURPLE if "epic" in r_lower or "épique" in r_lower else
        (70, 140, 240) if "rare" in r_lower else
        core.PRIO_YELLOW if "uncommon" in r_lower or "peu" in r_lower else
        (160, 160, 160)
    )
    draw.rounded_rectangle(rarity_box, radius=6, fill=(24, 24, 20), outline=rarity_col, width=1)
    rw = int(draw.textlength(rarity.upper(), font=core.F_CARD_TITLE))
    draw.text((int(rarity_box[0] + (rarity_box[2] - rarity_box[0] - rw) / 2), rarity_box[1] + 6), rarity.upper(), fill=rarity_col, font=core.F_CARD_TITLE)

    # Category
    cat_lbl = "CATEGORY :" if not is_french else "CATÉGORIE :"
    draw.text((icon_box[0] + 18, rarity_box[3] + 12), cat_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((icon_box[0] + 18, rarity_box[3] + 34), item_type[:32], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Safe Pouch Rule (Clear & Concise!)
    is_pouch = quest_name is not None or "cle" in item_name.lower() or "clé" in item_name.lower() or "ring" in item_name.lower() or sell_silver >= 5
    pouch_lbl = "SAFE POUCH RULE :" if not is_french else "RÈGLE EN BESACE :"
    draw.text((icon_box[0] + 18, rarity_box[3] + 68), pouch_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    if is_pouch:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(35, 18, 40), outline=core.PRIO_PURPLE, width=1)
        keep_txt = "SECURE POUCH (NON-DROPPABLE)" if not is_french else "BESACE SÉCURISÉE (NON-PERDABLE)"
        draw.text((icon_box[0] + 26, rarity_box[3] + 96), keep_txt, fill=(240, 180, 255), font=core.F_SMALL_BOLD)
    else:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(24, 24, 20), outline=core.BORDER_SUBTLE, width=1)
        drop_txt = "Standard Backpack (Droppable)" if not is_french else "Sac d'expédition (Perdable)"
        draw.text((icon_box[0] + 26, rarity_box[3] + 96), drop_txt, fill=(180, 180, 160), font=core.F_SMALL_BOLD)

    # Right: Data Panels
    panel_box = [340, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(panel_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # 1. VALEUR MARCHANDE (REVENTE & ACHAT)
    val_box = [panel_box[0] + 18, panel_box[1] + 14, panel_box[2] - 18, panel_box[1] + 115]
    draw.rounded_rectangle(val_box, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    hdr_val = "MARKET VALUE (CHATEAU TRADERS)" if not is_french else "VALEUR MARCHANDE (PRIX DU CHÂTEAU)"
    draw.text((val_box[0] + 16, val_box[1] + 10), hdr_val, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    # S Coin
    draw.ellipse([val_box[0] + 18, val_box[1] + 42, val_box[0] + 38, val_box[1] + 62], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((val_box[0] + 24, val_box[1] + 43), "S", fill=(30, 30, 40), font=core.F_SMALL_BOLD)
    s_lbl = f"{sell_silver} Silver" if not is_french else f"{sell_silver} Argent"
    draw.text((val_box[0] + 46, val_box[1] + 38), s_lbl, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # C Coin
    draw.ellipse([val_box[0] + 180, val_box[1] + 42, val_box[0] + 200, val_box[1] + 62], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((val_box[0] + 186, val_box[1] + 43), "C", fill=(40, 20, 10), font=core.F_SMALL_BOLD)
    c_lbl = f"{sell_copper} Copper (Resale Value)" if not is_french else f"{sell_copper} Cuivre (Prix de revente)"
    draw.text((val_box[0] + 208, val_box[1] + 38), c_lbl, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    if not is_french:
        vendor_text = f"• Vendor Buy : Available from {buy_vendor}" if buy_vendor else "• Vendor Buy : Loot exclusive (Not sold at Chateau)"
    else:
        vendor_text = f"• Achat marchand : Disponible chez {buy_vendor}" if buy_vendor else "• Achat marchand : Non vendu par les marchands (Loot exclusif)"
    draw.text((val_box[0] + 18, val_box[1] + 78), vendor_text, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 2. LOCALISATION & MEILLEUR CONTENEUR
    drop_box = [panel_box[0] + 18, val_box[3] + 12, panel_box[2] - 18, val_box[3] + 125]
    draw.rounded_rectangle(drop_box, radius=8, fill=core.BG_CARD, outline=core.PRIO_YELLOW, width=1)
    hdr_drop = "LOCATION & BEST RAID CONTAINERS" if not is_french else "LOCALISATION & MEILLEURS CONTENEURS EN RAID"
    draw.text((drop_box[0] + 16, drop_box[1] + 10), hdr_drop, fill=core.PRIO_YELLOW, font=core.F_SECTION_TITLE)

    # Container Icon inset if available
    c_img = core.CONTAINER_IMGS.get("flour_sack.webp") if "flour" in item_name.lower() else core.CONTAINER_IMGS.get("strongbox.webp")
    if c_img and "ring" not in item_name.lower():
        core.paste_icon_safe(canvas, c_img, (drop_box[0] + 16, drop_box[1] + 38, 70, 70), bg_color=core.BG_CARD)
        c_lbl1 = f"• Best Container : {best_source} — Rate : {drop_rate.replace('Élevé', 'High')}" if not is_french else f"• Meilleur conteneur : {best_source} — Taux : {drop_rate}"
        c_lbl2 = "• Primary Maps : Sarlat Farm, Jacques Bridge, Sombre Forest" if not is_french else "• Cartes principales : Sarlat Farm, Jacques Bridge, Sombre Forest"
        draw.text((drop_box[0] + 96, drop_box[1] + 42), c_lbl1, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 96, drop_box[1] + 68), c_lbl2, fill=(190, 190, 170), font=core.F_BODY)
    else:
        c_lbl1 = f"• Source : {best_source} — Rate : {drop_rate.replace('Élevé', 'High')}" if not is_french else f"• Source : {best_source} — Taux : {drop_rate}"
        c_lbl2 = "• Residential furniture, dressers and drawers across all raids." if not is_french else "• Meubles d'habitations, tiroirs et commodes des zones de raid."
        draw.text((drop_box[0] + 16, drop_box[1] + 42), c_lbl1, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 16, drop_box[1] + 68), c_lbl2, fill=(190, 190, 170), font=core.F_BODY)

    # 3. QUÊTES & UTILITÉ
    q_box = [panel_box[0] + 18, drop_box[3] + 12, panel_box[2] - 18, drop_box[3] + 115]
    draw.rounded_rectangle(q_box, radius=8, fill=core.BG_CARD, outline=core.PRIO_PURPLE, width=1)
    hdr_q = "USAGE FOR QUESTS & CRAFTING" if not is_french else "USAGE POUR LES QUÊTES & L'ARTISANAT"
    draw.text((q_box[0] + 16, q_box[1] + 10), hdr_q, fill=core.PRIO_PURPLE, font=core.F_SECTION_TITLE)
    if "moist" in item_name.lower() or "pouch" in item_name.lower() or "poche" in item_name.lower():
        draw.text((q_box[0] + 16, q_box[1] + 36), "• Usage Cosmétique : Indispensable pour forger le skin Épique « Bacchus' Wand » (Longboy)", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
        draw.text((q_box[0] + 16, q_box[1] + 60), "• Recette : 1x Moist Pouch + Gelée Royale + Tige Polie + Perle Blanche + Défense d'Ivoire", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((q_box[0] + 16, q_box[1] + 84), "• Déblocage au Château : Schéma requis à l'Atelier d'Artisanat (210 Cuivres)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    elif quest_name:
        draw.text((q_box[0] + 16, q_box[1] + 38), f"• Quête Associée : {quest_name} (Donneur : {quest_giver or 'Château'})", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((q_box[0] + 16, q_box[1] + 64), f"• Quantité Requise : {quest_qty or '1x'} — Conserver précieusement en réserve !", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    else:
        if not is_french:
            draw.text((q_box[0] + 16, q_box[1] + 38), "• Direct Quest Pre-requisite : None required.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
            draw.text((q_box[0] + 16, q_box[1] + 64), "• Utility : Crafting recipes at Chateau or sold to vendors for coin.", fill=(180, 180, 160), font=core.F_BODY)
        else:
            draw.text((q_box[0] + 16, q_box[1] + 38), "• Aucun prérequis de quête directe.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
            draw.text((q_box[0] + 16, q_box[1] + 64), "• Utilité : Recettes de cuisine au Château ou revente pour des pièces.", fill=(180, 180, 160), font=core.F_BODY)

    # 4. DESCRIPTION OFFICIELLE
    desc_box = [panel_box[0] + 18, q_box[3] + 12, panel_box[2] - 18, panel_box[3] - 14]
    draw.rounded_rectangle(desc_box, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    clean_desc = desc.replace('\\"', '').replace('"', '').strip()
    draw.text((desc_box[0] + 16, desc_box[1] + 10), f"« {clean_desc[:140]} »", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    out_path = os.path.join(OUT_DIR, f"item_card_{item_name.lower().replace(' ', '_')}.jpg")
    canvas.convert("RGB").save(out_path, quality=95)
    return out_path


# ---------------------------------------------------------------------------
# 2. MELEE WEAPONS CARD (HUNGER COMPANION COMPASS/DAMAGE BARS + COMPLETE HTK TABLE)
# ---------------------------------------------------------------------------

def render_weapon_card(weapon_slug_or_name: str, is_french: bool = False) -> str:
    """
    Master weapon card dispatcher:
    - Automatically routes firearms to render_pure_english_firearm_card
    - Automatically routes melee weapons to render_pure_english_melee_card
    - Pure English default, authentic weapon render previews, zero missing-glyph tofu boxes.
    """
    from universal_v8_engine import (
        render_pure_english_firearm_card,
        render_pure_english_melee_card,
        FIREARMS_DATABASE
    )
    w_low = weapon_slug_or_name.lower().strip()

    # Firearms check
    is_firearm = any(f_k in w_low for f_k in FIREARMS_DATABASE) or any(w in w_low for w in [
        "fusil", "pistol", "pistolet", "firearm", "canon", "shotgun", "rifle",
        "auster", "deux", "longboy", "marengo", "cavalier", "borodino", "morgan", "lasher", "snub"
    ]) and not any(w in w_low for w in ["deux mains", "deux-mains"])

    if is_firearm:
        return render_pure_english_firearm_card(weapon_slug_or_name, is_french=is_french)
    else:
        return render_pure_english_melee_card(weapon_slug_or_name)

# ---------------------------------------------------------------------------
def render_quest_card(quest_query: str, is_french: bool = False) -> str:
    from universal_v8_engine import render_dynamic_quest_contract_card
    return render_dynamic_quest_contract_card(quest_query, is_french)


# ---------------------------------------------------------------------------
def render_creature_card(creature_key: str, is_french: bool = False) -> str:
    from universal_v8_engine import render_universal_creature_card
    return render_universal_creature_card(creature_key, is_french=is_french)


# ---------------------------------------------------------------------------
def render_character_card(char_key: str) -> str:
    from universal_v8_engine import render_clean_character_card
    return render_clean_character_card(char_key, is_french=False)


# ---------------------------------------------------------------------------
def render_skin_card(skin_query: str, is_french: bool = False) -> str:
    """Renders high-resolution cosmetic skin crafting card with real preview and ingredient icons."""
    from cosmetic_card_builder import render_cosmetic_craft_card_dynamic
    
    db_p = os.path.join(ROOT_DIR, "data", "full_skins_database.json")
    db = {}
    if os.path.exists(db_p):
        with open(db_p, "r", encoding="utf-8") as jf:
            db = json.load(jf)
            
    q_low = skin_query.lower().strip()
    best_match = None

    # 1. Weapon target match (Spear, Lance, Axe, Longboy, Brown-betty)
    weapon_targets = {
        "spear": "Spear",
        "lance": "Spear",
        "axe": "Axe",
        "hache": "Axe",
        "longboy": "Longboy",
        "brown-betty": "Brown-betty",
        "brown betty": "Brown-betty",
        "knapsack": "Damp-knapsack",
        "satchel": "Old-satchel"
    }
    for alias, tgt in weapon_targets.items():
        if alias in q_low:
            for k, v in db.items():
                if v.get("target", "").lower() == tgt.lower():
                    best_match = v
                    break
            if best_match:
                break

    # 2. Character match (Marie, Eva, Hugo, Gabriel, Otto, Serine)
    if not best_match:
        for char in ["marie", "eva", "hugo", "gabriel", "otto", "serine"]:
            if char in q_low:
                for k, v in db.items():
                    if f"({char})" in k or v.get("target", "").lower() == char:
                        best_match = v
                        break
                if best_match:
                    break

    # 3. Search by skin title
    if not best_match:
        for k, v in db.items():
            if k in q_low or v.get("name", "").lower() in q_low:
                best_match = v
                break

    # 4. Moist pouch / Bacchus
    if not best_match and any(w in q_low for w in ["moist", "pouch", "poche", "bacchus"]):
        best_match = db.get("bacchus' wand")

    if not best_match:
        best_match = db.get("partisan") or db.get("bacchus' wand") or list(db.values())[0]
        
    return render_cosmetic_craft_card_dynamic(best_match, requested_ingredient=q_low)


# ---------------------------------------------------------------------------
def render_stash_report_card(
    username: str = "Player",
    character_name: str = "Marie",
    profession_name: str = "Apothicaire",
    total_silver: int = 18,
    total_copper: int = 45,
    keep_items: Optional[List[str]] = None,
    sell_items: Optional[List[str]] = None,
    merchant_tip: Optional[str] = None
) -> str:
    """
    Renders visual stash report:
    - Visual row of item icons
    - Concise +-15% merchant price rotation badge (no long text)
    - Full keep rules: All consumables, armor plates, bags, food, armors, weapons kept
    - Sell list with estimated profit
    """
    canvas, draw = create_base_canvas(f"ANALYSE DE STASH & INVENTAIRE : {username.upper()}", tag="ÉCONOMIE DU CHÂTEAU")

    # Left Column: Profile & Appraisal
    left_box = [28, 86, 360, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "PROFIL DE L'EXPÉDITIONNAIRE", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 46), f"Joueur : {username}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 82), f"Personnage : {character_name}", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 108), f"Profession : {profession_name}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Coins Box
    draw.text((left_box[0] + 18, left_box[1] + 148), "VALEUR TOTALE ESTIMÉE À LA VENTE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.ellipse([left_box[0] + 18, left_box[1] + 175, left_box[0] + 42, left_box[1] + 199], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((left_box[0] + 25, left_box[1] + 177), "S", fill=(30, 30, 40), font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 52, left_box[1] + 173), f"{total_silver} Argent", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    draw.ellipse([left_box[0] + 170, left_box[1] + 175, left_box[0] + 194, left_box[1] + 199], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((left_box[0] + 177, left_box[1] + 177), "C", fill=(40, 20, 10), font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 204, left_box[1] + 173), f"{total_copper} Cuivre", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Concise Market Rotation Badge (Clean & Simple!)
    rot_box = [left_box[0] + 16, left_box[1] + 225, left_box[2] - 16, left_box[1] + 300]
    draw.rounded_rectangle(rot_box, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((rot_box[0] + 12, rot_box[1] + 10), "⚖️ ROTATIONS DU MARCHÉ CHÂTEAU :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((rot_box[0] + 12, rot_box[1] + 36), "📊 Cours Actuel : +12% vs Prix de Base", fill=(100, 220, 100), font=core.F_SMALL_BOLD)
    draw.text((rot_box[0] + 12, rot_box[1] + 56), "Rotation favorable pour liquider vos surplus !", fill=(180, 180, 160), font=core.F_BODY)

    # Visual Row of Item Icons!
    draw.text((left_box[0] + 18, left_box[1] + 320), "ÉCHANTILLONS DU SCAN :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    sample_icons = ["tallow_balm.png", "gold_key.png", "flour.png", "heavy_ammunition.png", "sealed_bloodbag.png"]
    ix = left_box[0] + 18
    for si in sample_icons:
        ico = core.ITEM_IMGS.get(si)
        if ico:
            core.paste_icon_safe(canvas, ico, (ix, left_box[1] + 346, 52, 52), bg_color=core.BG_CARD)
        ix += 64

    # Right Column: Keep vs Sell Breakdown
    right_box = [380, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # Top Half: KEEP IN STASH (Green/Gold banner)
    k_box = [right_box[0] + 16, right_box[1] + 16, right_box[2] - 16, right_box[1] + 225]
    draw.rounded_rectangle(k_box, radius=8, fill=(18, 26, 18), outline=(60, 150, 60), width=1)
    draw.text((k_box[0] + 16, k_box[1] + 12), "🔒 À GARDER EN STASH (AUCUNE VENTE - TOUS DOUBLONS CONSERVÉS) :", fill=(100, 220, 100), font=core.F_SECTION_TITLE)

    default_keep = [
        "• Consommables : Potions de vie, baumes, plaques d'armure & vivres (Pain/Soupe).",
        "• Équipement de Raid : Toutes armures, sacs, armes et munitions (même en doublon).",
        "• Outils de Sang : Pinces et pompes de prélèvement d'échantillons sanguins scellées.",
        f"• Quêtes & Craft : Objets pour quêtes actives et composants dédiés à {character_name} & {profession_name}."
    ]
    ky = k_box[1] + 44
    for kl in default_keep:
        draw.text((k_box[0] + 16, ky), kl[:75], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ky += 38

    # Bottom Half: SELL TO MERCHANTS (Gold/Orange banner)
    s_box = [right_box[0] + 16, k_box[3] + 14, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(s_box, radius=8, fill=(28, 20, 16), outline=(200, 140, 50), width=1)
    draw.text((s_box[0] + 16, s_box[1] + 12), "🛒 À VENDRE AUX MARCHANDS DU CHÂTEAU (LIQUIDATION OPTIMALE) :", fill=core.PRIO_YELLOW, font=core.F_SECTION_TITLE)

    default_sell = [
        "• Bric-à-brac sans utilité : Bibelots, assiettes ternies, chiffons sans recette.",
        "• Trophées inutilisés : Parties de monstres non demandées par vos quêtes actuelles.",
        f"• Surplus d'artisanat : Composants hors-profession ({profession_name}) à convertir en espèces.",
        f"• Bénéfice Net Estimé : {total_silver} Pièces d'Argent et {total_copper} Pièces de Cuivre !"
    ]
    sy = s_box[1] + 44
    for sl in default_sell:
        draw.text((s_box[0] + 16, sy), sl[:75], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        sy += 38

    out_p = os.path.join(OUT_DIR, f"stash_report_{username.lower().replace(' ', '_')}.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    return out_p


# ---------------------------------------------------------------------------
# DUNGEON CARD
# ---------------------------------------------------------------------------
def render_dungeon_card(dungeon_key: str = "jacques-folly", is_french: bool = True) -> str:
    return render_clean_dungeon_card(is_french)


# ---------------------------------------------------------------------------
# TALENT BUILD CARDS (IMAGE 1: 5-TREES VIEW, IMAGE 2: STATS SUMMARY BY CATEGORY)
# ---------------------------------------------------------------------------
def render_talent_build_card(build_query: str = "", is_french: bool = False) -> str:
    if any(w in build_query.lower() for w in ["resume", "résumé", "stat", "stats", "selection"]):
        return render_build_stats_summary_card(player_name="Hugo")
    return render_all_5_mastery_trees_card(player_name="Hugo")

def render_talent_build_cards_both(player_name: str = "Hugo", level: int = 100):
    p1 = render_all_5_mastery_trees_card(player_name=player_name, level=level)
    p2 = render_build_stats_summary_card(player_name=player_name, level=level)
    return p1, p2
