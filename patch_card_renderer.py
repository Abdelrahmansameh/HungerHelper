import os
import re

with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace render_weapon_card entirely with modern router
old_weapon_def_pattern = re.compile(r"def render_weapon_card\(weapon_slug_or_name: str.*?(?=\n# ---|\ndef render_quest_card)", re.DOTALL)

new_weapon_def = '''def render_weapon_card(weapon_slug_or_name: str, is_french: bool = False) -> str:
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
'''

content = old_weapon_def_pattern.sub(new_weapon_def, content)

# Ensure render_character_card and render_creature_card default to is_french=False
content = content.replace('def render_character_card(char_key: str) -> str:\n    return render_clean_character_card(char_key, is_french=True)',
                          'def render_character_card(char_key: str) -> str:\n    from universal_v8_engine import render_clean_character_card\n    return render_clean_character_card(char_key, is_french=False)')

content = content.replace('def render_creature_card(creature_key: str, is_french: bool = True) -> str:\n    return render_clean_creature_card(creature_key, is_french)',
                          'def render_creature_card(creature_key: str, is_french: bool = False) -> str:\n    from universal_v8_engine import render_universal_creature_card\n    return render_universal_creature_card(creature_key, is_french=is_french)')

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated co_pilot/card_renderer.py successfully!")
