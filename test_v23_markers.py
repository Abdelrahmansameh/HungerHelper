import os, sys, math, sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v22 as core
import generate_perfect_briefings_v22 as gen

print("Testing V23 map marker logic...")
cfg = gen.RAIDS_CONFIG[0] # Raid 1
points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
print(f"Total points: {len(points)}")

screen_pts = []
for pt in points:
    sx, sy = gen.to_map_coord(pt['x'], pt['y'])
    # get cont_img
    cont_img = None
    for k, v in cfg['container_priority_map'].items():
        if v['keyword'] in pt['label'] or k == pt['type']:
            cont_img = v.get('cont_img')
            break
    screen_pts.append({
        'sx': sx, 'sy': sy,
        'color': pt['color'],
        'type': pt['type'],
        'cont_img': cont_img,
        'label': pt['label']
    })

# Proximity clustering
clusters = []
assigned = [False] * len(screen_pts)
for i in range(len(screen_pts)):
    if assigned[i]: continue
    c = [screen_pts[i]]
    assigned[i] = True
    for j in range(i+1, len(screen_pts)):
        if assigned[j]: continue
        for m in c:
            if math.hypot(m['sx'] - screen_pts[j]['sx'], m['sy'] - screen_pts[j]['sy']) < 24:
                c.append(screen_pts[j])
                assigned[j] = True
                break
    clusters.append(c)

print(f"Formed {len(clusters)} clusters from {len(screen_pts)} points.")

all_badges = []
for c in clusters:
    if len(c) == 1:
        p = c[0]
        all_badges.append({
            'bx': float(p['sx']), 'by': float(p['sy']),
            'color': p['color'], 'cont_img': p['cont_img'],
            'spawns': [(p['sx'], p['sy'])],
            'is_multi': False
        })
    else:
        cx = sum(p['sx'] for p in c) / len(c)
        cy = sum(p['sy'] for p in c) / len(c)
        by_type = {}
        for p in c:
            by_type.setdefault(p['type'], []).append(p)
        
        num_types = len(by_type)
        for t_idx, (t_key, pts) in enumerate(by_type.items()):
            color = pts[0]['color']
            cont_img = pts[0]['cont_img']
            spawns = [(p['sx'], p['sy']) for p in pts]
            r_orbit = 38.0
            angle = -math.pi/2 + (t_idx - (num_types - 1)/2.0) * (2 * math.pi / max(3, num_types))
            bx = cx + r_orbit * math.cos(angle)
            by = cy + r_orbit * math.sin(angle)
            all_badges.append({
                'bx': bx, 'by': by,
                'color': color, 'cont_img': cont_img,
                'spawns': spawns,
                'is_multi': True
            })

print(f"Total badges generated: {len(all_badges)}")

# Collision relaxation
MIN_DIST = 36.0
for it in range(40):
    overlap_found = False
    for i in range(len(all_badges)):
        for j in range(i+1, len(all_badges)):
            dx = all_badges[i]['bx'] - all_badges[j]['bx']
            dy = all_badges[i]['by'] - all_badges[j]['by']
            d = math.hypot(dx, dy)
            if d < 0.001:
                dx, dy = 1.0, 0.0
                d = 1.0
            if d < MIN_DIST:
                overlap_found = True
                overlap = (MIN_DIST - d) * 0.5
                all_badges[i]['bx'] += (dx/d) * overlap
                all_badges[i]['by'] += (dy/d) * overlap
                all_badges[j]['bx'] -= (dx/d) * overlap
                all_badges[j]['by'] -= (dy/d) * overlap
    if not overlap_found:
        print(f"Relaxed completely after {it+1} iterations!")
        break

# Verify no overlaps
min_sep = 999999
for i in range(len(all_badges)):
    for j in range(i+1, len(all_badges)):
        d = math.hypot(all_badges[i]['bx'] - all_badges[j]['bx'], all_badges[i]['by'] - all_badges[j]['by'])
        if d < min_sep:
            min_sep = d
print(f"Minimum distance between any two badges: {min_sep:.2f}px (Target >= {MIN_DIST}px)")
