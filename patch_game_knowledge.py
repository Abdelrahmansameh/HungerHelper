p = "co_pilot/game_knowledge.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = """    if not is_needs_query and not any(w in lowered for w in ["family ring"]):
        return None

    # Detect item
    item_detected = "farine"
    item_en = "flour"
    giver = "Denis le Meunier"
    quest_name = "Le Pain du Château"
    quantity = "5 sacs de farine"
    importance = "CRITIQUE (Débloque les rations de survie au Château)"
    location_hint = "Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier)."

    if any(w in lowered for w in ["family", "gavroche", "ring", "anneau"]):
        item_detected, item_en = "anneau de famille (family ring)", "family ring"
        giver = "Gavroche le Gamin"
        quest_name = "Le Legs des Gavroche"
        quantity = "1 Anneau de Famille"
        importance = "QUÊTE HISTOIRE UNIQUE (Indispensable pour débloquer les talents niveau 3)"
        location_hint = "Se trouve dans les tiroirs et commodes du Manoir Ruiné sur le Pont Jacques, ou dans les armoires de Sarlat Farm." """

replacement = """    if not is_needs_query:
        return None

    # Detect item
    item_detected = "farine"
    item_en = "flour"
    giver = "Denis le Meunier"
    quest_name = "Making Dough"
    quantity = "Sacs de farine"
    importance = "CRITIQUE (Débloque le pain et les rations au Château)"
    location_hint = "Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier)."

    if any(w in lowered for w in ["family ring", "bague", "anneau de famille"]):
        item_detected, item_en = "anneau de famille (family ring)", "family-ring"
        giver = "Louis"
        quest_name = "The Last Prisoner"
        quantity = "1 Anneau de Famille"
        importance = "QUÊTE HISTOIRE UNIQUE (Indispensable pour valider The Last Prisoner)"
        location_hint = "Défini pour les armoires et conteneurs résidentiels de Jacques Bridge et Sarlat Farm." """

# Normalize whitespace in replacement to match target
target_stripped = target.strip()
for l in text.split("\n"):
    if 'if not is_needs_query and not any' in l:
        print("Found line:", l)

# Replace target
text = text.replace(target.strip(), replacement.strip(), 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated game_knowledge.py successfully!")
