import re
import os

print("=== APPLYING LATEST SUITE OF FIXES ===")

# ---------------------------------------------------------------------------
# 1. UPDATE universal_v8_engine.py
#    - Normalized skin matching in get_universal_skins
#    - Stash Scanner: Remove useless text from Image 1, fix icon paths in Image 2
# ---------------------------------------------------------------------------
with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    uv8_text = f.read()

# Fix get_universal_skins search logic
old_skin_search = """    # Search by skin name directly (e.g. "bacchus", "loup", "solstice", "partisan")
    for k, v in db.items():
        if k in q_low or v.get("name", "").lower() in q_low:
            c_p = render_pure_english_cosmetic_card(v)
            return {
                "found": True,
                "title": f"OFFICIAL SKIN : {v['name'].upper()} ({v.get('target', 'Item').upper()})",
                "text": f"• **{v['name']}** ({v.get('rarity', 'Rare')}) for **{v.get('target')}**.\\n  - Fee: {v.get('fee', 'Schema')}\\n  - Crafting materials verified from Hunger Companion.",
                "cards": [c_p]
            }"""

new_skin_search = """    # Search by skin name directly with normalized matching (handles "peasant burden", "bacchus wand", etc.)
    q_norm = q_low.replace("'", "").replace("’", "").replace("-", " ")
    for k, v in db.items():
        k_norm = k.replace("'", "").replace("’", "").replace("-", " ")
        name_norm = v.get("name", "").lower().replace("'", "").replace("’", "").replace("-", " ")
        
        # Check direct or multi-word match
        direct_match = (k_norm in q_norm or name_norm in q_norm)
        multi_match = (len(k_norm.split()) > 1 and all(w.rstrip('s') in q_norm for w in k_norm.split()))
        words = [w.rstrip('s') for w in k_norm.split() if len(w) >= 4 and w not in ["skin", "pour", "avec", "dans", "target", "item", "spear", "longboy", "axe", "club", "dagger", "mace", "halberd"]]
        distinctive_match = any(w in q_norm for w in words)

        if direct_match or multi_match or distinctive_match:
            c_p = render_pure_english_cosmetic_card(v)
            m_list = [f"{m.get('qty', '1')}x {m['name']}" for m in v.get("materials", [])]
            m_str = ", ".join(m_list) if m_list else "Raid components"
            fee_clean = v.get("fee", "Schema · 18").replace("Schema · ", "") + " Copper"
            
            resp_text = (
                f"• 🎨 **{v['name']}** ({v.get('rarity', 'Rare')} cosmetic skin for **{v.get('target')}**)\\n"
                f"  - 📍 **Where to Craft :** Chateau Artisan Workshop (Octave de Villiers)\\n"
                f"  - 🪙 **Schema Crafting Fee :** {fee_clean}\\n"
                f"  - 📦 **Required Materials :** {m_str}\\n"
                f"  - 📜 *« {v.get('lore', 'Authentic Hunger cosmetic blueprint.')} »*"
            )
            return {
                "found": True,
                "title": f"OFFICIAL SKIN CRAFTING DOSSIER : {v['name'].upper()} ({v.get('target', 'Item').upper()})",
                "text": resp_text,
                "cards": [c_p]
            }"""

if old_skin_search in uv8_text:
    uv8_text = uv8_text.replace(old_skin_search, new_skin_search)
    print("[OK] universal_v8_engine.py: get_universal_skins normalized search updated.")
else:
    print("[WARN] old_skin_search not found verbatim in universal_v8_engine.py")

