from co_pilot.brain import extract_key_search_terms
from co_pilot.knowledge_db import search_quests, search_items

q = "montre moi tout les armes a 2 main melee"
cands = extract_key_search_terms(q)
print("Candidates for:", q)
print(cands)

for c in cands:
    qs = search_quests(c, limit=3)
    if qs:
        print(f"Candidate '{c}' found quests:", [q["name"] for q in qs])
