with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    cr = f.read().replace("\r\n", "\n")

import_addition = "from overhaul_all_cards import render_clean_melee_card, render_clean_creature_card, render_clean_character_card, render_clean_gavroche_quest_card, render_clean_dungeon_card\n"

# In render_weapon_card:
old_melee_part = """    # 2. MELEE WEAPONS (Zweihander, Spear, Halberd, Sabre, Axe, Dagger)"""
new_melee_part = """    # 2. MELEE WEAPONS (Zweihander, Spear, Halberd, Sabre, Axe, Dagger, Longsword)
    return render_clean_melee_card(weapon_slug_or_name, is_french)"""

if old_melee_part in cr and new_melee_part not in cr:
    # replace everything from old_melee_part to return in render_weapon_card
    idx = cr.find(old_melee_part)
    end_fn = cr.find("def render_quest_card", idx)
    cr = cr[:idx] + new_melee_part + "\n\n\n# ---------------------------------------------------------------------------\n" + cr[end_fn:]
    print("SUCCESS: render_weapon_card updated to call render_clean_melee_card!")

# In render_quest_card:
old_quest_def = """def render_quest_card(quest_query: str, is_french: bool = True) -> str:"""
new_quest_def = """def render_quest_card(quest_query: str, is_french: bool = True) -> str:
    return render_clean_gavroche_quest_card(is_french)"""

if old_quest_def in cr and new_quest_def not in cr:
    idx_q = cr.find(old_quest_def)
    end_q = cr.find("def render_creature_card", idx_q)
    cr = cr[:idx_q] + new_quest_def + "\n\n\n# ---------------------------------------------------------------------------\n" + cr[end_q:]
    print("SUCCESS: render_quest_card updated to call render_clean_gavroche_quest_card!")

# In render_creature_card:
old_creat_def = """def render_creature_card(creature_key: str, is_french: bool = True) -> str:"""
new_creat_def = """def render_creature_card(creature_key: str, is_french: bool = True) -> str:
    return render_clean_creature_card(creature_key, is_french)"""

if old_creat_def in cr and new_creat_def not in cr:
    idx_c = cr.find(old_creat_def)
    end_c = cr.find("def render_character_card", idx_c)
    cr = cr[:idx_c] + new_creat_def + "\n\n\n# ---------------------------------------------------------------------------\n" + cr[end_c:]
    print("SUCCESS: render_creature_card updated to call render_clean_creature_card!")

# In render_character_card:
old_char_def = """def render_character_card(char_key: str) -> str:"""
new_char_def = """def render_character_card(char_key: str) -> str:
    return render_clean_character_card(char_key, is_french=True)"""

if old_char_def in cr and new_char_def not in cr:
    idx_ch = cr.find(old_char_def)
    end_ch = cr.find("def render_skin_card", idx_ch)
    cr = cr[:idx_ch] + new_char_def + "\n\n\n# ---------------------------------------------------------------------------\n" + cr[end_ch:]
    print("SUCCESS: render_character_card updated to call render_clean_character_card!")

# In render_dungeon_card:
old_dung_def = """def render_dungeon_card(dungeon_key: str = \"jacques-folly\", is_french: bool = True) -> str:"""
new_dung_def = """def render_dungeon_card(dungeon_key: str = \"jacques-folly\", is_french: bool = True) -> str:
    return render_clean_dungeon_card(is_french)"""

if old_dung_def in cr and new_dung_def not in cr:
    idx_d = cr.find(old_dung_def)
    end_d = cr.find("def render_stash_report_card", idx_d)
    cr = cr[:idx_d] + new_dung_def + "\n\n\n# ---------------------------------------------------------------------------\n" + cr[end_d:]
    print("SUCCESS: render_dungeon_card updated to call render_clean_dungeon_card!")

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(import_addition + cr)

print("card_renderer.py fully linked to overhauled clean cards!")
