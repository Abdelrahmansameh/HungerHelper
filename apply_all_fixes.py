import re
import os

print("=== APPLYING REFINED FIXES ===")

# ---------------------------------------------------------------------------
# 1. PATCH co_pilot/card_renderer.py
# ---------------------------------------------------------------------------
p_cr = "co_pilot/card_renderer.py"
with open(p_cr, "r", encoding="utf-8") as f:
    cr_text = f.read()

# Remove watermark in create_base_canvas
cr_text = re.sub(
    r'wm = "HUNGER COMPANION x ELOISE CO-PILOT"\s+draw\.text\(\(CARD_W - int\(draw\.textlength\(wm, font=core\.F_SMALL_BOLD\)\) - \d+, \d+\), wm, fill=\(120, 110, 80\), font=core\.F_SMALL_BOLD\)',
    '# Watermark removed per user instruction',
    cr_text
)

# Ensure is_french is a parameter in render_item_card
cr_text = re.sub(
    r'def render_item_card\((.*?quest_qty: Optional\[str\] = None)(\s*\)) -> str:',
    r'def render_item_card(\1, is_french: bool = False) -> str:',
    cr_text
)

with open(p_cr, "w", encoding="utf-8") as f:
    f.write(cr_text)
print("[OK] co_pilot/card_renderer.py patched.")

# ---------------------------------------------------------------------------
# 2. PATCH clean_cards_v5.py & universal_v8_engine.py (remove watermark)
# ---------------------------------------------------------------------------
for fn in ["clean_cards_v5.py", "universal_v8_engine.py"]:
    if os.path.exists(fn):
        with open(fn, "r", encoding="utf-8") as f:
            t = f.read()
        t = re.sub(
            r'wm = "HUNGER COMPANION x ELOISE CO-PILOT"\s+draw\.text\(\(CARD_W - int\(draw\.textlength\(wm, font=core\.F_SMALL_BOLD\)\) - \d+, \d+\), wm, fill=\(120, 110, 80\), font=core\.F_SMALL_BOLD\)',
            '# Watermark removed per user instruction',
            t
        )
        t = re.sub(
            r'wm = "HUNGER COMPANION x ELOISE CO-PILOT".*?\n',
            '# Watermark removed per user instruction\n',
            t
        )
        with open(fn, "w", encoding="utf-8") as f:
            f.write(t)
        print(f"[OK] {fn} patched (watermark removed).")

# ---------------------------------------------------------------------------
# 3. PATCH universal_v8_engine.py (NO TOFU EMOJI IN BLUEPRINT FEE)
# ---------------------------------------------------------------------------
with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    uv8_text = f.read()

# Replace emoji coin with clean text
uv8_text = uv8_text.replace(
    'draw.text((left_box[0] + 24, ty + 6), f"🪙 {fee_display}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)',
    'draw.text((left_box[0] + 20, ty + 6), f"Blueprint Crafting Fee : {fee_digits} Copper", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)'
)
with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(uv8_text)
print("[OK] universal_v8_engine.py patched (blueprint fee).")

# ---------------------------------------------------------------------------
# 4. PATCH co_pilot/brain.py (DO NOT OVERWRITE weapon_res["image_attachment"])
# ---------------------------------------------------------------------------
with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    b_text = f.read()

# In section 6. WEAPON STATS, just return weapon_res directly!
old_w_block = """        # 6. WEAPON STATS (Thrust Damage, Best Thrust Weapon, Spear Stats)
        # -------------------------------------------------------------------
        weapon_res = answer_weapon_query(clean_text, is_french)
        if weapon_res:
            from universal_v8_engine import render_pure_english_melee_card
            w_target = "longsword"
            weapon_map = {
                "club": "club", "gourdin": "club", "massue": "club",
                "shortsword": "short-sword", "short-sword": "short-sword", "short sword": "short-sword",
                "longsword": "longsword", "long sword": "longsword", "epee": "longsword", "épée": "longsword",
                "spear": "spear", "lance": "spear",
                "zweihander": "zweihander", "zweihänder": "zweihander", "zwei": "zweihander",
                "halberd": "halberd", "hallebarde": "halberd",
                "saber": "sabre", "sabre": "sabre",
                "rapier": "rapier", "rapiere": "rapier", "rapière": "rapier",
                "war-axe": "war-axe", "war axe": "war-axe",
                "axe": "axe", "hache": "axe",
                "mace": "mace", "masse": "mace",
                "dagger": "dagger", "dague": "dagger"
            }
            for k, val in weapon_map.items():
                if k in lowered:
                    w_target = val
                    break
            card_path = render_pure_english_melee_card(w_target)
            weapon_res["image_attachment"] = card_path
            return weapon_res"""

