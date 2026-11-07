with open('co_pilot/vision_analyzer.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'from universal_v7_engine import render_universal_stash_analysis',
    'from universal_v8_engine import render_universal_stash_analysis'
)

# Replace the prompt instructions
old_rules = '''CONSIGNES STRICTES :
1. NE PAS LISTER LES OBJETS À GARDER : Tous les soins, vivres, armures, sacs, armes, outils et SURTOUT TOUTES LES LETTRES ET DOCUMENTS SCELLÉS SONT STRICTEMENT CONSERVÉS (source majeure d'EXP de progression de personnage ! Ne jamais proposer de vendre des lettres ou documents scellés).
2. 🛒 **ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU :**
   - Liste uniquement les babioles, bibelots sans recette, doublons inutiles et objets superflus détectés à liquider.
   - Indique la quantité et l'estimation unitaire en Cuivres.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Donne le total des articles à vendre en Pièces d'Argent (1 ag = 100 c) et Pièces de Cuivre.
4. ⚖️ **ROTATION DU MARCHÉ :** Indique simplement si le cours actuel est favorable (+-15% par rapport au cours de base).
5. Sois très concis, clair et direct. Pas de phrases superflues.
Termine obligatoirement par 1 à 2 phrases orales après la balise [SPOKEN].'''

new_rules = '''CONSIGNES STRICTES :
1. NE PAS LISTER LES OBJETS À GARDER : Tous les soins, vivres, armures, sacs, armes, outils et SURTOUT TOUTES LES LETTRES ET DOCUMENTS SCELLÉS SONT STRICTEMENT CONSERVÉS (source majeure d'EXP de progression de personnage ! Ne jamais proposer de vendre des lettres ou documents scellés).
2. 🛒 **ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU :**
   - Liste uniquement les babioles, bibelots sans recette, doublons inutiles et objets superflus détectés à liquider.
   - Indique la quantité et l'estimation unitaire en Cuivres.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Donne le total des articles à vendre en Pièces d'Argent (1 ag = 100 c) et Pièces de Cuivre.
4. Sois très concis, clair et direct. Pas de phrases superflues. Ne mentionne pas de rotation fictive de marché.
Termine obligatoirement par 1 à 2 phrases orales après la balise [SPOKEN].'''

if old_rules in text:
    text = text.replace(old_rules, new_rules)
    print("Replaced rules successfully!")
else:
    print("old_rules not matched")

with open('co_pilot/vision_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated co_pilot/vision_analyzer.py!")
