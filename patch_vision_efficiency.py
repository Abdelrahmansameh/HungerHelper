p = "co_pilot/vision_analyzer.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = """    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        img = Image.open(image_path)

        prompt = f\"\"\"
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER' (par Good Fun Corporation).
Un joueur ({username}) t'envoie une capture d'écran de son jeu (inventaire de raid, sac à dos, besace, ou stash au Château).
Question du joueur : \"{user_query or 'Analyse mon inventaire, combien ça vaut et que dois-je garder ou vendre ?'}\"

DIRECTIVES D'ANALYSE :
1. Examine attentivement la grille d'inventaire et les icônes d'objets visibles.
2. Identifie chaque objet avec son nom exact dans HUNGER, sa quantité (stack) et sa rareté (Commun, Peu Commun, Rare, Épique, Légendaire).
3. Calcule la valeur marchande totale en Argent (100 cuivre = 1 argent) et en Cuivre.
4. Fais le triage tactique strict :
   - 🔒 **À GARDER (Besace Sécurisée) :** Objets indispensables pour les quêtes actives/futures (farine pour Denis le Meunier, anneau de famille pour Louis, salpêtre pour la poudre, bezoard, clés de donjon comme Jacques Folly Key).
   - 💰 **À VENDRE (Liquidités) :** Butin superflu, babioles de valeur, doublons d'armes.
5. 🛒 **ANALYSE DES MARCHANDS DU CHÂTEAU :**
   - Indique auprès de quel marchand vendre chaque objet (Denis le Meunier, Paul le Forgeron, Voyant le Fusilier, Octave de Villiers, Piro le Médecin).
   - Explique la règle de prix marchand : les marchands rachètent au prix de base, mais revendent beaucoup plus cher si on veut leur racheter en boutique !
   
RÉPONDS EN FRANÇAIS dans un style sharp, tactique, concis et ultra-lisible avec des puces.
Fournis un résumé parlé (court, 2 phrases max) à la fin sous la balise [SPOKEN].
\"\"\"
        response = client.models.generate_content(
            model=\"gemini-2.5-flash\",
            contents=[img, prompt]
        )"""

replacement = """    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)

        # Token-Efficient Image Pre-processing:
        # Scale image to max 1024x1024 (standard Gemini vision token grid = only 258 tokens!)
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        max_dim = 1024
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        prompt = f\"\"\"
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER' (par Good Fun Corporation).
Un joueur ({username}) t'envoie une capture d'écran de son jeu (inventaire de raid, sacoche, ou coffre de stash au Château).
Demande du joueur : \"{user_query or 'Analyse mon inventaire, combien ça vaut et que dois-je garder ou vendre ?'}\"

INSTRUCTIONS STRICTES ET CONCISES (Économie de tokens) :
1. Examine la grille d'inventaire et les icônes visibles.
2. Identifie les objets clés avec quantités.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Calcule la somme en Argent (100c = 1ag) et Cuivre.
4. 🔒 **À GARDER (Besace Sécurisée) :** Objets indispensables pour quêtes (farine, anneau de famille, salpêtre, clés de donjon, bezoard).
5. 🛒 **À VENDRE AUX MARCHANDS :** Objets à convertir en pièces.
6. ⚖️ **PRIX MARCHANDS CHÂTEAU :** Rappelle que les marchands rachètent au prix de base mais revendent beaucoup plus cher (x2 à x3) en boutique.

Rédige en français concis et clair sous forme de puces.
Termine obligatoirement par un résumé oral court (2 phrases) après la balise [SPOKEN].
\"\"\"
        # Call gemini-flash-lite-latest with strict max_output_tokens=750 to maximize efficiency
        response = client.models.generate_content(
            model=\"gemini-flash-lite-latest\",
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=750,
                temperature=0.1
            )
        )"""

assert target in text, "target not found"
text = text.replace(target, replacement, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("co_pilot/vision_analyzer.py updated for maximum token efficiency!")