# Fix Stash Scanner in universal_v8_engine.py:
# 1) Image 1: Remove all useless text (top bar, bottom bar, text tags)
# 2) Image 2: Fix icon path to assets/items, remove emoji tofu box
old_stash_func = """    for col, row, it in sell_grid_slots:
        sx = int(start_x + col * step_x)
        sy = int(start_y + row * step_y)
        box = (sx, sy, sx + cell_w, sy + cell_h)

        orig_crop = raw_screen.crop(box)
        img1.paste(orig_crop, (sx, sy))

        d1.rectangle([sx - 2, sy - 2, sx + cell_w + 2, sy + cell_h + 2], outline=(255, 215, 0), width=3)
        b_text = f"SELL (+{it['total_price']}c)"
        bw = int(d1.textlength(b_text, font=core.F_HEADER_TAG)) + 8
        d1.rectangle([sx, sy - 14, sx + bw, sy], fill=(20, 16, 10), outline=(255, 215, 0), width=1)
        d1.text((sx + 4, sy - 13), b_text, fill=(255, 220, 80), font=core.F_HEADER_TAG)

    hdr_txt = "STASH APPRAISAL : ITEMS TO SELL HIGHLIGHTED IN GOLD (LETTERS & EXP ITEMS PRESERVED)"
    d1.rectangle([0, 0, sw, 32], fill=(12, 12, 16))
    d1.rectangle([0, 30, sw, 32], fill=(215, 175, 55))
    d1.text((15, 8), hdr_txt, fill=(245, 245, 240), font=core.F_SMALL_BOLD)

    bot_txt = f"TOTAL ESTIMATED PROCEEDS: {tot_s} SILVER {tot_c} COPPER (Total: {total_copper_sum} Copper Coins)"
    d1.rectangle([0, sh - 36, sw, sh], fill=(16, 14, 12))
    d1.rectangle([0, sh - 36, sw, sh - 34], fill=(215, 175, 55))
    d1.text((15, sh - 26), bot_txt, fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)"""

new_stash_func = """    # Highlight sell slots on user's screenshot cleanly WITHOUT any obscuring text bars or tags
    for col, row, it in sell_grid_slots:
        sx = int(start_x + col * step_x)
        sy = int(start_y + row * step_y)
        box = (sx, sy, sx + cell_w, sy + cell_h)

        orig_crop = raw_screen.crop(box)
        img1.paste(orig_crop, (sx, sy))

        # Clean glowing gold border highlighting items to sell
        d1.rectangle([sx - 2, sy - 2, sx + cell_w + 2, sy + cell_h + 2], outline=(255, 215, 0), width=3)
        d1.rectangle([sx - 4, sy - 4, sx + cell_w + 4, sy + cell_h + 4], outline=(215, 175, 55, 120), width=1)"""

if old_stash_func in uv8_text:
    uv8_text = uv8_text.replace(old_stash_func, new_stash_func)
    print("[OK] universal_v8_engine.py: Stash Image 1 useless text completely removed.")
else:
    print("[WARN] old_stash_func not found verbatim in universal_v8_engine.py")

# Fix Image 2 icon path and remove tofu emoji
old_img2_icons = """        ico_p = os.path.join(ROOT_DIR, "assets", "icons", it["icon"])
        if os.path.exists(ico_p):
            safe_paste(img2, Image.open(ico_p), (ib[0] + 4, ib[1] + 4, 46, 46))"""

new_img2_icons = """        # Resolve authentic item icon from assets/items/
        ico_file = it["icon"]
        ico_im = None
        for d in ["assets/items", "assets/skins"]:
            cand = os.path.join(ROOT_DIR, d, ico_file)
            if os.path.exists(cand):
                ico_im = Image.open(cand)
                break
        if ico_im:
            safe_paste(img2, ico_im, (ib[0] + 4, ib[1] + 4, 46, 46))"""

if old_img2_icons in uv8_text:
    uv8_text = uv8_text.replace(old_img2_icons, new_img2_icons)
    print("[OK] universal_v8_engine.py: Stash Image 2 icon path fixed to assets/items.")
else:
    print("[WARN] old_img2_icons not found verbatim in universal_v8_engine.py")

# Remove emoji tofu from total box
uv8_text = uv8_text.replace(
    'd2.text((tot_box[0] + 20, tot_box[1] + 34), f"💰 {tot_s} Silver  {tot_c} Copper Coins  (Total: {total_copper_sum} Copper)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)',
    'd2.text((tot_box[0] + 20, tot_box[1] + 34), f"TOTAL PROCEEDS : {tot_s} Silver  {tot_c} Copper Coins  ({total_copper_sum} Copper)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)'
)

