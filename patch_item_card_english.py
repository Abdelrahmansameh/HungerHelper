import re

p_cr = "co_pilot/card_renderer.py"
with open(p_cr, "r", encoding="utf-8") as f:
    text = f.read()

# Replace lines 300-365 in render_item_card with clean bilingual (pure English default)
old_section = """    # Category
    draw.text((icon_box[0] + 18, rarity_box[3] + 12), "CATÉGORIE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((icon_box[0] + 18, rarity_box[3] + 34), item_type[:32], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Safe Pouch Rule (Clear & Concise!)
    is_pouch = quest_name is not None or "cle" in item_name.lower() or "clé" in item_name.lower() or "ring" in item_name.lower() or sell_silver >= 5
    draw.text((icon_box[0] + 18, rarity_box[3] + 68), "RÈGLE EN BESACE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    if is_pouch:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(35, 18, 40), outline=core.PRIO_PURPLE, width=1)
        draw.text((icon_box[0] + 26, rarity_box[3] + 96), "🔒 À GARDER EN BESACE SÉCURISÉE", fill=(240, 180, 255), font=core.F_SMALL_BOLD)
    else:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(24, 24, 20), outline=core.BORDER_SUBTLE, width=1)
        draw.text((icon_box[0] + 26, rarity_box[3] + 96), "🎒 Sac classique (Perdable)", fill=(180, 180, 160), font=core.F_SMALL_BOLD)

    # Right: Data Panels
    panel_box = [340, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(panel_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # 1. VALEUR MARCHANDE (REVENTE & ACHAT)
    val_box = [panel_box[0] + 18, panel_box[1] + 14, panel_box[2] - 18, panel_box[1] + 115]
    draw.rounded_rectangle(val_box, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((val_box[0] + 16, val_box[1] + 10), "VALEUR MARCHANDE (PRIX DU CHÂTEAU)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    # S Coin
    draw.ellipse([val_box[0] + 18, val_box[1] + 42, val_box[0] + 38, val_box[1] + 62], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((val_box[0] + 24, val_box[1] + 43), "S", fill=(30, 30, 40), font=core.F_SMALL_BOLD)
    draw.text((val_box[0] + 46, val_box[1] + 38), f"{sell_silver} Argent", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # C Coin
    draw.ellipse([val_box[0] + 180, val_box[1] + 42, val_box[0] + 200, val_box[1] + 62], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((val_box[0] + 186, val_box[1] + 43), "C", fill=(40, 20, 10), font=core.F_SMALL_BOLD)
    draw.text((val_box[0] + 208, val_box[1] + 38), f"{sell_copper} Cuivre (Prix de revente)", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    vendor_text = f"• Achat marchand : Disponible chez {buy_vendor}" if buy_vendor else "• Achat marchand : Non vendu par les marchands (Loot de raid exclusif)"
    draw.text((val_box[0] + 18, val_box[1] + 78), vendor_text, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 2. LOCALISATION & MEILLEUR CONTENEUR
    drop_box = [panel_box[0] + 18, val_box[3] + 12, panel_box[2] - 18, val_box[3] + 125]
    draw.rounded_rectangle(drop_box, radius=8, fill=core.BG_CARD, outline=core.PRIO_YELLOW, width=1)
    draw.text((drop_box[0] + 16, drop_box[1] + 10), "LOCALISATION & MEILLEURS CONTENEURS EN RAID", fill=core.PRIO_YELLOW, font=core.F_SECTION_TITLE)

    # Container Icon inset if available
    c_img = core.CONTAINER_IMGS.get("flour_sack.webp") if "flour" in item_name.lower() else core.CONTAINER_IMGS.get("strongbox.webp")
    if c_img and "ring" not in item_name.lower():
        core.paste_icon_safe(canvas, c_img, (drop_box[0] + 16, drop_box[1] + 38, 70, 70), bg_color=core.BG_CARD)
        draw.text((drop_box[0] + 96, drop_box[1] + 42), f"• Meilleur conteneur : {best_source} — Taux : {drop_rate}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 96, drop_box[1] + 68), "• Cartes principales : Sarlat Farm, Jacques Bridge, Sombre Forest", fill=(190, 190, 170), font=core.F_BODY)
    else:
        draw.text((drop_box[0] + 16, drop_box[1] + 42), f"• Source : {best_source} — Taux : {drop_rate}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 16, drop_box[1] + 68), "• Meubles d'habitations, tiroirs et commodes des zones de raid.", fill=(190, 190, 170), font=core.F_BODY)

    # 3. QUÊTES & UTILITÉ
    q_box = [panel_box[0] + 18, drop_box[3] + 12, panel_box[2] - 18, drop_box[3] + 115]
    draw.rounded_rectangle(q_box, radius=8, fill=core.BG_CARD, outline=core.PRIO_PURPLE, width=1)
    draw.text((q_box[0] + 16, q_box[1] + 10), "USAGE POUR LES QUÊTES & L'ARTISANAT", fill=core.PRIO_PURPLE, font=core.F_SECTION_TITLE)"""