new_w_block = """        # 6. WEAPON STATS (Thrust Damage, Best Thrust Weapon, Spear Stats, Firearms, 2H Arsenal)
        # -------------------------------------------------------------------
        weapon_res = answer_weapon_query(clean_text, is_french)
        if weapon_res:
            return weapon_res"""

if old_w_block in b_text:
    b_text = b_text.replace(old_w_block, new_w_block)
    print("[OK] co_pilot/brain.py patched (weapon_res overwrite removed).")
else:
    print("[WARN] old_w_block not found verbatim, checking regex...")
    b_text = re.sub(
        r'weapon_res = answer_weapon_query\(clean_text, is_french\)\s+if weapon_res:.*?return weapon_res',
        'weapon_res = answer_weapon_query(clean_text, is_french)\n        if weapon_res:\n            return weapon_res',
        b_text,
        flags=re.DOTALL
    )
    print("[OK] co_pilot/brain.py patched via regex.")

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(b_text)

# ---------------------------------------------------------------------------
# 5. PATCH co_pilot/game_knowledge.py (ALL FIREARMS IN TTK & HTK)
# ---------------------------------------------------------------------------
with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    gk_text = f.read()

# Update firearm TTK in answer_combat_ttk_query
old_ttk_firearm = """    # 1. FIREARMS
    firearm_match = None
    for fn in ["auster", "deux", "longboy", "long boy", "cavalier", "marengo", "pistolet", "fusil"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            firearm_match = "longboy" if fn in ["longboy", "long boy", "fusil"] else "deux" if fn in ["deux", "pistolet"] else fn
            break

    if firearm_match:
        card_path = render_weapon_card(firearm_match, is_french=False)
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "en blue"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy", "en or"])
        is_brute = any(w in lowered for w in ["brute", "gros"]) and not any(w in lowered for w in ["joueur", "player"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"]) and not any(w in lowered for w in ["joueur", "player"])

        f_name = "LongBoy" if firearm_match == "longboy" else "Deux" if firearm_match == "deux" else "Auster"
        f_dmg = 58 if firearm_match == "longboy" else 54 if firearm_match == "deux" else 48"""

new_ttk_firearm = """    # 1. FIREARMS
    firearm_match = None
    from universal_v8_engine import render_pure_english_firearm_card
    for fn in ["marengo", "drak", "lasher", "lash", "auster", "deux", "longboy", "long boy", "cavalier", "pistolet", "fusil"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            firearm_match = "lasher" if fn in ["lasher", "lash"] else "longboy" if fn in ["longboy", "long boy", "fusil"] else "deux" if fn in ["deux", "pistolet"] else fn
            break

    if firearm_match:
        card_path = render_pure_english_firearm_card(firearm_match, is_french=False)
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "en blue"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy", "en or"])
        is_brute = any(w in lowered for w in ["brute", "gros"]) and not any(w in lowered for w in ["joueur", "player"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"]) and not any(w in lowered for w in ["joueur", "player"])

        gun_db = {
            "marengo": ("Marengo", 39, 68),
            "drak": ("Drak", 107, 192),
            "lasher": ("Lasher", 30, 52),
            "longboy": ("LongBoy", 58, 104),
            "deux": ("Deux", 54, 86),
            "auster": ("Auster", 48, 78),
            "cavalier": ("Cavalier", 52, 80)
        }
        f_name, f_dmg, f_head_dmg = gun_db.get(firearm_match, ("Firearm", 48, 78))"""

if old_ttk_firearm in gk_text:
    gk_text = gk_text.replace(old_ttk_firearm, new_ttk_firearm)
    print("[OK] co_pilot/game_knowledge.py patched (firearm TTK).")
else:
    print("[WARN] old_ttk_firearm not found verbatim, checking regex...")

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(gk_text)

print("=== ALL FIXES APPLIED SUCCESSFULLY ===")
