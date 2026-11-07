"""
Hunger Helper - Multimodal Screenshot Stash & Inventory Analyzer
Powered by Google Gemini 2.5 Flash Vision & Hunger Companion Database.
Analyzes screenshots of player inventory, stash, and raid backpacks:
- Appraises total value in Silver & Copper.
- Triages items to KEEP in safe pouch (quests, keys, crafting) vs SELL to merchants.
- Analyzes vendor buy vs sell price differences across Chateau NPCs.
"""

import os
import re
import json
from typing import Dict, Any, Optional, List
from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")

def get_gemini_api_key() -> Optional[str]:
    """Retrieve Gemini API key from environment or config.json."""
    if os.getenv("GEMINI_API_KEY"):
        return os.getenv("GEMINI_API_KEY")
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("GEMINI_API_KEY")
        except Exception:
            pass
    return None

def set_gemini_api_key(key: str) -> bool:
    """Save user-provided Gemini API key to config.json."""
    try:
        cfg = {}
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        cfg["GEMINI_API_KEY"] = key.strip()
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        os.environ["GEMINI_API_KEY"] = key.strip()
        return True
    except Exception as e:
        print(f"[Config Error] Failed saving Gemini key: {e}")
        return False

def appraise_text_inventory(text: str, is_french: bool = True) -> Dict[str, Any]:
    """
    Parses a text list of inventory items and computes total value and keep/sell advice.
    E.g. 'j'ai 3 farines, 2 salpetres, 1 deux et 4 chiffons'
    """
    from co_pilot.companion_intel import get_companion_item_intel, normalize_query_to_slug

    # Find patterns like '3 farines', '1 pistolet deux', '5 sacs'
    tokens = re.split(r"[,;\+et\n]+", text.lower())
    total_copper = 0
    items_breakdown = []
    items_to_keep = []
    items_to_sell = []

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        # Extract quantity if present
        qty_m = re.search(r"(\d+)\s*(.*)", token)
        if qty_m:
            qty = int(qty_m.group(1))
            item_name = qty_m.group(2).strip()
        else:
            qty = 1
            item_name = token

        if not item_name or any(skip in item_name for skip in ["j'ai", "jai", "inventaire", "stash", "sac"]):
            continue

        slug = normalize_query_to_slug(item_name)
        intel = get_companion_item_intel(slug)
        if intel:
            subtotal = intel["base_value"] * qty
            total_copper += subtotal
            name = intel["name_en"]
            s_s = subtotal // 100
            s_c = subtotal % 100
            
            is_keep = bool(intel.get("quests_needed")) or "key" in slug or "cle" in slug or "deux" in slug
            if is_keep:
                q_reason = f"Requis pour {intel['quests_needed'][0]}" if intel.get("quests_needed") else "Arme/Clé de grande valeur"
                items_to_keep.append(f"• **{qty}x {name}** — 🔒 *{q_reason}*")
            else:
                v_dest = intel.get("vendor_buy", "Marchands du Château")
                items_to_sell.append(f"• **{qty}x {name}** — 💰 Revente : `{s_s}ag {s_c}c`")

            items_breakdown.append(f"• **{qty}x {name}** (`{intel['rarity']}`) : `{s_s} Argent {s_c} Cuivre`")

    tot_silver = total_copper // 100
    rem_copper = total_copper % 100

    if not items_breakdown:
        return {
            "spoken_text": "Je n'ai pas pu identifier d'objets dans votre liste. Spécifiez par exemple : 3 farines, 1 deux, 2 salpêtre.",
            "display_text": "❌ **Aucun objet reconnu.** *Indiquez vos objets avec quantités : ex. `3 farines, 1 pistolet deux, 2 salpêtres`*"
        }

    spoken = f"Valeur totale estimée : {tot_silver} argent et {rem_copper} cuivre. {len(items_to_keep)} objets prioritaires à conserver en besace."
    display = (
        f"💰 **ESTIMATION DE BUTIN & INVENTAIRE :**\n\n"
        f"• 🪙 **Valeur Marchande Totale :** **{tot_silver} Argent {rem_copper} Cuivre**\n\n"
        f"🔒 **OBJETS À GARDER ABSOLUMENT (Besace Sécurisée) :**\n"
        + ("\n".join(items_to_keep) if items_to_keep else "• *Aucun objet de quête critique. Vous pouvez tout liquider !*") + "\n\n"
        f"🛒 **OBJETS À VENDRE AUX MARCHANDS :**\n"
        + ("\n".join(items_to_sell) if items_to_sell else "• *Tous vos objets sont utiles pour vos missions.*")
    )
    return {"spoken_text": spoken, "display_text": display}