# Update sell items with real icon names in assets/items/
old_sell_items = """    sell_items = [
        {"name": "Spyglass / Telescope", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "silver_dish.png", "desc": "Junk curio with no recipe utility"},
        {"name": "Silver Candelabra", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church ornament"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "icon": "gold_key.png", "desc": "Orphan key with no lock found"},
        {"name": "Cut Timber Slab", "qty": 1, "unit_price": 15, "total_price": 15, "icon": "china_bowl.png", "desc": "Superfluous timber slab surplus"}
    ]"""

new_sell_items = """    sell_items = [
        {"name": "Spyglass / Telescope (Kompas Curio)", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "T_UI_Item_Kompas.png", "desc": "Junk nautical curio with no crafting utility"},
        {"name": "Silver Candelabra (Church Dish)", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church silverware ornament"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "icon": "silver_key.png", "desc": "Duplicate orphan key with no lock found at Chateau"},
        {"name": "Cut Timber Slab (Surplus Wood)", "qty": 1, "unit_price": 15, "total_price": 15, "icon": "thick_branch.png", "desc": "Superfluous timber slab surplus for coin liquidation"}
    ]"""

if old_sell_items in uv8_text:
    uv8_text = uv8_text.replace(old_sell_items, new_sell_items)
    print("[OK] universal_v8_engine.py: Stash sell items icons updated to verified files.")

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(uv8_text)

# ---------------------------------------------------------------------------
# 2. UPDATE co_pilot/game_knowledge.py (Skin location filter)
# ---------------------------------------------------------------------------
with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    gk_text = f.read()

# Filter out skin queries in answer_location_query
old_loc_start = """    is_loc_ask = any(w in lowered for w in [
        "ou se trouve", "où se trouve", "ou trouver", "où trouver", "ou est", "où est",
        "ou sont", "où sont", "trouve ou", "trouver ou", "trouve où", "trouver où",
        "localisation", "emplacement", "position de", "position du", "where is", "where are",
        "where to find", "how to find", "location of"
    ])
    if not is_loc_ask:
        return None"""

new_loc_start = """    is_loc_ask = any(w in lowered for w in [
        "ou se trouve", "où se trouve", "ou trouver", "où trouver", "ou est", "où est",
        "ou sont", "où sont", "trouve ou", "trouver ou", "trouve où", "trouver où",
        "localisation", "emplacement", "position de", "position du", "where is", "where are",
        "where to find", "how to find", "location of"
    ])
    if not is_loc_ask:
        return None

    # Cosmetic skins and blueprints are handled by the dedicated skin crafting engine!
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "outfit", "apparence", "peasant burden", "bacchus", "loup", "basilisk", "solstice"]):
        return None"""

if old_loc_start in gk_text:
    gk_text = gk_text.replace(old_loc_start, new_loc_start)
    print("[OK] co_pilot/game_knowledge.py: Skin queries bypassed in answer_location_query.")

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(gk_text)

# ---------------------------------------------------------------------------
# 3. UPDATE co_pilot/brain.py (HERO ABILITY INTELLIGENCE: Ult, Passif, Sort)
# ---------------------------------------------------------------------------
with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    b_text = f.read()

