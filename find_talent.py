import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('co_pilot/card_renderer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['ARBRE', 'Joueur', 'PHYSIOLOG', 'render_talent_build_card']):
        print(f"{i+1}: {line.strip()}")
