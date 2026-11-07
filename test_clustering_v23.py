import math
import perfect_briefings_core_v22 as core
import generate_perfect_briefings_v22 as gen

def test_raid_clustering(raid_id):
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
    print(f"Raid {raid_id}: {len(screen_pts)} points")
    
    # Proximity clustering
    CLUSTER_DIST = 38 # distance threshold
    clusters = []
    assigned = [False] * len(screen_pts)
    
    for i in range(len(screen_pts)):
        if assigned[i]: continue
        cluster = [screen_pts[i]]
        assigned[i] = True
        
        for j in range(i + 1, len(screen_pts)):
            if assigned[j]: continue
            # check distance to any member
            for m in cluster:
                d = math.hypot(m['sx'] - screen_pts[j]['sx'], m['sy'] - screen_pts[j]['sy'])
                if d < CLUSTER_DIST:
                    cluster.append(screen_pts[j])
                    assigned[j] = True
                    break
        clusters.append(cluster)
        
    print(f"  Clusters: {len(clusters)}")
    multi_count = sum(1 for c in clusters if len(c) > 1)
    print(f"  Clusters with multiple points: {multi_count}")
    for idx, c in enumerate(clusters):
        if len(c) > 1:
            types = {}
            for p in c:
                types[p['type']] = types.get(p['type'], 0) + 1
            print(f"    Cluster {idx}: {len(c)} points -> {types}")

test_raid_clustering(1)
test_raid_clustering(2)
