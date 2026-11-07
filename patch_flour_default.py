with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix is_needs_query in answer_squad_item_needs_query
old_needs = """    is_needs_query = any(w in lowered for w in [
        "qui a besoin", "qui cherche", "qui demande", "who needs", "who wants", "besoin de",
        "est-ce que j'ai besoin", "est ce que jai besoin", "est-ce que", "est ce que",
        "a besoin de", "a besoin d", "dois-je garder", "dois je garder",
        "je dois garder", "utile pour", "je garde ou je jette", "garder ou jeter",
        "faut il garder", "faut-il garder", "do i need", "should i keep"
    ])"""

new_needs = """    is_needs_query = any(w in lowered for w in [
        "qui a besoin", "qui cherche", "qui demande", "who needs", "who wants", "besoin de", "besoin d",
        "est-ce que j'ai besoin", "est ce que jai besoin", "est ce que j'ai besoin",
        "a besoin de", "a besoin d", "dois-je garder", "dois je garder",
        "je dois garder", "utile pour", "je garde ou je jette", "garder ou jeter",
        "faut il garder", "faut-il garder", "do i need", "should i keep"
    ])
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "peasant", "bacchus", "loup", "basilisk", "solstice"]):
        return None"""

if old_needs in text:
    text = text.replace(old_needs, new_needs)
    print("Fixed is_needs_query in game_knowledge.py!")

# Also prevent default to flour if flour is not asked
old_flour_default = """    # Detect item
    item_detected = "farine"
    item_en = "flour"
    giver = "Éloïse (Château Hub)"
    quest_name = "Making Dough"
    quantity = "20x Sacs de Farine"
    importance = "CRITIQUE (Débloque le pain et les rations au Château)"
    location_hint = "Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier, taux 47.6%)." """

new_flour_default = """    # Ensure an item is actually targeted
    has_item_target = any(w in lowered for w in ["farine", "flour", "bague", "ring", "salpetre", "saltpetre", "charbon", "charcoal", "bezoar", "chiffon", "damp rag", "balm", "baume"])
    if not has_item_target:
        return None

    item_detected = "farine"
    item_en = "flour"
    giver = "Éloïse (Château Hub)"
    quest_name = "Making Dough"
    quantity = "20x Sacs de Farine"
    importance = "CRITIQUE (Débloque le pain et les rations au Château)"
    location_hint = "Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier, taux 47.6%)." """

if old_flour_default in text:
    text = text.replace(old_flour_default, new_flour_default)
    print("Prevented accidental default to flour in game_knowledge.py!")

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)
print("co_pilot/game_knowledge.py patched successfully!")
