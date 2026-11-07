import math

def test_collision_resolution():
    badges = [
        {'bx': 500, 'by': 500, 'spawns': [(500, 500), (505, 502)]},
        {'bx': 510, 'by': 508, 'spawns': [(510, 508)]},
        {'bx': 502, 'by': 515, 'spawns': [(502, 515)]}
    ]
    MIN_DIST = 36.0
    for it in range(25):
        moved = False
        for i in range(len(badges)):
            for j in range(i+1, len(badges)):
                dx = badges[i]['bx'] - badges[j]['bx']
                dy = badges[i]['by'] - badges[j]['by']
                d = math.hypot(dx, dy)
                if d < 0.001:
                    dx, dy = 1.0, 0.0
                    d = 1.0
                if d < MIN_DIST:
                    moved = True
                    overlap = (MIN_DIST - d) * 0.5
                    badges[i]['bx'] += (dx / d) * overlap
                    badges[i]['by'] += (dy / d) * overlap
                    badges[j]['bx'] -= (dx / d) * overlap
                    badges[j]['by'] -= (dy / d) * overlap
        if not moved:
            break
            
    print("Final distances:")
    for i in range(len(badges)):
        for j in range(i+1, len(badges)):
            d = math.hypot(badges[i]['bx'] - badges[j]['bx'], badges[i]['by'] - badges[j]['by'])
            print(f"  {i} - {j}: {d:.2f}px (>= {MIN_DIST})")

test_collision_resolution()
