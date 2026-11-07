import math
import perfect_briefings_core_v22 as core
import generate_perfect_briefings_v22 as gen

def test_tight_clustering(raid_id, dist_thresh=20):
    cfg = [r for r in gen.RAIDS_CONFIG if r['id'] == raid_id][0]
    points = core.get_filtered_loot_from_db(cfg["map_name"], cfg["container_priority_map"])
    
    screen_pts = []
    for pt in points:
        sx, sy = gen.to_map_coord(pt['x'], pt['y'])
        screen_pts.append({
            'sx': sx, 'sy': sy,
            'color': pt['color'],
            'type': pt['type'],
            'label': pt['label']
        })
        
    # Leader/Centroid based clustering:
    # A point only joins a cluster if its distance to the cluster CENTROID is < dist_thresh
    clusters = []
    for p in screen_pts:
        best_c = None
        best_d = 999999
        for c in clusters:
            cx = sum(x['sx'] for x in c) / len(c)
            cy = sum(x['sy'] for x in c) / len(c)
            d = math.hypot(cx - p['sx'], cy - p['sy'])
            if d < dist_thresh and d < best_d:
                best_d = d
                best_c = c
        if best_c is not None:
            best_c.append(p)
        else:
            clusters.append([p])
            
    print(f"Raid {raid_id} (thresh={dist_thresh}): {len(screen_pts)} pts -> {len(clusters)} clusters")
    for idx, c in enumerate(clusters):
        if len(c) > 1:
            types = {}
            for p in c:
                types[p['type']] = types.get(p['type'], 0) + 1
            print(f"    Cluster {idx}: {len(c)} points -> {types}")

test_tight_clustering(1, 20)
test_tight_clustering(1, 24)