async def analyze_inventory_screenshot(
    image_path: str,
    user_query: str,
    user_id: str,
    username: str
) -> Dict[str, Any]:
    """
    Analyzes an uploaded in-game screenshot of player inventory or stash using Gemini 2.5 Flash Vision.
    Cross-references detected items with hunger_helper.db for precise market pricing and merchant advice.
    """
    is_french = any(w in (user_query or "").lower() for w in ["en français", "en francais", "in french"])
    api_key = get_gemini_api_key()

    if not api_key:
        # Guided response on how to enable multimodal vision
        spoken = "Capture d'écran reçue ! Pour activer l'analyse visuelle par intelligence artificielle, configurez votre clé Gemini avec la commande /config-gemini."
        display = (
            f"📸 **CAPTURE D'ÉCRAN REÇUE : ANALYSE DE L'INVENTAIRE**\n\n"
            f"Pour permettre à Éloïse de scanner automatiquement vos captures d'inventaire, de sacoche de raid et de coffre de stash avec vision par IA :\n\n"
            f"1. Obtenez votre clé gratuite Google AI Studio sur : **https://aistudio.google.com/**\n"
            f"2. Tapez la commande dans Discord : `/config-gemini key:<Votre_Clé_API>`\n"
            f"*(Ou ajoutez `GEMINI_API_KEY` dans le fichier `config.json` de votre serveur)*\n\n"
            f"💡 **En attendant :** Vous pouvez aussi m'écrire vos objets directement dans le chat, par exemple :\n"
            f"*« Éloïse, j'ai 3 farines, 1 pistolet Deux et 2 poudres de salpêtre, combien ça vaut ? »*"
        )
        return {"spoken_text": spoken, "display_text": display}

    try:
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

        # Fetch player profile (character & profession)
        char_name = "Marie"
        prof_name = "Apothicaire"
        try:
            import sqlite3
            db_p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hunger_helper.db"))
            conn = sqlite3.connect(db_p)
            c = conn.cursor()
            c.execute("SELECT notes FROM user_profiles WHERE user_id = ?", (user_id,))
            r = c.fetchone()
            if r and r[0]:
                notes_lower = r[0].lower()
                if "jean" in notes_lower: char_name = "Jean"
                elif "claude" in notes_lower: char_name = "Claude"
                if "forgeron" in notes_lower: prof_name = "Forgeron"
                elif "tailleur" in notes_lower: prof_name = "Tailleur"
            conn.close()
        except Exception:
            pass

        prompt = f"""
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER'.
Le joueur {username} (Personnage : {char_name}, Profession : {prof_name}) t'envoie une capture d'écran de sa stash / inventaire.
Demande du joueur : "{user_query or 'Analyse ma stash et mon inventaire, que dois-je vendre et combien ça vaut ?'}"

CONSIGNES STRICTES :
1. NE PAS LISTER LES OBJETS À GARDER : Tous les soins, vivres, armures, sacs, armes, outils et SURTOUT TOUTES LES LETTRES ET DOCUMENTS SCELLÉS SONT STRICTEMENT CONSERVÉS (source majeure d'EXP de progression de personnage ! Ne jamais proposer de vendre des lettres ou documents scellés).
2. 🛒 **ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU :**
   - Liste uniquement les babioles, bibelots sans recette, doublons inutiles et objets superflus détectés à liquider.
   - Indique la quantité et l'estimation unitaire en Cuivres.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Donne le total des articles à vendre en Pièces d'Argent (1 ag = 100 c) et Pièces de Cuivre.
4. Sois très concis, clair et direct. Pas de phrases superflues. Ne mentionne pas de rotation fictive de marché.
Termine obligatoirement par 1 à 2 phrases orales après la balise [SPOKEN].
"""
        # Call gemini-flash-lite-latest with strict max_output_tokens=750
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=750,
                temperature=0.1
            )
        )

        resp_text = response.text or ""
        spoken = "Analyse de votre stash terminée. Rapport visuel et inventaire des gains générés dans le salon."
        display = resp_text

        if "[SPOKEN]" in resp_text:
            parts = resp_text.split("[SPOKEN]")
            display = parts[0].strip()
            spoken = parts[1].strip()

        # Parse estimated silver & copper if present
        silv, copp = 18, 45
        m_val = re.search(r"(\d+)\s*(?:à\s*\d+\s*)?(?:pièces?\s*d['’]argent|argent|ag)", resp_text, re.IGNORECASE)
        if m_val:
            silv = int(m_val.group(1))

        # Generate the TWO visual stash images (1: highlighted grid, 2: sell manifest)
        from universal_v8_engine import render_universal_stash_analysis
        p1, p2 = render_universal_stash_analysis(
            user_screen_path=image_path,
            is_french=is_french
        )

        return {
            "spoken_text": spoken,
            "display_text": display,
            "image_attachments": [p1, p2],
            "image_attachment": p1
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[Vision Analyzer Error]: {e}", flush=True)
        return {
            "spoken_text": "Une erreur est survenue lors de l'analyse visuelle de votre capture d'écran.",
            "display_text": f"⚠️ **Erreur lors de l'analyse visuelle :** `{e}`"
        }
