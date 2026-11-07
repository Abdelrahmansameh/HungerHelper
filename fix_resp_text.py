with open('universal_v8_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_resp = [
    '            resp_lines = [\n',
    '                f"• 🎨 **{v[\'name\']}** ({v.get(\'rarity\', \'Rare\')} cosmetic skin for **{v.get(\'target\')}**)",\n',
    '                f"  - 📍 **World Spawn / Mob Drop :** {drop_intel}",\n',
    '                f"  - 🪙 **Base Resale Value :** {fee_clean} (Sold to vendors · Not sold by merchants)",\n',
    '                f"  - 🔓 **Unlock Rule :** Discover Schema in Chateau to permanently add to Appearance menu.",\n',
    '                f"  - 📦 **Required Materials :** {m_str}",\n',
    '                f"  - 📜 *« {v.get(\'lore\', \'Official cosmetic blueprint.\')} »*"\n',
    '            ]\n',
    '            resp_text = "\\n".join(resp_lines)\n'
]

# Lines 571 to 582 (1-based), so index 570 to 582
out_lines = lines[:570] + new_resp + lines[582:]

with open('universal_v8_engine.py', 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

import py_compile
py_compile.compile('universal_v8_engine.py', doraise=True)
print("universal_v8_engine.py compiled successfully!")
