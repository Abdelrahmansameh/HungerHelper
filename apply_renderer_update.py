import sys

with open("co_pilot/card_renderer.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 1. Update find_item_icon
old_alias_end = '"brute": "brute_foot.png"\n    }'
new_alias_additions = '''"brute": "brute_foot.png",
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
    }'''

assert old_alias_end in content, "old_alias_end not found!"
content = content.replace(old_alias_end, new_alias_additions, 1)

# Improve return in find_item_icon
old_fallback = '    return core.CONTAINER_IMGS.get("strongbox.webp")'
new_fallback = '''    # Check assets/items dynamically
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
    return core.CONTAINER_IMGS.get("strongbox.webp")'''

assert old_fallback in content, "old_fallback not found!"
content = content.replace(old_fallback, new_fallback, 1)

# 2. Update render_item_card for Moist Pouch
old_item_branch = '            if "flour" in item_name.lower():'
new_item_branch = '''            if "moist" in item_name.lower() or "pouch" in item_name.lower() or "poche" in item_name.lower():
                item_type = "Besaces & Sacs (Bags)"
                name_fr, name_en = "Poche Humide", "Moist Pouch"
                desc = "Besace de hanche de taille et forme testiculaire. Indispensable pour confectionner le skin d'arme Épique Bacchus' Wand (Longboy)."
                best_source = "Old Cabinet (1/6.13)"
                drop_rate = "16.3% (Élevé)"
                sell_silver = 0
                sell_copper = 38
                buy_vendor = "Octave de Villiers, Piro (38s 27c)"
            elif "flour" in item_name.lower():'''

assert old_item_branch in content, "old_item_branch not found!"
content = content.replace(old_item_branch, new_item_branch, 1)

# Update craft/quest panel in render_item_card for Moist Pouch
old_quest_panel = '    if quest_name:\n        draw.text((q_box[0] + 16, q_box[1] + 38), f"• Quête Associée : {quest_name} (Donneur : {quest_giver or \'Château\'})", fill=core.COLOR_PARCHMENT, font=core.F_BODY)'
new_quest_panel = '''    if "moist" in item_name.lower() or "pouch" in item_name.lower() or "poche" in item_name.lower():
        draw.text((q_box[0] + 16, q_box[1] + 36), "• Usage Cosmétique : Indispensable pour forger le skin Épique « Bacchus' Wand » (Longboy)", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
        draw.text((q_box[0] + 16, q_box[1] + 60), "• Recette : 1x Moist Pouch + Gelée Royale + Tige Polie + Perle Blanche + Défense d'Ivoire", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((q_box[0] + 16, q_box[1] + 84), "• Déblocage au Château : Schéma requis à l'Atelier d'Artisanat (210 Cuivres)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    elif quest_name:
        draw.text((q_box[0] + 16, q_box[1] + 38), f"• Quête Associée : {quest_name} (Donneur : {quest_giver or 'Château'})", fill=core.COLOR_PARCHMENT, font=core.F_BODY)'''

assert old_quest_panel in content, "old_quest_panel not found!"
content = content.replace(old_quest_panel, new_quest_panel, 1)

# 3. Replace render_skin_card with dynamic full implementation
old_skin_card_start = 'def render_skin_card(skin_query: str, is_french: bool = True) -> str:'
idx_skin = content.find(old_skin_card_start)
assert idx_skin != -1, "old_skin_card_start not found!"

# Find end of render_skin_card
idx_stash = content.find("def render_stash_report_card", idx_skin)
assert idx_stash != -1, "render_stash_report_card not found!"

new_skin_card_code = '''def render_skin_card(skin_query: str, is_french: bool = True) -> str:
    """Renders high-resolution cosmetic skin crafting card with real preview and ingredient icons."""
    from cosmetic_card_builder import render_cosmetic_craft_card_dynamic
    
    db_p = os.path.join(ROOT_DIR, "data", "full_skins_database.json")
    db = {}
    if os.path.exists(db_p):
        with open(db_p, "r", encoding="utf-8") as jf:
            db = json.load(jf)
            
    q_low = skin_query.lower().strip()
    
    # Moist pouch / Bacchus / Longboy
    if any(w in q_low for w in ["moist", "pouch", "poche", "bacchus", "longboy"]):
        bacchus_data = db.get("bacchus' wand")
        if bacchus_data:
            return render_cosmetic_craft_card_dynamic(bacchus_data, requested_ingredient="moist pouch")
            
    # Search by skin name
    best_match = None
    for k, v in db.items():
        if k in q_low or v.get("name", "").lower() in q_low:
            best_match = v
            break
            
    # Search by character
    if not best_match:
        for char in ["marie", "eva", "hugo", "gabriel", "otto", "serine"]:
            if char in q_low:
                for k, v in db.items():
                    if f"({char})" in k or v.get("target", "").lower() == char:
                        best_match = v
                        break
                if best_match:
                    break
                    
    if not best_match:
        best_match = db.get("bacchus' wand") or list(db.values())[0]
        
    return render_cosmetic_craft_card_dynamic(best_match, requested_ingredient=q_low)


# ---------------------------------------------------------------------------
'''

content = content[:idx_skin] + new_skin_card_code + content[idx_stash:]

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated co_pilot/card_renderer.py successfully!")
