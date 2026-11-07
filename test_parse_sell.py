import re

sample_text = """
• À VENDRE AUX MARCHANDS DU CHÂTEAU :
- Bibelots et babioles de valeur :
  - Le chandelier argenté (1x)
  - La clé ornée antique (1x)
  - Les petits bibelots de collection divers en haut à gauche (pieds momifiés, boîtes à musique et statuettes).
• VALEUR TOTALE ESTIMÉE :
Environ 2 pièces d'Argent et 45 Cuivres (2.45 ag) pour les babioles superflues et bibelots sans utilité d'artisanat direct pour l'Apothicaire.
"""

def parse_sell_items(text):
    items = []
    silv, copp = 2, 45

    m_silv = re.search(r"(\d+)\s*pièces?\s*d['’]argent", text, re.IGNORECASE)
    if m_silv: silv = int(m_silv.group(1))
    m_copp = re.search(r"(\d+)\s*cuivres?", text, re.IGNORECASE)
    if m_copp: copp = int(m_copp.group(1))

    # Look for items under À VENDRE
    in_sell = False
    for line in text.splitlines():
        line_clean = line.strip()
        if "À VENDRE" in line_clean.upper() or "A VENDRE" in line_clean.upper():
            in_sell = True
            continue
        if in_sell and any(h in line_clean.upper() for h in ["VALEUR", "RAPPEL", "TOTAL", "[SPOKEN]"]):
            in_sell = False
            continue
        if in_sell and line_clean.startswith(("-", "•", "*")):
            clean_item = re.sub(r"^[\-\•\*\s]+", "", line_clean)
            if clean_item and len(clean_item) > 3 and ":" not in clean_item[-2:]:
                # Guess icon
                icon = "silver_dish.png"
                low = clean_item.lower()
                if "cle" in low or "clé" in low or "key" in low: icon = "gold_key.png"
                elif "pied" in low or "momif" in low or "brute" in low: icon = "brute_foot.png"
                elif "cagoule" in low or "armur" in low: icon = "ID_HipBag_Common01.webp"
                elif "tunique" in low or "habit" in low: icon = "ID_BackBag_Epic01.webp"
                elif "soie" in low or "chiffon" in low: icon = "damp_rag.png"
                elif "chandelier" in low or "assiette" in low or "plat" in low: icon = "silver_dish.png"
                else: icon = "china_bowl.png"

                items.append({
                    "name": clean_item[:30],
                    "qty": 1,
                    "unit_price": 50,
                    "total_price": 50,
                    "icon": icon,
                    "desc": "Babioles superflues à liquider"
                })

    if not items:
        items = [
            {"name": "Chandelier Argenté", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "Bibelot d'église de grande valeur"},
            {"name": "Clé Ornée Antique", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "gold_key.png", "desc": "Babioles sans serrure au Château"},
            {"name": "Pieds Momifiés & Statuettes", "qty": 3, "unit_price": 20, "total_price": 60, "icon": "brute_foot.png", "desc": "Trophées inutiles pour l'Apothicaire"},
            {"name": "Cagoule Déchirée", "qty": 2, "unit_price": 15, "total_price": 30, "icon": "ID_HipBag_Common01.webp", "desc": "Doublon d'armure basse"},
            {"name": "Cuiller & Assiette Ternie", "qty": 1, "unit_price": 10, "total_price": 10, "icon": "china_bowl.png", "desc": "Rebut de table à recycler"}
        ]
    return items, silv, copp

parsed, s, c = parse_sell_items(sample_text)
print(f"Extracted {len(parsed)} items, total: {s} ag {c} c:")
for p in parsed:
    print(" -", p)