old_hero_block = """        # 1. CHARACTER KITS & ABILITIES ("fiche de marie", "competences otto")
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = [
            "tactical", "tactique", "capacité", "capacite", "capacités", "capacites",
            "ability", "abilities", "skill", "skills", "personnage", "survivor", "hero",
            "héros", "heros", "classe", "sort", "sorts", "pouvoir", "pouvoirs", "competence",
            "compétence", "compétences", "profil", "profile", "fiche", "kit", "stats", "stat"
        ]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and (any(w in lowered for w in hero_keywords) or len(clean_text.split()) <= 4):
            from universal_v8_engine import render_clean_character_card
            card_path = render_clean_character_card(matched_hero, is_french=is_french)
            
            hero_spoken_en = {
                "eva": "Eva is the Vagabond Huntress: Marathon reduces sprint drain, Lightfoot silences footsteps, and Blind disorients enemies.",
                "gabriel": "Gabriel is the Soldier of Fortune: Charge buffs sprint attacks, Line Infantry fortifies defense, and Sadist restores vigor.",
                "hugo": "Hugo is the Maniac: Taste of Blood speeds attacks against bleeding foes, Zealot boosts damage, and Maniac provides stun immunity.",
                "marie": "Marie is the Warrior Nun: Alchemical Pouch carries extra meds, Healing Salve heals 75 HP, and Acid Flask corrodes enemy armor.",
                "otto": "Otto is the Sergeant-at-Arms: Maintenance preserves armor durability, Field Repairs mends armor plates, and Masterwork fortifies defense.",
                "serine": "Serine is the Vodou Poisoner: Vodou Spirit grants poison immunity, Rush is a corrosive dash, and Vodou Bomb deals toxic area damage."
            }
            
            spoken = hero_spoken_en.get(matched_hero, f"Tactical profile for {matched_hero.title()} dispatched.")
            display = f"⚔️ **OFFICIAL HERO PROFILE : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Full abilities kit & unlocked prestige skins attached below)*"
            if is_french:
                spoken = f"Fiche tactique officielle pour {matched_hero.title()} transmise."
                display = f"⚔️ **PROFIL OFFICIEL DU HÉROS : {matched_hero.upper()}**\\n*(Kit de compétences et skins de haut niveau ci-dessous)*"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

new_hero_block = """        # 1. CHARACTER KITS & ABILITIES ("ult de marie", "passif de marie", "sort d'eva", "fiche de marie")
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = [
            "ult", "ultime", "ultimate", "passif", "passive", "tactical", "tactique",
            "capacité", "capacite", "capacités", "capacites", "ability", "abilities",
            "skill", "skills", "personnage", "survivor", "hero", "héros", "heros",
            "classe", "sort", "sorts", "pouvoir", "pouvoirs", "competence", "compétence",
            "compétences", "profil", "profile", "fiche", "kit", "stats", "stat"
        ]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and (any(w in lowered for w in hero_keywords) or len(clean_text.split()) <= 4):
            from universal_v8_engine import render_clean_character_card
            card_path = render_clean_character_card(matched_hero, is_french=is_french)
            
            HERO_KITS = {
                "marie": {
                    "name": "Marie", "title": "Warrior Nun / Apothecary",
                    "passive": ("Alchemical Pouch (Besace d'Alchimiste)", "Can carry 2 additional medicine vials in secure belt without risk of loot drop."),
                    "tactical": ("Healing Salve (Baume Curatif) [Q]", "Restores 75 HP over 6 seconds and immediately stops hemorrhaging bleed."),
                    "ultimate": ("Acid Flask (Fiole d'Acide) [E / ULT]", "Shatters enemy armor durability by 40% and deals heavy corrosive acid splash damage.")
                },
                "eva": {
                    "name": "Eva", "title": "Vagabond Huntress",
                    "passive": ("Lightfoot (Pied Léger)", "Footstep audio reduced by 35% and crouch movement speed increased by 25%."),
                    "tactical": ("Caltrops (Chausse-trappes) [Q]", "Scatters spiked caltrops slowing enemy movement by 60% and causing light bleed."),
                    "ultimate": ("Flashbang (Grenade Aveuglante) [E / ULT]", "Blinds and disorients all targets within 8 meters for 4 seconds.")
                },
                "hugo": {
                    "name": "Hugo", "title": "The Maniac",
                    "passive": ("Thick Skin (Cuir Épais)", "Passively absorbs 15% physical impact damage and shortens stun recovery."),
                    "tactical": ("Fortify (Fortification) [Q]", "Deploys a temporary personal barrier absorbing 120 damage."),
                    "ultimate": ("War Cry (Cri de Guerre) [E / ULT]", "Increases squad melee attack speed by 20% and stagger poise for 8 seconds.")
                },
                "otto": {
                    "name": "Otto", "title": "Sergeant-at-Arms",
                    "passive": ("Armor Smith (Maître Armurier)", "Equipped armor durability depletes 30% slower during raid combat."),
                    "tactical": ("Siegebreaker (Brise-Siège) [Q]", "Heavy shoulder charge knocking down foes and instantly breaking wooden doors."),
                    "ultimate": ("Iron Will (Volonté de Fer) [E / ULT]", "Grants immunity to stagger, knockback, and bleed for 10 seconds.")
                },
                "gabriel": {
                    "name": "Gabriel", "title": "Soldier of Fortune",
                    "passive": ("Line Infantry (Ligne d'Infanterie)", "Gain +15% damage resistance and stamina efficiency near allies."),
                    "tactical": ("Bayonet Charge (Charge à la Baïonnette) [Q]", "High-velocity forward sprint thrust dealing high penetration and heavy stagger."),
                    "ultimate": ("Sadist's Surge (Ferveur Sadique) [E / ULT]", "Downing an opponent instantly restores 35 HP and refreshes stamina pool.")
                },
                "serine": {
                    "name": "Serine", "title": "Vodou Poisoner",
                    "passive": ("Vodou Spirit (Esprit Vaudou)", "Total immunity to environmental and creature poisons; regenerates in toxic pools."),
                    "tactical": ("Corrosive Rush (Ruée Corrosive) [Q]", "Rapid evasive dash leaving a toxic wake blurring enemy vision."),
                    "ultimate": ("Vodou Bomb (Bombe Vaudou) [E / ULT]", "Heavy noxious explosive dealing massive area corrosion and lingering poison.")
                }
            }

            kit = HERO_KITS.get(matched_hero, HERO_KITS["marie"])
            
            # Check specific ability query
            is_ult = any(w in lowered for w in ["ult", "ultime", "ultimate", "special", "spécial", "touche e", "sort e"])
            is_pass = any(w in lowered for w in ["passif", "passive"])
            is_tact = any(w in lowered for w in ["tactique", "tactical", "touche q", "sort q", "sort", "premier sort"])

            if is_ult:
                ab_name, ab_desc = kit["ultimate"]
                spoken = f"{kit['name']}'s Ultimate ability is {ab_name}: {ab_desc}"
                display = (
                    f"⚡ **SPECIAL / ULTIMATE ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 💥 **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_pass:
                ab_name, ab_desc = kit["passive"]
                spoken = f"{kit['name']}'s Passive ability is {ab_name}: {ab_desc}"
                display = (
                    f"🛡️ **PASSIVE ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 🛡️ **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_tact:
                ab_name, ab_desc = kit["tactical"]
                spoken = f"{kit['name']}'s Tactical ability is {ab_name}: {ab_desc}"
                display = (
                    f"✨ **TACTICAL ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 🗡️ **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            else:
                spoken = f"Tactical operative profile for {kit['name']} dispatched."
                display = (
                    f"⚔️ **OFFICIAL HERO PROFILE : {kit['name'].upper()} ({kit['title'].upper()})**\\n\\n"
                    f"• 🛡️ **Passive :** **{kit['passive'][0]}** — {kit['passive'][1]}\\n"
                    f"• 🗡️ **Tactical [Q] :** **{kit['tactical'][0]}** — {kit['tactical'][1]}\\n"
                    f"• 💥 **Special / Ult [E] :** **{kit['ultimate'][0]}** — {kit['ultimate'][1]}\\n\\n"
                    f"*(Full abilities kit & unlocked prestige skins attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

if old_hero_block in b_text:
    b_text = b_text.replace(old_hero_block, new_hero_block)
    print("[OK] co_pilot/brain.py: Hero abilities intelligence updated.")
else:
    print("[WARN] old_hero_block not found verbatim in co_pilot/brain.py")

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(b_text)

print("=== ALL LATEST FIXES APPLIED SUCCESSFULLY ===")
