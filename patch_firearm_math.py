import math

with open('co_pilot/game_knowledge.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        if is_naked:
            t_name, t_head, t_body = "Naked Player (100 HP)", 1, 2
        elif is_blue:
            t_name, t_head, t_body = "Blue / Sapper Armor Player (160 HP)", 2, 4
        elif is_legend:
            t_name, t_head, t_body = "Legendary Armor Player (200 HP)", 3, 5
        elif is_brute:
            t_name, t_head, t_body = "Brute (900 HP)", 9, 18
        elif is_drooler:
            t_name, t_head, t_body = "Drooler (450 HP)", 5, 10
        else:
            t_name, t_head, t_body = "Green Armor Player (140 HP)", 2, 3"""

replacement = """        if is_naked:
            t_name, target_hp = "Naked Player (100 HP)", 100
        elif is_blue:
            t_name, target_hp = "Blue / Sapper Armor Player (160 HP)", 160
        elif is_legend:
            t_name, target_hp = "Legendary Armor Player (200 HP)", 200
        elif is_brute:
            t_name, target_hp = "Brute (900 HP)", 900
        elif is_drooler:
            t_name, target_hp = "Drooler (450 HP)", 450
        else:
            t_name, target_hp = "Green Armor Player (140 HP)", 140

        t_head = max(1, math.ceil(target_hp / f_head_dmg))
        t_body = max(1, math.ceil(target_hp / f_dmg))"""

if target in text:
    text = text.replace(target, replacement)
    with open('co_pilot/game_knowledge.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Firearm math dynamic calculation patched!")
else:
    print("Target not found!")
