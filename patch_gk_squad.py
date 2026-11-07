with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

text_n = text.replace("\r\n", "\n")

old_fn = """def answer_squad_item_needs_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Answers which active or future quests require a specific loot item, and whether to safe-pouch it.\"\"\"
    lowered = query.lower()
    is_needs_query = any(w in lowered for w in [
        \"qui a besoin\", \"qui cherche\", \"qui demande\", \"who needs\", \"who wants\", \"besoin de\",
        \"est-ce que j'ai besoin\", \"est ce que jai besoin\", \"dois-je garder\", \"dois je garder\",
        \"je dois garder\", \"utile pour\", \"je garde ou je jette\", \"garder ou jeter\",
        \"faut il garder\", \"faut-il garder\", \"do i need\", \"should i keep\"
    ])
    if not is_needs_query:
        return None

    # Detect item
    item_detected = \"farine\"
    item_en = \"flour\"
    giver = \"Denis le Meunier\"
    quest_name = \"Making Dough\"
    quantity = \"Sacs de farine\"
    importance = \"CRITIQUE (Débloque le pain et les rations au Château)\"
    location_hint = \"Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier).\""""

new_fn = """def answer_squad_item_needs_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Answers which active or future quests require a specific loot item, and whether to safe-pouch it.\"\"\"
    lowered = query.lower()
    is_needs_query = any(w in lowered for w in [
        \"qui a besoin\", \"qui cherche\", \"qui demande\", \"who needs\", \"who wants\", \"besoin de\",
        \"est-ce que j'ai besoin\", \"est ce que jai besoin\", \"est-ce que\", \"est ce que\",
        \"a besoin de\", \"a besoin d\", \"dois-je garder\", \"dois je garder\",
        \"je dois garder\", \"utile pour\", \"je garde ou je jette\", \"garder ou jeter\",
        \"faut il garder\", \"faut-il garder\", \"do i need\", \"should i keep\"
    ])
    if not is_needs_query:
        return None

    # 1. Try Player-specific / Squad DB Quest Sync check
    from co_pilot.quest_sync import check_player_item_need
    import re
    # Check if a user name is mentioned
    player_match = re.search(r\"(?:est-ce que|est ce que|qui)\s+([a-zA-Z0-9_-]+)\s+a besoin\", lowered)
    target_player = player_match.group(1) if player_match else "Abdallah"

    # Extract target item word
    it_cand = None
    for item_k in [\"farine\", \"flour\", \"bezoar\", \"bague\", \"ring\", \"salpetre\", \"salpêtre\", \"saltpetre\", \"charbon\", \"charcoal\", \"pouch\", \"moist\"]:
        if item_k in lowered:
            it_cand = item_k
            break
    
    if it_cand:
        sync_res = check_player_item_need(target_player, it_cand)
        if sync_res.get(\"needed\"):
            spoken = f\"Oui ! {sync_res['message']}\" if is_french else f\"Yes! {sync_res['message']}\"
            display = (
                f\"📜 **SYNCHRONISATION DES QUÊTES DE L'ESCOUADE :**\\n\\n\"
                f\"{sync_res['message']}\\n\\n\"
                f\"🔒 **Consigne :** Gardez cet item dans votre besace sécurisée ou stockez-le dans votre coffre de Stash !\"
            )
            return {\"spoken_text\": spoken, \"display_text\": display}

    # Detect item
    item_detected = \"farine\"
    item_en = \"flour\"
    giver = \"Éloïse (Château Hub)\"
    quest_name = \"Making Dough\"
    quantity = \"20x Sacs de Farine\"
    importance = \"CRITIQUE (Débloque le pain et les rations au Château)\"
    location_hint = \"Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier, taux 47.6%).\""""

if old_fn in text_n:
    text_n = text_n.replace(old_fn, new_fn)
    with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
        f.write(text_n)
    print("GK_SQUAD_SYNC_PATCHED")
else:
    print("old_fn not found")
