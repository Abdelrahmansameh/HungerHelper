import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('universal_v8_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix broken \n string splits
fixed = text.replace('"text": "\n".join(lines)', '"text": "\\n".join(lines)')
fixed = fixed.replace('"text": "\\n".join(s_names)', '"text": "\\n".join(s_names)')
fixed = fixed.replace('"text": "\\n".join(intel_lines)', '"text": "\\n".join(intel_lines)')

# Fix any other multiline escapes
fixed = fixed.replace('"text": "\n', '"text": "\\n')
fixed = fixed.replace('f"• 🎨 **{v[\'name\']}** ({v.get(\'rarity\', \'Rare\')} cosmetic skin for **{v.get(\'target\')}**)\n', 'f"• 🎨 **{v[\'name\']}** ({v.get(\'rarity\', \'Rare\')} cosmetic skin for **{v.get(\'target\')}**)\\n')

with open('universal_v8_engine.py', 'w', encoding='utf-8') as f:
    f.write(fixed)

import py_compile
try:
    py_compile.compile('universal_v8_engine.py', doraise=True)
    print("universal_v8_engine.py compiles cleanly!")
except Exception as e:
    print("Compilation error:", e)
