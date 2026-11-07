import json

db = json.load(open('data/full_companion_skins.json', encoding='utf-8'))
queries = [
    "ou est ce que je peux trouver le skin peasant burden",
    "ou je peux trouver le skin de la spear peasant",
    "peasant burden",
    "skin bacchus wand",
    "skin loup",
    "skin basilisk",
    "skin solstice"
]

for q in queries:
    q_norm = q.lower().replace("'", "").replace("’", "").replace("-", " ")
    matched = None
    for k, v in db.items():
        k_norm = k.replace("'", "").replace("’", "").replace("-", " ")
        name_norm = v.get('name', '').lower().replace("'", "").replace("’", "").replace("-", " ")
        if k_norm in q_norm or name_norm in q_norm or (len(k_norm.split()) > 1 and all(w.rstrip('s') in q_norm for w in k_norm.split())):
            matched = v
            break
        # Also check single distinctive word match
        words = [w.rstrip('s') for w in k_norm.split() if len(w) >= 4 and w not in ["skin", "pour", "avec", "dans", "target", "item", "spear", "longboy", "axe", "club"]]
        if any(w in q_norm for w in words):
            matched = v
            break

    print(f"Query: '{q}' -> Matched: {matched.get('name') if matched else 'None'} ({matched.get('target') if matched else ''})")
