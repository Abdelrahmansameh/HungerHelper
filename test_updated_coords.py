import perfect_briefings_core_v24 as core
import generate_perfect_briefings_v24 as gen

print("Testing to_map_coord for updated points:")
test_points = [
    ("Chapel Altar (Sarlat)", 3034.16, 2512.26),
    ("Book 1: Rozier (Windmill)", 1259.35, 1065.22),
    ("Book 2: Census (Farmhouse)", 2446.74, 1550.63),
    ("Book 3: Catechisme (Chapel)", 3048.29, 2488.7),
    ("Book 4: Montesquieu (Tower)", 1391.83, 1535.7),
    ("Book 5: Buffon (Carriage)", 2094.88, 1346.36),
    ("Book 6: Rondelet (Mill)", 3168.6, 2405.75),
    ("Book 7: Codex (Infirmary)", 2592.18, 2992.87)
]

for name, x, y in test_points:
    mx, my = gen.to_map_coord(x, y)
    print(f"  {name}: world=({x:.1f}, {y:.1f}) -> screen=({mx}, {my})")
