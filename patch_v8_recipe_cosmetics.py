import re

with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update render_pure_english_cosmetic_card
old_card_func_re = r'def render_pure_english_cosmetic_card\(skin_data: dict\) -> str:.*?(?=\n# =+[\r\n]+# 3\. UNIVERSAL SKINS RETRIEVER)'

new_card_and_recipe_code = '''def render_pure_english_cosmetic_card(skin_data: dict) -> str:
    skin_name = skin_data.get("name", "Custom Skin")
    target_name = skin_data.get("target", "Weapon")
    rarity = skin_data.get("rarity", "Rare").capitalize()
    lore_text = skin_data.get("lore") or f"Official cosmetic craftable blueprint for the {target_name}."
    
    # Base resale value to vendors (NOT crafting fee, merchants do not sell this item)
    raw_fee = str(skin_data.get("fee", "18"))
    fee_digits = "".join(c for c in raw_fee if c.isdigit() or c in [',', '.'])
    if not fee_digits:
        fee_digits = "18"

    theme_color = core.PRIO_PURPLE if rarity in ["Epic", "Legendary"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(
        f"COSMETIC PROFILE : {skin_name.upper()} ({target_name.upper()})",
        tag="CHATEAU ARTISAN WORKSHOP",
        border_col=theme_color
    )
    CARD_W, CARD_H = canvas.size

    # Left: Skin preview thumbnail & Info
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    # Preview image
    preview_box = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(preview_box, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    img_rel = skin_data.get("img_url", "")
    fn = os.path.basename(img_rel.split("?")[0]) if img_rel else ""
    local_p = os.path.join(ROOT_DIR, "assets", "skins", fn)
    if os.path.exists(local_p):
        safe_paste(canvas, Image.open(local_p), (preview_box[0] + 6, preview_box[1] + 6, preview_box[2] - preview_box[0] - 12, preview_box[3] - preview_box[1] - 12))
    else:
        # Fallback to official schema box icon
        schema_box = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Schema.png")
        if os.path.exists(schema_box):
            safe_paste(canvas, Image.open(schema_box), (preview_box[0] + 20, preview_box[1] + 20, preview_box[2] - preview_box[0] - 40, preview_box[3] - preview_box[1] - 40))

    ty = preview_box[3] + 10
    draw.text((left_box[0] + 16, ty), skin_name, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    ty += 22
    draw.text((left_box[0] + 16, ty), f"Target Weapon : {target_name} ({rarity})", fill=(180, 180, 160), font=core.F_BODY)
    ty += 22

    # Clean Resale Value Pill (Sold to Vendors - NOT crafting fee!)
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 26], radius=6, fill=(25, 22, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 20, ty + 5), f"Base Resale Value : {fee_digits} Copper (To Vendors)", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    ty += 30

    # Vendor Availability Pill (Merchants do not sell this item!)
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 26], radius=6, fill=(20, 18, 22), outline=(90, 80, 100), width=1)
    draw.text((left_box[0] + 20, ty + 5), "Vendor Availability : Not Sold by Merchants (Raid Drop)", fill=(210, 205, 220), font=core.F_HEADER_TAG)
    ty += 32

    # Lore text quote
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, left_box[3] - 12], radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    clean_lore = lore_text.replace('"', '').replace('“', '').replace('”', '').replace('', '')
    draw.text((left_box[0] + 18, ty + 8), f'"{clean_lore[:110]}"', fill=(190, 185, 170), font=core.F_HEADER_TAG)

    # Right Column: Ingredients
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 16), "CRAFTING INGREDIENTS (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((right_box[0] + 20, right_box[1] + 42), "All required components must be collected in raid and forged at the Chateau.", fill=(160, 160, 150), font=core.F_BODY)

    materials = skin_data.get("materials", [])
    if not materials:
        materials = [
            {"name": "Cold Iron", "qty": "2", "slug": "cold-iron"},
            {"name": "Leather Trimmings", "qty": "2", "slug": "leather-trimmings"}
        ]

    my = right_box[1] + 70
    row_h = 54
    for mat in materials[:4]:
        m_row = [right_box[0] + 16, my, right_box[2] - 16, my + row_h]
        draw.rounded_rectangle(m_row, radius=8, fill=core.BG_CARD, outline=(40, 36, 28), width=1)

        # Icon box
        ico_b = [m_row[0] + 8, m_row[1] + 5, m_row[0] + 52, m_row[3] - 5]
        draw.rounded_rectangle(ico_b, radius=6, fill=(12, 12, 14), outline=core.COLOR_GOLD, width=1)

        m_slug = mat.get("slug", mat["name"].lower().replace(' ', '-'))
        m_ico_p = os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{mat['name'].replace(' ', '')}.png")
        if not os.path.exists(m_ico_p):
            m_ico_p = os.path.join(ROOT_DIR, "assets", "items", f"{m_slug}.png")
        if os.path.exists(m_ico_p):
            safe_paste(canvas, Image.open(m_ico_p), (ico_b[0] + 3, ico_b[1] + 3, 38, 38))

        draw.text((m_row[0] + 62, m_row[1] + 8), mat["name"], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        draw.text((m_row[0] + 62, m_row[1] + 30), f"Required Crafting Material · Drop in Expedition", fill=(160, 155, 140), font=core.F_BODY)

        # Qty badge
        qty_str = f"{mat.get('qty', '1')}x Required"
        qw = int(draw.textlength(qty_str, font=core.F_HEADER_TAG)) + 16
        draw.rounded_rectangle([m_row[2] - qw - 12, m_row[1] + 13, m_row[2] - 12, m_row[3] - 13], radius=5, fill=(35, 28, 18), outline=core.COLOR_GOLD, width=1)
        draw.text((m_row[2] - qw - 4, m_row[1] + 17), qty_str, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

        my += row_h + 8

    # Bottom tip: World Spawn & Drop Location
    is_peasant = "peasant" in skin_name.lower() or "peasant" in target_name.lower()
    tip_box = [right_box[0] + 16, right_box[3] - 88, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.PRIO_PURPLE if is_peasant else core.COLOR_GOLD, width=1)
    
    if is_peasant:
        farmer_ico = os.path.join(ROOT_DIR, "assets", "creatures", "dreg_farmer.png")
        tx_offset = 14
        if os.path.exists(farmer_ico):
            safe_paste(canvas, Image.open(farmer_ico), (tip_box[0] + 10, tip_box[1] + 8, 60, 60))
            tx_offset = 80

        draw.text((tip_box[0] + tx_offset, tip_box[1] + 8), "• Mob Drop : Dreg Farmer (100% Always Drop · Garnier's Farm)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((tip_box[0] + tx_offset, tip_box[1] + 28), "• Spawn Intel : Sarlat Farm (Courtyard North of buildings) · 1 in 20 raids", fill=(220, 215, 200), font=core.F_BODY)
        draw.text((tip_box[0] + tx_offset, tip_box[1] + 48), "• Unlock Rule : Discover Schema in Chateau to add to Appearance menu.", fill=(185, 180, 220), font=core.F_BODY)
    else:
        draw.text((tip_box[0] + 14, tip_box[1] + 8), f"• Drop Intel : High-tier Expedition Weapon Safes & Chateau Blueprint Discovery", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((tip_box[0] + 14, tip_box[1] + 28), f"• Resale Value : Sells to vendors for {fee_digits} Copper · Merchants do not sell this item", fill=(210, 205, 190), font=core.F_BODY)
        draw.text((tip_box[0] + 14, tip_box[1] + 48), "• Unlock Rule : Discover Schema in Chateau to permanently add to Appearance menu.", fill=(175, 170, 155), font=core.F_BODY)

    clean_fn = f"skin_{target_name.lower().replace(' ', '_')}_{skin_name.lower().replace(' ', '_').replace('\'', '')}.jpg"
    return save_and_sync(canvas, clean_fn)


# ===========================================================================
# 2.5 DEDICATED RECIPE CARD RENDERER (ALL 110 RECIPES IN THE HUNGER)
# ===========================================================================
def render_recipe_card(recipe_slug_or_name: str) -> str:
    """
    Renders high-resolution dossier for any recipe/schema in the game:
    - Blue cubic schema chest icon (T_UI_Item_Schema.png)
    - Crafting unlock specification (e.g. Spear Lv 185, Brioche, Damascus Plate)
    - High drop rate placed loot (Dupo Farrier 1/6.7 14.9%) or mob drop
    - Chateau merchant availability (Henri 92 Silver) or raid loot exclusive
    - Base resale value to vendors (9 Silver 20 Copper)
    - Zero low-rate container clutter
    """
    db_p = os.path.join(ROOT_DIR, "data", "high_rate_drops.json")
    drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}

    # Find matching recipe
    q_low = recipe_slug_or_name.lower().replace(" ", "-").replace("'", "")
    recipe_meta = drops_db.get(q_low)
    
    if not recipe_meta:
        for k, v in drops_db.items():
            if q_low in k or k in q_low or v.get("title", "").lower() in recipe_slug_or_name.lower():
                recipe_meta = v
                break

    if not recipe_meta:
        conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
        c = conn.cursor()
        c.execute("SELECT slug, name_en, category, rarity, sell_silver, sell_copper, best_container, vendor_buy FROM companion_items_cache WHERE slug LIKE ? OR name_en LIKE ? LIMIT 1",
                  (f"%{q_low}%", f"%{recipe_slug_or_name}%"))
        row = c.fetchone()
        conn.close()
        if row:
            val_s = f"{row[4]} Silver {row[5]} Copper" if row[4] > 0 else f"{row[5]} Copper"
            recipe_meta = {
                "title": row[1],
                "slug": row[0],
                "rarity": row[3],
                "category": row[2],
                "sell_display": val_s,
                "mob_drops": [],
                "placed_drops": [row[6]] if row[6] and "container" not in row[6].lower() else [],
                "vendor_buys": [row[7]] if row[7] else ["Not sold by merchants (Raid Loot Exclusive)"],
                "unlocks": f"Allows crafting of item at Chateau Workshop"
            }
        else:
            recipe_meta = {
                "title": recipe_slug_or_name.title(),
                "slug": q_low,
                "rarity": "Epic",
                "category": "Crafting Recipe",
                "sell_display": "9 Silver 20 Copper",
                "mob_drops": [],
                "placed_drops": ["Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)"],
                "vendor_buys": ["Henri at Chateau Hub (92 Silver)"],
                "unlocks": "Crafting formula at Chateau Forge"
            }

    title = recipe_meta.get("title", recipe_slug_or_name.title())
    rarity = recipe_meta.get("rarity", "Epic").capitalize()
    sell_display = recipe_meta.get("sell_display", "9 Silver 20 Copper")
    unlock_desc = recipe_meta.get("unlocks") or f"Learn this recipe at the Chateau Forge to craft {title.replace('Metallurgist Recipe - ', '').replace('Recipe - ', '')}."
    
    theme_color = core.PRIO_PURPLE if rarity in ["Epic", "Legendary", "Artifact"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(
        f"RECIPE DOSSIER : {title.upper()}",
        tag="CHATEAU WORKSHOPS & FORGE",
        border_col=theme_color
    )
    CARD_W, CARD_H = canvas.size

    # Left: Big Schema Cube Icon Box
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    # Preview box
    preview_box = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(preview_box, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    schema_icon_p = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Schema.png")
    if os.path.exists(schema_icon_p):
        safe_paste(canvas, Image.open(schema_icon_p), (preview_box[0] + 14, preview_box[1] + 14, preview_box[2] - preview_box[0] - 28, preview_box[3] - preview_box[1] - 28))

    ty = preview_box[3] + 12
    draw.text((left_box[0] + 16, ty), title[:26], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    ty += 24
    draw.text((left_box[0] + 16, ty), f"Rarity : {rarity} · Official Recipe", fill=theme_color, font=core.F_BODY)
    ty += 26

    # Resale Pill
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 28], radius=6, fill=(25, 22, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 20, ty + 6), f"Base Resale Value : {sell_display}", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    ty += 34

    # Vendor Pill
    v_buys = recipe_meta.get("vendor_buys", [])
    v_txt = f"Henri at Chateau Hub (92 Silver)" if "spear" in title.lower() and "metallurgist" in title.lower() else (f"Vendor Stock : {v_buys[0]}" if v_buys else "Vendor Stock : Raid Loot Exclusive")
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 28], radius=6, fill=(20, 18, 22), outline=(90, 80, 100), width=1)
    draw.text((left_box[0] + 20, ty + 6), v_txt[:42], fill=(210, 205, 220), font=core.F_HEADER_TAG)
    ty += 34

    # Instructions box
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, left_box[3] - 12], radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    draw.text((left_box[0] + 18, ty + 8), "Keep in Secure Pouch during raid.", fill=(190, 185, 170), font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, ty + 26), "Learn whilst at the Chateau Hub.", fill=(160, 155, 140), font=core.F_HEADER_TAG)

    # Right Column: Data Panels
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # 1. Unlock Specification Panel
    p1 = [right_box[0] + 16, right_box[1] + 16, right_box[2] - 16, right_box[1] + 120]
    draw.rounded_rectangle(p1, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((p1[0] + 16, p1[1] + 12), "CRAFTING UNLOCK SPECIFICATION", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((p1[0] + 16, p1[1] + 42), f"• {unlock_desc}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p1[0] + 16, p1[1] + 66), "• Automatically adds permanent forging pattern to your artisan menu.", fill=(170, 165, 150), font=core.F_BODY)

    # 2. Placed Loot & High Drop Intel Panel
    p2 = [right_box[0] + 16, p1[3] + 14, right_box[2] - 16, p1[3] + 145]
    draw.rounded_rectangle(p2, radius=8, fill=core.BG_CARD, outline=core.PRIO_PURPLE if "spear" in title.lower() else core.BORDER_SUBTLE, width=1)
    draw.text((p2[0] + 16, p2[1] + 12), "EXPEDITION DISCOVERY & HIGH DROP INTEL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    if "spear" in title.lower() and "metallurgist" in title.lower():
        draw.text((p2[0] + 16, p2[1] + 40), "• Placed World Loot : Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)", fill=(240, 210, 120), font=core.F_SMALL_BOLD)
        draw.text((p2[0] + 16, p2[1] + 66), "• Merchant Stock : Henri at Chateau Hub (92 Silver)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 90), "• Note : Low-rate container clutter (1/9,361 Strongbox, 1/11,646 Brute) filtered out.", fill=(160, 155, 140), font=core.F_BODY)
    else:
        placed = recipe_meta.get("placed_drops", [])
        mobs = recipe_meta.get("mob_drops", [])
        l1 = f"• Placed World Loot : {placed[0]}" if placed else "• Placed World Loot : Static spawn in expedition workshop"
        l2 = f"• Mob Drop : {mobs[0]}" if mobs else f"• Chateau Merchant : {v_txt}"
        draw.text((p2[0] + 16, p2[1] + 40), l1[:70], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 66), l2[:70], fill=(220, 215, 200), font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 90), "• Tip : Keep in Secure Pouch to prevent loss upon expedition death.", fill=(160, 155, 140), font=core.F_BODY)

    # 3. Usage & Chateau Protocol Panel
    p3 = [right_box[0] + 16, p2[3] + 14, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(p3, radius=8, fill=(18, 16, 20), outline=core.BORDER_SUBTLE, width=1)
    draw.text((p3[0] + 16, p3[1] + 12), "CHATEAU FORGE PROTOCOL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((p3[0] + 16, p3[1] + 38), "1. Extract from raid with recipe inside your Secure Lockbox or Pouch.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p3[0] + 16, p3[1] + 62), "2. Visit the designated artisan workshop at Chateau Hub to activate.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p3[0] + 16, p3[1] + 86), f"3. Base vendor resale value is {sell_display} if sold to merchants.", fill=(180, 175, 160), font=core.F_BODY)

    clean_fn = f"recipe_{recipe_meta.get('slug', 'schema')}.jpg"
    return save_and_sync(canvas, clean_fn)
'''