new_section = """    # Category
    cat_lbl = "CATEGORY :" if not is_french else "CATÉGORIE :"
    draw.text((icon_box[0] + 18, rarity_box[3] + 12), cat_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((icon_box[0] + 18, rarity_box[3] + 34), item_type[:32], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Safe Pouch Rule (Clear & Concise!)
    is_pouch = quest_name is not None or "cle" in item_name.lower() or "clé" in item_name.lower() or "ring" in item_name.lower() or sell_silver >= 5
    pouch_lbl = "SAFE POUCH RULE :" if not is_french else "RÈGLE EN BESACE :"
    draw.text((icon_box[0] + 18, rarity_box[3] + 68), pouch_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    if is_pouch:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(35, 18, 40), outline=core.PRIO_PURPLE, width=1)
        keep_txt = "🔒 KEEP IN SECURE POUCH" if not is_french else "🔒 À GARDER EN BESACE SÉCURISÉE"
        draw.text((icon_box[0] + 26, rarity_box[3] + 96), keep_txt, fill=(240, 180, 255), font=core.F_SMALL_BOLD)
    else:
        draw.rounded_rectangle([icon_box[0] + 18, rarity_box[3] + 92, icon_box[2] - 18, rarity_box[3] + 120], radius=4, fill=(24, 24, 20), outline=core.BORDER_SUBTLE, width=1)
        drop_txt = "🎒 Standard Backpack (Droppable)" if not is_french else "🎒 Sac classique (Perdable)"
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
        c_lbl1 = f"• Best Container : {best_source} — Rate : {drop_rate}" if not is_french else f"• Meilleur conteneur : {best_source} — Taux : {drop_rate}"
        c_lbl2 = "• Primary Maps : Sarlat Farm, Jacques Bridge, Sombre Forest" if not is_french else "• Cartes principales : Sarlat Farm, Jacques Bridge, Sombre Forest"
        draw.text((drop_box[0] + 96, drop_box[1] + 42), c_lbl1, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 96, drop_box[1] + 68), c_lbl2, fill=(190, 190, 170), font=core.F_BODY)
    else:
        c_lbl1 = f"• Source : {best_source} — Rate : {drop_rate}" if not is_french else f"• Source : {best_source} — Taux : {drop_rate}"
        c_lbl2 = "• Residential furniture, dressers and drawers across all raids." if not is_french else "• Meubles d'habitations, tiroirs et commodes des zones de raid."
        draw.text((drop_box[0] + 16, drop_box[1] + 42), c_lbl1, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((drop_box[0] + 16, drop_box[1] + 68), c_lbl2, fill=(190, 190, 170), font=core.F_BODY)

    # 3. QUÊTES & UTILITÉ
    q_box = [panel_box[0] + 18, drop_box[3] + 12, panel_box[2] - 18, drop_box[3] + 115]
    draw.rounded_rectangle(q_box, radius=8, fill=core.BG_CARD, outline=core.PRIO_PURPLE, width=1)
    hdr_q = "USAGE FOR QUESTS & CRAFTING" if not is_french else "USAGE POUR LES QUÊTES & L'ARTISANAT"
    draw.text((q_box[0] + 16, q_box[1] + 10), hdr_q, fill=core.PRIO_PURPLE, font=core.F_SECTION_TITLE)"""

if old_section in text:
    text = text.replace(old_section, new_section)
    with open(p_cr, "w", encoding="utf-8") as f:
        f.write(text)
    print("render_item_card successfully patched for pure English default!")
else:
    print("Could not find old_section in card_renderer.py!")
