import generate_perfect_briefings_v22 as gen
for r in gen.RAIDS_CONFIG:
    print(f"Raid {r['id']}:")
    for k, v in r.get('container_priority_map', {}).items():
        print(f"  {k}: {v.get('label')}, item_img: {v.get('item_img')}, keyword: {v.get('keyword')}")
