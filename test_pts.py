import os, sqlite3
import perfect_briefings_core_v22 as core
import generate_perfect_briefings_v22 as gen

for r in gen.RAIDS_CONFIG:
    pts = core.get_filtered_loot_from_db(r['map_name'], r['container_priority_map'])
    print(f"Raid {r['id']}: {r['map_name']} -> {len(pts)} points")
    # check types
    type_counts = {}
    for p in pts:
        type_counts[p['type']] = type_counts.get(p['type'], 0) + 1
    print("  Types:", type_counts)