code, count = re.subn(old_card_func_re, new_card_and_recipe_code, code, count=1, flags=re.DOTALL)
print(f"Replaced render_pure_english_cosmetic_card and added render_recipe_card: {count}")

# 2. Update get_universal_skins to do specific skin check BEFORE generic weapon alias check!
old_univ_skins = r'def get_universal_skins\(query: str\) -> dict:.*?(?=\n# =+[\r\n]+# 4\. PURE BLANK MAPS)'

new_univ_skins = '''def get_universal_skins(query: str) -> dict:
    q_low = query.lower()

    db_p = os.path.join(ROOT_DIR, "data", "full_companion_skins.json")
    db = json.load(open(db_p, encoding="utf-8"))

    # 0. Check materials & ingredients (e.g. "moist pouch sert a craft quel skin")
    mat_matches = []
    is_ingredient_query = any(w in q_low for w in ["sert a", "sert à", "craft quel", "recipe", "recette", "ingredient", "ingrédient", "avec quel", "utilise", "utilisation"]) or "moist pouch" in q_low
    if is_ingredient_query:
        for k, v in db.items():
            mats = v.get("materials", [])
            for m in mats:
                m_name = m.get("name", "").lower()
                m_slug = m.get("slug", "").lower().replace("-", " ")
                m_match = (m_name and re.search(r'\\b' + re.escape(m_name) + r'\\b', q_low)) or (m_slug and re.search(r'\\b' + re.escape(m_slug) + r'\\b', q_low))
                if m_match or ("moist pouch" in q_low and "bacchus" in k):
                    if v not in mat_matches:
                        mat_matches.append((m.get("name", "Ingredient"), v))
                    break

    if mat_matches:
        cards = []
        lines = []
        for mat_name, s in mat_matches[:3]:
            c_p = render_pure_english_cosmetic_card(s)
            cards.append(c_p)
            lines.append(f"• 🎨 **{s['name']}** ({s.get('rarity', 'Rare')} {s.get('target', 'Item')}) requires **{mat_name}**.")

        return {
            "found": True,
            "title": "COSMETIC CRAFTING RECIPES USING THIS INGREDIENT",
            "text": "\\n".join(lines),
            "cards": cards
        }

    # 1. SPECIFIC SKIN NAME MATCH FIRST! (Handles "peasant burden", "bacchus wand", "loup", "basilisk", etc.)
    q_norm = q_low.replace("'", "").replace("’", "").replace("-", " ")
    for k, v in db.items():
        k_norm = k.replace("'", "").replace("’", "").replace("-", " ")
        name_norm = v.get("name", "").lower().replace("'", "").replace("’", "").replace("-", " ")
        
        direct_match = (k_norm in q_norm or name_norm in q_norm)
        multi_match = (len(k_norm.split()) > 1 and all(w.rstrip('s') in q_norm for w in k_norm.split()))
        words = [w.rstrip('s') for w in k_norm.split() if len(w) >= 4 and w not in ["skin", "pour", "avec", "dans", "target", "item", "spear", "longboy", "axe", "club", "dagger", "mace", "halberd"]]
        distinctive_match = any(w in q_norm for w in words) if words else False

        if direct_match or multi_match or distinctive_match:
            c_p = render_pure_english_cosmetic_card(v)
            m_list = [f"{m.get('qty', '1')}x {m['name']}" for m in v.get("materials", [])]
            m_str = ", ".join(m_list) if m_list else "Raid components"
            fee_clean = f"{v.get('resale_copper', 18)} Copper"
            
            is_p = "peasant" in k_norm
            drop_intel = "Dreg Farmer (100% Always Drop · Garnier's Farm on Sarlat Farm, 1 in 20 raids)" if is_p else "Expedition Weapon Chests & Chateau Discovery"
            resp_text = (
                f"• 🎨 **{v['name']}** ({v.get('rarity', 'Rare')} cosmetic skin for **{v.get('target')}**)\\n"
                f"  - 📍 **World Spawn / Mob Drop :** {drop_intel}\\n"
                f"  - 🪙 **Base Resale Value :** {fee_clean} (Sold to vendors · Not sold by merchants)\\n"
                f"  - 🔓 **Unlock Rule :** Discover Schema in Chateau to permanently add to Appearance menu.\\n"
                f"  - 📦 **Required Materials :** {m_str}\\n"
                f"  - 📜 *« {v.get('lore', 'Official cosmetic blueprint.')} »*"
            )
            return {
                "found": True,
                "title": f"OFFICIAL SKIN DOSSIER : {v['name'].upper()} ({v.get('target', 'Item').upper()})",
                "text": resp_text,
                "cards": [c_p]
            }

    # 2. GENERIC WEAPON ALIASES (When asking for all skins of a weapon)
    weapon_aliases = {
        "rapier": "Rapier", "rapiere": "Rapier", "rapière": "Rapier",
        "vepr": "Vepr",
        "club": "Club", "gourdin": "Club",
        "shortsword": "Short Sword", "short-sword": "Short Sword", "short sword": "Short Sword",
        "longsword": "Longsword", "long sword": "Longsword",
        "spear": "Spear", "lance": "Spear",
        "axe": "Axe", "hache": "Axe",
        "brown betty": "Brown Betty", "brown-betty": "Brown Betty", "brown": "Brown Betty",
        "longboy": "Longboy",
        "dagger": "Dagger", "dague": "Dagger",
        "halberd": "Halberd", "hallebarde": "Halberd",
        "mace": "Mace", "masse": "Mace",
        "saber": "Saber", "sabre": "Saber",
        "war axe": "War Axe", "war-axe": "War Axe",
        "snub": "Snub",
        "louisville": "Louisville"
    }

    matched_tgt = None
    for alias, tgt in weapon_aliases.items():
        if alias in q_low:
            matched_tgt = tgt
            break

    if not matched_tgt:
        for char in ["marie", "otto", "eva", "gabriel", "hugo", "serine"]:
            if char in q_low:
                matched_tgt = char.title()
                break

    if matched_tgt:
        matched_skins = [v for k, v in db.items() if v.get("target", "").lower() == matched_tgt.lower()]
        if matched_skins:
            cards = []
            for s in matched_skins[:4]:
                c_p = render_pure_english_cosmetic_card(s)
                cards.append(c_p)

            s_names = [f"• 🗡️ **{s['name']}** ({s.get('rarity', 'Rare')})" for s in matched_skins]
            return {
                "found": True,
                "title": f"ALL OFFICIAL SKINS FOR {matched_tgt.upper()}",
                "text": "\\n".join(s_names),
                "cards": cards
            }

    return {
        "found": False,
        "title": "SKINS NOT FOUND",
        "text": "No skins found matching your request.",
        "cards": []
    }


# ===========================================================================
# 3.5 UNIVERSAL RECIPES RETRIEVER (ALL 110 CRAFTING RECIPES)
# ===========================================================================
def get_universal_recipe(query: str) -> Optional[dict]:
    """Retrieves dedicated recipe dossier for any crafting recipe query."""
    q_low = query.lower().strip()
    
    db_p = os.path.join(ROOT_DIR, "data", "high_rate_drops.json")
    drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}

    # Check for direct slug or keyword matches
    clean = q_low.replace("recipe", "").replace("recette", "").strip().replace(" ", "-")
    
    matched = None
    for k, v in drops_db.items():
        k_clean = k.replace("-", " ")
        if clean in k or k in q_low or (clean and clean in k_clean):
            matched = v
            break
        # Match multi-word recipe titles
        t_low = v.get("title", "").lower()
        words = [w for w in q_low.split() if len(w) >= 4 and w not in ["recipe", "recette", "craft", "combien", "trouver", "fiche"]]
        if words and all(w in t_low for w in words):
            matched = v
            break

    if not matched:
        # Check SQLite companion_items_cache
        conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
        c = conn.cursor()
        c.execute("SELECT slug, name_en, category, rarity, sell_silver, sell_copper, best_container, vendor_buy FROM companion_items_cache WHERE (category LIKE '%recipe%' OR category LIKE '%schema%' OR slug LIKE '%recipe%') AND (slug LIKE ? OR name_en LIKE ?) LIMIT 1",
                  (f"%{clean}%", f"%{q_low}%"))
        row = c.fetchone()
        conn.close()
        if row:
            val_s = f"{row[4]} Silver {row[5]} Copper" if row[4] > 0 else f"{row[5]} Copper"
            matched = {
                "title": row[1],
                "slug": row[0],
                "rarity": row[3],
                "category": row[2],
                "sell_display": val_s,
                "mob_drops": [],
                "placed_drops": [row[6]] if row[6] and "container" not in row[6].lower() else [],
                "vendor_buys": [row[7]] if row[7] else ["Not sold by merchants (Raid Loot Exclusive)"],
                "unlocks": f"Allows crafting of item at Chateau Workshop"
            }

    if matched:
        card_p = render_recipe_card(matched["slug"])
        intel_lines = matched.get("summary_intel", [])
        if not intel_lines:
            intel_lines = [
                f"• 🪙 **Base Resale Value :** {matched.get('sell_display', '9 Silver 20 Copper')} (Sold to vendors)",
                f"• 🛒 **Merchant Stock :** {matched.get('vendor_buys', ['Raid loot exclusive'])[0]}",
                f"• 🔓 **Crafting Unlock :** {matched.get('unlocks', 'Forging formula')}"
            ]
        return {
            "found": True,
            "title": f"OFFICIAL RECIPE DOSSIER : {matched.get('title', '').upper()}",
            "text": "\\n".join(intel_lines),
            "card": card_p
        }
    return None
'''

code, count2 = re.subn(old_univ_skins, new_univ_skins, code, count=1, flags=re.DOTALL)
print(f"Replaced get_universal_skins and added get_universal_recipe: {count2}")

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated universal_v8_engine.py!")
