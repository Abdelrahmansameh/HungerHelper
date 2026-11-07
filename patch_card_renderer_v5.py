import os

p = "co_pilot/card_renderer.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

text_n = text.replace("\r\n", "\n")

# 1. Update imports
old_imp = """from overhaul_v3_cards import render_clean_creature_card, render_clean_character_card, render_clean_gavroche_quest_card, render_clean_dungeon_card
from overhaul_all_cards import render_clean_melee_card
from test_mastery_cards_v2 import render_build_all_trees_view, render_build_stats_summary_by_category"""

new_imp = """from clean_cards_v5 import (
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
from stash_dual_images_v5 import render_real_stash_two_images"""

if old_imp in text_n:
    text_n = text_n.replace(old_imp, new_imp)
else:
    # try replacing line 1
    lines = text_n.split("\n")
    lines[0] = new_imp
    text_n = "\n".join(lines)

# 2. Update render_skin_card
old_skin_fn = """def render_skin_card(skin_query: str, is_french: bool = True) -> str:
    \"\"\"Renders high-resolution cosmetic skin crafting card with real preview and ingredient icons.\"\"\"
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
        
    return render_cosmetic_craft_card_dynamic(best_match, requested_ingredient=q_low)"""

new_skin_fn = """def render_skin_card(skin_query: str, is_french: bool = False) -> str:
    \"\"\"Renders high-resolution cosmetic skin crafting card with real preview and ingredient icons.\"\"\"
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
        
    return render_cosmetic_craft_card_dynamic(best_match, requested_ingredient=q_low)"""

if old_skin_fn in text_n:
    text_n = text_n.replace(old_skin_fn, new_skin_fn)
else:
    print("Warning: old_skin_fn not found verbatim")

# 3. Update build cards
old_bld = """def render_talent_build_card(build_query: str = "", is_french: bool = True) -> str:
    if any(w in build_query.lower() for w in ["resume", "stat", "stats", "selection"]):
        return render_build_stats_summary_by_category()
    return render_build_all_trees_view()

def render_talent_build_cards_both(player_name: str = "Abdallah", level: int = 100):
    p1 = render_build_all_trees_view(player_name=player_name, level=level)
    p2 = render_build_stats_summary_by_category(player_name=player_name, level=level)
    return p1, p2"""

new_bld = """def render_talent_build_card(build_query: str = "", is_french: bool = False) -> str:
    if any(w in build_query.lower() for w in ["resume", "stat", "stats", "selection"]):
        return render_build_stats_summary_card(player_name=player_name if 'player_name' in locals() else "Abdallah")
    return render_all_5_mastery_trees_card()

def render_talent_build_cards_both(player_name: str = "Abdallah", level: int = 100):
    p1 = render_all_5_mastery_trees_card(player_name=player_name, level=level)
    p2 = render_build_stats_summary_card(player_name=player_name, level=level)
    return p1, p2"""

if old_bld in text_n:
    text_n = text_n.replace(old_bld, new_bld)

with open(p, "w", encoding="utf-8") as f:
    f.write(text_n)

print("CARD_RENDERER_UPDATED_SUCCESSFULLY")
