import math
import perfect_briefings_core_v23 as core
import generate_perfect_briefings_v23 as gen

def test_v24_markers(raid_id):
    cfg = gen.RAIDS_CONFIG[raid_id - 1]
    points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    
    screen_pts = []
    for pt in points:
        sx, sy = gen.to_map_coord(pt['x'], pt['y'])
        screen_pts.append({
            'sx': sx, 'sy': sy,
            'color': pt['color'],
            'type': pt['type'],
            'cont_img': pt.get('cont_img')
        })
        
    clusters = []
    assigned = [False] * len(screen_pts)
    for i in range(len(screen_pts)):
        if assigned[i]: continue
        c = [screen_pts[i]]
        assigned[i] = True
        for j in range(i+1, len(screen_pts)):
            if assigned[j]: continue
            for m in c:
                if math.hypot(m['sx'] - screen_pts[j]['sx'], m['sy'] - screen_pts[j]['sy']) < 28:
                    c.append(screen_pts[j])
                    assigned[j] = True
                    break
        clusters.append(c)
        
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
                r_orbit = 46.0
                angle = -math.pi/2 + (t_idx - (num_types - 1)/2.0) * (2 * math.pi / max(3, num_types))
                bx = cx + r_orbit * math.cos(angle)
                by = cy + r_orbit * math.sin(angle)
                all_badges.append({
                    'bx': bx, 'by': by,
                    'color': pts[0]['color'], 'cont_img': pts[0]['cont_img'],
                    'spawns': [(p['sx'], p['sy']) for p in pts],
                    'is_multi': True
                })
                
    MIN_DIST = 52.0
    for it in range(50):
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
            break
            
    min_sep = 999999
    for i in range(len(all_badges)):
        for j in range(i+1, len(all_badges)):
            d = math.hypot(all_badges[i]['bx'] - all_badges[j]['bx'], all_badges[i]['by'] - all_badges[j]['by'])
            if d < min_sep:
                min_sep = d
    print(f"Raid {raid_id}: {len(screen_pts)} pts -> {len(all_badges)} badges, min distance: {min_sep:.2f}px (Target >= {MIN_DIST}px)")

for r in range(1, 8):
    test_v24_markers(r)
