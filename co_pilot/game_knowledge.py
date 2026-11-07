import re
import os
import sys
import json
import sqlite3
import random
import math
from typing import Dict, Any, Optional, List, Tuple

DOC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(DOC_DIR, "hunger_helper.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------------------------
# 1. VERBAL LEARNING & UNKNOWN TERMS
# ---------------------------------------------------------------------------

def get_learned_terms() -> Dict[str, str]:
    """Retrieve all user-taught terms and their meanings."""
    conn = get_db_connection()
    c = conn.cursor()
    terms = {}
    try:
        c.execute("SELECT term, meaning FROM learned_terms")
        for row in c.fetchall():
            terms[row["term"].lower()] = row["meaning"]
    except Exception:
        pass
    finally:
        conn.close()
    return terms

def save_learned_term(term: str, meaning: str, added_by: str = "Commander") -> bool:
    """Store a newly explained term into the database."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT OR REPLACE INTO learned_terms (term, meaning, added_by, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (term.strip().lower(), meaning.strip(), added_by))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Learning DB Error]: {e}")
        return False
    finally:
        conn.close()

# ---------------------------------------------------------------------------
# 2. CUSTOM USER FARM ITEMS
# ---------------------------------------------------------------------------

def add_custom_farm_item(user_id: str, item_name: str, reason: str = "") -> bool:
    """Add a custom item to the user's keep/farm list (e.g. for cosmetics)."""
    conn = get_db_connection()
    c = conn.cursor()
    slug = item_name.strip().lower().replace(" ", "-")
    try:
        c.execute("""
            INSERT INTO user_custom_farm (user_id, item_slug, item_name, reason, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, slug, item_name.strip(), reason.strip()))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Custom Farm DB Error]: {e}")
        return False
    finally:
        conn.close()

def get_custom_farm_items(user_id: str) -> List[Dict[str, Any]]:
    """Retrieve all custom items the user requested to keep/farm."""
    conn = get_db_connection()
    c = conn.cursor()
    items = []
    try:
        c.execute("SELECT item_name, reason, updated_at FROM user_custom_farm WHERE user_id = ?", (user_id,))
        for r in c.fetchall():
            items.append({"name": r["item_name"], "reason": r["reason"]})
    except Exception:
        pass
    finally:
        conn.close()
    return items

# ---------------------------------------------------------------------------
# 3. WEAPONS INTEL (Thrust, Slash, Overhead, Sell Price)
# ---------------------------------------------------------------------------

def answer_weapon_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answer queries regarding weapon damage stats, firearms, 1-handed, 2-handed weapons, Pricker, etc."""
    lowered = query.lower()
    from universal_v8_engine import (
        render_pure_english_firearm_card,
        render_pure_english_melee_card,
        render_two_handed_melee_overview_card,
        render_one_handed_melee_overview_card,
        get_firearms_database
    )

    # 0. 2-HANDED MELEE WEAPONS QUERY ("show me every 2 hand melee", "armes a 2 main", "2 mains", "two handed")
    if any(w in lowered for w in [
        "2 hand", "two hand", "2-hand", "two-handed", "2-handed", "two handed",
        "2 main", "2 mains", "deux main", "deux mains", "2-main", "2mains", "2main"
    ]):
        card_p = render_two_handed_melee_overview_card()
        spoken = "All official two-handed melee weapons in Hunger dispatched: Zweihander, Halberd, Spear, and War Axe."
        display = (
            "⚔️ **OFFICIAL 2-HANDED MELEE ARSENAL (HUNGER COMPANION)**\n\n"
            "• 🥇 **Zweihänder (Legendary)** : 52.0 Thrust | 82.0 Heavy | 52.0 Light (3 hits vs Legendary Armor)\n"
            "• 🥈 **Halberd (Epic)** : 50.6 Thrust | 70.0 Heavy | 46.0 Light (3 hits vs Legendary Armor)\n"
            "• 🥉 **Spear (Rare)** : 48.3 Thrust | 58.0 Heavy | 42.0 Light (4 hits vs Legendary Armor)\n"
            "• 🛡️ **War Axe (Rare)** : 32.0 Thrust | 60.0 Heavy | 40.0 Light (4 hits vs Legendary Armor)\n\n"
            "*(Comparative 4-weapon analytical dossier attached below)*"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

    # 0.5 1-HANDED MELEE WEAPONS QUERY ("show me every 1 hand melee", "armes a 1 main", "1 main", "one handed")
    if any(w in lowered for w in [
        "1 hand", "one hand", "1-hand", "one-handed", "1-handed", "one handed",
        "1 main", "une main", "1 mains", "une mains", "1-main", "1main"
    ]):
        card_p = render_one_handed_melee_overview_card()
        spoken = "All 8 official one-handed melee weapons in Hunger dispatched: Sabre, Rapier, Axe, Mace, Short Sword, Club, Dagger, and Pricker."
        display = (
            "🗡️ **OFFICIAL 1-HANDED MELEE ARSENAL (HUNGER COMPANION)**\n\n"
            "• 🥇 **Sabre (Epic)** : 34.0 Thrust | 50.0 Heavy | 34.0 Light (4 hits vs Epic Armor)\n"
            "• 🥈 **Rapier (Rare)** : 30.8 Thrust | 42.0 Heavy | 28.0 Light (5 hits vs Epic Armor)\n"
            "• 🥉 **Axe (Rare)** : 15.0 Thrust | 44.0 Heavy | 30.0 Light (5 hits vs Epic Armor)\n"
            "• 🔨 **Mace (Uncommon)** : 24.0 Thrust | 40.0 Heavy | 30.0 Light (5 hits vs Epic Armor)\n"
            "• ⚔️ **Short Sword (Uncommon)** : 26.0 Thrust | 34.0 Heavy | 26.0 Light (6 hits vs Epic Armor)\n"
            "• 🪵 **Club (Common)** : 17.0 Thrust | 43.0 Heavy | 34.0 Light (5 hits vs Epic Armor)\n"
            "• 🗡️ **Dagger (Common)** : 25.2 Thrust | 30.0 Heavy | 24.0 Light (7 hits vs Epic Armor)\n"
            "• 📌 **Pricker (Common)** : 21.0 Thrust | 25.0 Heavy | 20.0 Light (8 hits vs Epic Armor)\n\n"
            "*(Full 8-weapon comparison grid attached below)*"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

    # 1. FIREARMS LOOKUP (ALL 24 FIREARMS: Borodino, Volcan, Vepr, Marengo, Drak, etc.)
    f_db = get_firearms_database()
    firearm_slug = None
    clean_q = re.sub(r"\blash\b", "lasher", lowered.replace("borondi", "borodino").replace("brown betty", "brown-betty").replace("long boy", "longboy"))
    for slug, f_info in f_db.items():
        if slug in clean_q or f_info["name"].lower() in clean_q:
            if slug == "deux" and ("deux main" in lowered or "deux-main" in lowered):
                continue
            firearm_slug = slug
            break
            
    if firearm_slug:
        f_info = f_db[firearm_slug]
        card_path = render_pure_english_firearm_card(firearm_slug, is_french=False)
        fn_title = f"{f_info['name']} ({f_info['rarity']} {f_info['type']})"
        dmg = int(f_info['damage'])
        head = int(f_info['headshot'])
        clip = f_info['clip']
        reload_t = f_info['reload']
        ammo = f_info['ammo']
        vendor = f_info['vendor']
        
        spoken = f"{f_info['name']} deals {dmg} base damage ({head} headshot) chambering {ammo}. Technical dossier dispatched."
        display = (
            f"🎯 **FIREARM BALLISTIC DOSSIER : {f_info['name'].upper()}**\n\n"
            f"• 💥 **Base Damage :** **{dmg} per shot** | 🎯 **Headshot Critical :** **{head} dmg**\n"
            f"• 🔄 **Magazine Capacity :** **{clip}** | ⚡ **Tactical Reload :** **{reload_t}**\n"
            f"• 📦 **Ammunition :** **{ammo}** | 🏷️ **Rarity :** **{f_info['rarity']}**\n"
            f"• 🛒 **Merchant Availability :** {vendor}\n\n"
            f"*(Authentic weapon card attached below)*"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 2. MELEE WEAPONS THRUST RANKING
    conn = get_db_connection()
    c = conn.cursor()

    is_thrust = any(w in lowered for w in ["thrust", "estoc", "pénétration", "penetration", "perce", "pierce"])
    if is_thrust and any(w in lowered for w in ["meilleur", "meilleure", "plus grand", "plus fort", "best", "highest", "top", "max"]):
        c.execute("SELECT name_en, name_fr, rarity_en, rarity_fr, thrust_damage FROM weapons WHERE thrust_damage > 0 ORDER BY thrust_damage DESC LIMIT 3")
        top3 = c.fetchall()
        conn.close()
        card_path = render_pure_english_melee_card("zweihander")
        spoken = "The weapon with the highest thrust damage is the Legendary Zweihander with 52, followed by the Halberd with 50.6, and the Spear with 48.3."
        top_str = "\n".join([f"  {idx}. **{r['name_en']}** ({r['rarity_en']}) : **{r['thrust_damage']}** thrust" for idx, r in enumerate(top3, 1)])
        display = (
            f"🏆 **HIGHEST THRUST DAMAGE WEAPONS (HUNGER COMPANION) :**\n\n{top_str}\n\n"
            f"• 🥇 **Zweihander (Legendary)** : **52** thrust damage\n"
            f"• 🥈 **Halberd (Epic)** : **50.6** thrust damage\n"
            f"• 🥉 **Spear (Rare)** : **48.3** thrust damage"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 3. INDIVIDUAL MELEE WEAPONS LOOKUP
    c.execute("SELECT * FROM weapons")
    weapons = c.fetchall()
    conn.close()

    for w_row in weapons:
        w = dict(w_row)
        w_slug = w["slug"]
        w_en = w["name_en"].lower()
        w_fr = w["name_fr"].lower()
        if w_slug in lowered or w_en in lowered or (len(w_fr) >= 4 and w_fr in lowered):
            card_path = render_pure_english_melee_card(w_slug)
            w_name = w["name_en"]
            rarity = w.get("rarity_en", "Common")
            t_dmg = w.get("thrust_damage", 0)
            l_dmg = w.get("light_damage", 0)
            h_dmg = w.get("heavy_damage", 0)
            sell_p = w.get("sell_price", "1 0")

            spoken = f"{w_name} ({rarity}) deals {t_dmg} thrust, {h_dmg} heavy, and {l_dmg} light damage. Card dispatched."
            display = (
                f"🗡️ **MELEE WEAPON PROFILE : {w_name.upper()} ({rarity.upper()})**\n\n"
                f"• 🎯 **Thrust Damage :** **{t_dmg}**\n"
                f"• 💥 **Heavy Strike :** **{h_dmg}**\n"
                f"• ⚔️ **Light Strike :** **{l_dmg}** (Out of energy: {w.get('light_no_energy', 10)})\n"
                f"• 💰 **Sell Price :** **{sell_p}**\n\n"
                f"*(Authentic directional attack compass card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    return None


def answer_effect_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answer queries regarding poison antiheal, duration, and mechanics."""
    lowered = query.lower()
    
    # 1. Does poison have antiheal?
    if "poison" in lowered and any(w in lowered for w in ["antiheal", "anti-soin", "anti soin", "soin", "heal", "empêche", "soigner"]):
        if is_french:
            spoken = (
                "Non, le poison n'a aucun effet d'anti-soin dans Hunger. "
                "Il inflige 0,1 dégât par seconde en ignorant l'armure, mais vous pouvez librement vous soigner avec des baumes ou bandages."
            )
            display = (
                f"🧪 **MÉCANIQUE DU POISON & SOIN :**\n\n"
                f"❌ **Effet Anti-Soin (Antiheal) :** **NON**\n"
                f"Le poison n'empêche **absolument pas** de se soigner. Vous pouvez consommer baumes, remèdes et bandages sans malus d'efficacité.\n\n"
                f"⚡ **Effets réels du Poison :**\n"
                f"• **Dégâts :** 0.1 dégât/seconde (ignore totalement l'armure).\n"
                f"• **Light Poison :** Dure 2 minutes (12 dégâts totaux).\n"
                f"• **Mid Poison :** Dure 4 minutes (24 dégâts totaux).\n"
                f"• **Heavy Poison :** Dure 6 minutes (36 dégâts totaux).\n"
                f"• **Remède :** Remèdes médicinaux de Jacques ou immunité au poison."
            )
        else:
            spoken = (
                "No, poison does not apply an antiheal effect in Hunger. "
                "It deals 0.1 damage per second ignoring armor, but you can freely use balms or bandages to heal."
            )
            display = (
                f"🧪 **POISON & HEALING MECHANICS :**\n\n"
                f"❌ **Antiheal Effect :** **NO**\n"
                f"Poison does **not** reduce or block healing. You can use medical balms, draughts, and bandages freely.\n\n"
                f"⚡ **True Poison Effects :**\n"
                f"• **Damage :** 0.1 damage/s (ignores armor completely).\n"
                f"• **Light Poison :** Lasts 2 minutes (12 total damage).\n"
                f"• **Mid Poison :** Lasts 4 minutes (24 total damage).\n"
                f"• **Heavy Poison :** Lasts 6 minutes (36 total damage).\n"
                f"• **Cure :** Jacques Medicinals or poison immunity perks."
            )
        return {"spoken_text": spoken, "display_text": display}


    # 1.1 Poison duration specific handler
    if "poison" in lowered and any(w in lowered for w in ["combien de temps", "how long", "durée", "duree", "duration", "dure", "dur"]):
        if is_french:
            spoken = "Le poison dure 2 minutes en niveau léger, 4 minutes en moyen et 6 minutes en lourd."
            display = (
                "🧪 **DURÉE DES EFFETS DE POISON :**\n\n"
                "• 🟢 **Poison Léger (Light)** : **2 minutes** (12 dégâts totaux)\n"
                "• 🟡 **Poison Moyen (Mid)** : **4 minutes** (24 dégâts totaux)\n"
                "• 🔴 **Poison Lourd (Heavy)** : **6 minutes** (36 dégâts totaux)\n\n"
                "💡 *Dégâts : 0.1 PV/seconde ignorant l'armure. Guérissable avec un remède de Jacques.*"
            )
        else:
            spoken = "Poison lasts 2 minutes for Light, 4 minutes for Mid, and 6 minutes for Heavy."
            display = "🧪 **POISON DURATION TIERS**\n• Light: 2 min\n• Mid: 4 min\n• Heavy: 6 min"
        return {"spoken_text": spoken, "display_text": display}


    # 1.2 Bleed duration specific handler
    if any(w in lowered for w in ["saignement", "bleed", "saigne"]) and any(w in lowered for w in ["combien de temps", "how long", "durée", "duree", "duration", "dure", "dur"]):
        if is_french:
            spoken = "Le saignement dure 10 secondes en léger, 20 secondes en moyen et 30 secondes en lourd."
            display = (
                "🩸 **DURÉE DES EFFETS DE SAIGNEMENT :**\n\n"
                "• 🟢 **Saignement Léger (Light)** : **10 secondes**\n"
                "• 🟡 **Saignement Moyen (Mid)** : **20 secondes**\n"
                "• 🔴 **Saignement Lourd (Heavy)** : **30 secondes**\n\n"
                "💡 *Stoppé immédiatement avec des bandages ou le tactical de Marie.*"
            )
        else:
            spoken = "Bleed lasts 10 seconds for Light, 20 seconds for Mid, and 30 seconds for Heavy."
            display = "🩸 **BLEED DURATION TIERS**\n• Light: 10s\n• Mid: 20s\n• Heavy: 30s"
        return {"spoken_text": spoken, "display_text": display}


    # 2. General duration query
    if any(w in lowered for w in ["combien de temps", "how long", "durée", "duree", "duration", "dure", "dur"]):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM effects")
        rows = c.fetchall()
        conn.close()
        for r in rows:
            if r["slug"].replace("-", " ") in lowered or r["name_en"].lower() in lowered or r["name_fr"].lower() in lowered:
                if is_french:
                    spoken = f"L'effet {r['name_fr']} dure {r['duration_fr']}."
                    display = f"⏱️ **Effet {r['name_fr']} :** Durée **{r['duration_fr']}**.\n{r['description_fr']}"
                else:
                    spoken = f"The effect {r['name_en']} lasts {r['duration_en']}."
                    display = f"⏱️ **Effect {r['name_en']} :** Duration **{r['duration_en']}**.\n{r['description_en']}"
                return {"spoken_text": spoken, "display_text": display}


    # 3. Item causing an effect / effect of an item
    if any(w in lowered for w in ["fait tel effet", "provoque", "cause", "applique", "effet"]):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM effects")
        rows = c.fetchall()
        conn.close()
        for r in rows:
            if r["slug"].replace("-", " ") in lowered or r["name_en"].lower() in lowered or r["name_fr"].lower() in lowered:
                if is_french:
                    spoken = f"L'effet {r['name_fr']} ({r['duration_fr']}) : {r['description_fr']}."
                    display = f"🧪 **EFFET : {r['name_fr'].upper()}**\n• ⏱️ Durée : {r['duration_fr']}\n• 📝 Description : {r['description_fr']}"
                else:
                    spoken = f"The effect {r['name_en']} ({r['duration_en']}): {r['description_en']}."
                    display = f"🧪 **EFFECT : {r['name_en'].upper()}**\n• ⏱️ Duration: {r['duration_en']}\n• 📝 Description: {r['description_en']}"
                return {"spoken_text": spoken, "display_text": display}


    return None

# ---------------------------------------------------------------------------
# 5. DUNGEONS & KEYS INTEL (Jacques Folly, Entrances, Big Chest, Keys)
# ---------------------------------------------------------------------------

def answer_dungeon_key_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answer queries regarding Jacques Folly dungeon, key spawns, and locked chests."""
    lowered = query.lower()
    
    if any(w in lowered for w in ["folly", "donjon", "dungeon", "gros chest", "gros coffre", "clef", "clé", "key"]):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM dungeons_and_places WHERE slug = 'jacques-folly'")
        folly = c.fetchone()
        c.execute("SELECT * FROM keys_data WHERE slug = 'jacques-folly-key'")
        kdata = c.fetchone()
        conn.close()

        if folly and kdata:
            if is_french:
                spoken = (
                    "Le donjon de Jacques Folly se situe sous le pont Jacques aux coordonnées 1680, 197. "
                    "Il contient 174 conteneurs et nécessite la Clé de la folie de Jacques (3 usages), trouvable sur 5 spots du pont ou sur les Baveux et Brutes."
                )
                display = (
                    f"🏰 **DONJON : FOLIE DE JACQUES (JACQUES FOLLY) :**\n\n"
                    f"📍 **Emplacement :** Pont Jacques (`X: 1680.37, Y: 197.12`)\n"
                    f"📦 **Conteneurs :** 174 conteneurs (Grands coffres renforcés, armoires, bureaux)\n"
                    f"👾 **Ennemis :** 84 points de spawn de créatures (Baveux, Brutes, Dregs)\n"
                    f"🚪 **Accès (3 portes d'entrée verrouillées) :**\n"
                    f"  1. Porte Nord (`X: 1835.90, Y: 505.49`)\n"
                    f"  2. Crypte de la cour (`X: 1605.21, Y: 512.75`)\n"
                    f"  3. Porte de fer du sous-sol (`X: 1418.37, Y: 337.55`)\n\n"
                    f"🔑 **Clé requise :** **Clé de la folie de Jacques** (Épique, 3 utilisations, revente : 82ag 12c)\n"
                    f"🎯 **Spawns de la clé :** 5 emplacements sur le Pont Jacques (taux 1/133) et butin rare sur Baveux / Brute (taux 1/226)."
                )
            else:
                spoken = (
                    "The Jacques Folly dungeon is located under Jacques Bridge at coordinates 1680, 197. "
                    "It has 174 containers and requires the Jacques Folly Key (3 uses), found at 5 spots on the bridge or dropped by Droolers and Brutes."
                )
                display = (
                    f"🏰 **DUNGEON : JACQUES FOLLY :**\n\n"
                    f"📍 **Location :** Jacques Bridge (`X: 1680.37, Y: 197.12`)\n"
                    f"📦 **Loot :** 174 containers (Large reinforced strongboxes, cabinets, desks)\n"
                    f"👾 **Encounters :** 84 creature spawn points (Droolers, Brutes, Dregs)\n"
                    f"🚪 **Entrances (3 locked doors) :**\n"
                    f"  1. North Gate (`X: 1835.90, Y: 505.49`)\n"
                    f"  2. Courtyard Crypt (`X: 1605.21, Y: 512.75`)\n"
                    f"  3. Undercroft Iron Door (`X: 1418.37, Y: 337.55`)\n\n"
                    f"🔑 **Key Required :** **Jacques Folly Key** (Epic, 3 uses, sell: 82s 12c)\n"
                    f"🎯 **Key Spawns :** 5 spots across Jacques Bridge (1/133 rate) and rare monster drops from Droolers / Brutes (1/226)."
                )
            return {"spoken_text": spoken, "display_text": display}


    return None

# ---------------------------------------------------------------------------
# 6. MERCHANT STOCK & ITEM AVAILABILITY ("quel marchand vend...")
# ---------------------------------------------------------------------------

MERCHANT_ITEMS = {
    "longboy": {"merchant": "Reynauld ou Piro", "stock": "Arme Longboy (Taux : 35%)", "location": "Château / Marché"},
    "bloodbag": {"merchant": "Piro", "stock": "Sealed Bloodbag (Poche de sang scellée) (Taux : 55%)", "location": "Feu de fumée du château"},
    "sang": {"merchant": "Piro", "stock": "Sealed Bloodbag (Poche de sang scellée) (Taux : 55%)", "location": "Feu de fumée du château"},
    "seamstress": {"merchant": "Octave de Villiers", "stock": "5x Aiguilles de couturière (Seamstress Needle) (Taux : 85%)", "location": "Quartier noble du château"},
    "needle": {"merchant": "Octave de Villiers", "stock": "5x Aiguilles de couturière (Seamstress Needle) (Taux : 85%)", "location": "Quartier noble du château"},
    "aiguille": {"merchant": "Octave de Villiers", "stock": "5x Aiguilles de couturière (Seamstress Needle) (Taux : 85%)", "location": "Quartier noble du château"},
    "ammunition": {"merchant": "Reynauld ou Piro", "stock": "10x Heavy Ammunition (Munitions lourdes) (Taux : 100%)", "location": "Forge du château"},
    "munitions": {"merchant": "Reynauld ou Piro", "stock": "10x Heavy Ammunition (Munitions lourdes) (Taux : 100%)", "location": "Forge du château"},
    "branch": {"merchant": "Reynauld", "stock": "2x Thick Branch (Grosses branches) (Taux : 100%)", "location": "Forge / Entrée château"},
    "branche": {"merchant": "Reynauld", "stock": "2x Thick Branch (Grosses branches) (Taux : 100%)", "location": "Forge / Entrée château"}
}

def answer_merchant_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answers which merchant sells a specific item."""
    lowered = query.lower()
    for key, data in MERCHANT_ITEMS.items():
        if key in lowered:
            if is_french:
                spoken = f"{data['merchant']} vend cet objet : {data['stock']} à {data['location']}."
                display = (
                    f"🛒 **MARCHAND TROUVÉ :**\n"
                    f"• 👤 **Marchand :** **{data['merchant']}**\n"
                    f"• 📦 **Stock :** {data['stock']}\n"
                    f"• 📍 **Emplacement :** {data['location']}\n"
                    f"💡 *Cet item est disponible à l'achat, inutile de risquer un raid pour le farmer.*"
                )
            else:
                spoken = f"{data['merchant']} sells this item: {data['stock']} at {data['location']}."
                display = (
                    f"🛒 **MERCHANT LOCATED :**\n"
                    f"• 👤 **Merchant :** **{data['merchant']}**\n"
                    f"• 📦 **Stock :** {data['stock']}\n"
                    f"• 📍 **Location :** {data['location']}\n"
                    f"💡 *This item can be purchased directly from the vendor.*"
                )
            return {"spoken_text": spoken, "display_text": display}

    return None

# ---------------------------------------------------------------------------
# 7. RANDOM LORE & GAME FACTS
# ---------------------------------------------------------------------------

def answer_random_fact_query(is_french: bool) -> Dict[str, str]:
    """Provide a captivating random lore or mechanics fact from Hunger Companion."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM lore_facts ORDER BY RANDOM() LIMIT 1")
    fact = c.fetchone()
    conn.close()

    if not fact:
        if is_french:
            return {"spoken_text": "Fait tactique : Le Zweihänder inflige les plus gros dégâts d'estoc du jeu avec 52 points.", "display_text": "📜 **Fait du jeu :** Le Zweihänder est l'arme d'estoc la plus puissante (52 dégâts)."}
        else:
            return {"spoken_text": "Tactical fact: The Zweihänder deals the highest thrust damage in the game at 52 points.", "display_text": "📜 **Game Fact:** The Zweihänder deals the highest thrust damage in the game (52 thrust)."}

    if is_french:
        spoken = f"Voici un fait sur {fact['title_fr']} : {fact['text_fr'][:120]}..."
        display = f"📜 **LE SAVIEZ-VOUS ? — {fact['title_fr'].upper()} :**\n\n{fact['text_fr']}"
    else:
        spoken = f"Here is a fact regarding {fact['title_en']} : {fact['text_en'][:120]}..."
        display = f"📜 **DID YOU KNOW? — {fact['title_en'].upper()} :**\n\n{fact['text_en']}"

    return {"spoken_text": spoken, "display_text": display}


# ---------------------------------------------------------------------------
# 8. TOP 3 BEST CONTAINERS FOR AN ITEM
# ---------------------------------------------------------------------------

def answer_best_containers_query(item_query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Determine top container sources with highest drop rate for any item."""
    conn = get_db_connection()
    c = conn.cursor()
    
    clean_item = item_query.replace("drop", "").replace("farm", "").replace("container", "").replace("conteneur", "").strip()
    c.execute("""
        SELECT d.source, d.location, d.drop_rate, i.name
        FROM item_drops d
        JOIN items i ON d.item_id = i.id
        WHERE i.name LIKE ? OR i.slug LIKE ?
        ORDER BY d.drop_rate DESC
        LIMIT 3
    """, (f"%{clean_item}%", f"%{clean_item}%"))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return None

    item_name = rows[0]["name"]
    if is_french:
        c_lines = [f"  {idx}. **{r['source']}** sur *{r['location']}* : Taux de drop **{r['drop_rate']*100:.1f}%**" for idx, r in enumerate(rows, 1)]
        spoken = f"Les meilleurs conteneurs pour trouver {item_name} sont : {rows[0]['source']} avec {rows[0]['drop_rate']*100:.1f}% de chance."
        display = (
            f"📦 **LES 3 MEILLEURS CONTENEURS POUR : {item_name.upper()}**\n\n" +
            "\n".join(c_lines) +
            f"\n\n💡 *Astuce : Privilégiez {rows[0]['source']} lors de vos passages en raid.*"
        )
    else:
        c_lines = [f"  {idx}. **{r['source']}** in *{r['location']}* : Drop rate **{r['drop_rate']*100:.1f}%**" for idx, r in enumerate(rows, 1)]
        spoken = f"The best containers to drop {item_name} are: {rows[0]['source']} with a {rows[0]['drop_rate']*100:.1f}% chance."
        display = (
            f"📦 **TOP 3 CONTAINERS FOR : {item_name.upper()}**\n\n" +
            "\n".join(c_lines) +
            f"\n\n💡 *Tip: Prioritize {rows[0]['source']} on your raid routes.*"
        )

    return {"spoken_text": spoken, "display_text": display}


# ---------------------------------------------------------------------------
# 9. ITEMS TO KEEP INFOGRAPHIC & GUIDE (RENDERED FROM PROGRESSION)
# ---------------------------------------------------------------------------

def get_or_render_items_to_keep(user_id: str, is_french: bool) -> Tuple[str, str, str]:
    """Generates and returns (image_path, spoken_text, display_text) for items to keep."""
    if DOC_DIR not in sys.path:
        sys.path.insert(0, DOC_DIR)
    import render_progression_checked_guide as rguide
    out_path = os.path.join(DOC_DIR, "merchant_quest_items_guide.png")
    try:
        rguide.render()
    except Exception as e:
        print(f"[Guide Render Error]: {e}")
    
    custom_items = get_custom_farm_items(user_id)
    custom_str = ""
    if custom_items:
        custom_lines = [f"• **{it['name']}** (Raison : {it['reason'] or 'Farm personnalisé'})" for it in custom_items]
        custom_str = "\n\n🎒 **Vos items personnalisés ajoutés à garder :**\n" + "\n".join(custom_lines)

    if is_french:
        spoken = (
            "Voici le guide visuel complet des items à garder selon votre progression de quêtes. "
            "Il sépare les 5 items achetables aux marchands des 22 items à trouver uniquement en raid, triés par rareté."
        )
        display = (
            "📋 **GUIDE COMPLET DES ITEMS À GARDER (PROGRESSION DE QUÊTES) :**\n\n"
            "🟢 **1. ITEMS ACHETABLES AUX MARCHANDS :**\n"
            "• **Longboy Weapon** : Reynauld / Piro (35%)\n"
            "• **Sealed Bloodbag** : Piro au feu de fumée (55%)\n"
            "• **Seamstress Needle (5x)** : Octave de Villiers (85%)\n"
            "• **Heavy Ammunition (10x)** : Reynauld / Piro (100%)\n"
            "• **Thick Branch (2x)** : Reynauld (100%)\n\n"
            "🔴 **2. ITEMS EXCLUSIFS AUX RAIDS (NE PAS VENDRE !) :**\n"
            "• 🟡 **Très rares (<15%)** : Tallow Balm (Armoire médecin 9.1%), Arsenic (Jacques 10.6%), Opium Pipe (Coffre 13.7%)\n"
            "• 🟣 **Rares (15-35%)** : China Bowl (16.1%), Saltpetre (18.9%), Glass Vial (20.4%), Silver Dish (23.8%), Damp Rag (23.8%), Bezoar (35%)\n"
            "• 🔵 **Peu communs (40-60%)** : Hartshorn (45%), Flour (47.6%), Opium (47.6%), Charcoal (52.6%), Tavern Wine (55%), Thin Mead (55%)\n"
            f"{custom_str}\n\n"
            "🖼️ *Image haute résolution 2560x1440 jointe ci-dessous.*"
        )
    else:
        spoken = (
            "Here is the complete visual guide of items to keep based on your quest progression. "
            "Separating the 5 buyable items from the 22 raid-exclusive items, ranked by rarity."
        )
        display = (
            "📋 **COMPLETE GUIDE OF ITEMS TO KEEP (QUEST PROGRESSION) :**\n\n"
            "🟢 **1. BUYABLE FROM MERCHANTS :**\n"
            "• **Longboy Weapon** : Reynauld / Piro (35%)\n"
            "• **Sealed Bloodbag** : Piro at smoke fire (55%)\n"
            "• **Seamstress Needle (5x)** : Octave de Villiers (85%)\n"
            "• **Heavy Ammunition (10x)** : Reynauld / Piro (100%)\n"
            "• **Thick Branch (2x)** : Reynauld (100%)\n\n"
            "🔴 **2. RAID LOOT ONLY (DO NOT SELL !) :**\n"
            "• 🟡 **Rarest (<15%)** : Tallow Balm (9.1%), Arsenic (10.6%), Opium Pipe (13.7%)\n"
            "• 🟣 **Rare (15-35%)** : China Bowl (16.1%), Saltpetre (18.9%), Glass Vial (20.4%), Silver Dish (23.8%), Damp Rag (23.8%), Bezoar (35%)\n"
            "• 🔵 **Uncommon (40-60%)** : Hartshorn (45%), Flour (47.6%), Opium (47.6%), Charcoal (52.6%), Tavern Wine (55%), Thin Mead (55%)\n"
            f"{custom_str}\n\n"
            "🖼️ *High resolution 2560x1440 infographic attached below.*"
        )
    return out_path, spoken, display

# ---------------------------------------------------------------------------
# 10. EXTRACTION INTEL (Sarlat Farm, Jacques Bridge, Sombre Forest)
# ---------------------------------------------------------------------------

EXTRACTIONS_DATA = {
    "sarlat": {
        "name": "Sarlat Farm",
        "extracts": [
            ("Charrette de la Grange aux Dîmes (Tithe Barn)", "Est de la carte, toujours ouverte, point le plus rapide après les coffres du village."),
            ("Pont de la Route du Moulin (Mill Road Bridge)", "Nord-Est, sortie sécurisée à couvert le long du ravin."),
            ("Porte du Cimetière de la Chapelle (Church Cemetery)", "Centre-Sud près de la chapelle, attention aux patrouilles de Baveux.")
        ]
    },
    "jacques": {
        "name": "Jacques Bridge",
        "extracts": [
            ("Barricade de la Route Nord (North Highway)", "Extrémité Nord du pont, sortie directe sur la chaussée pavée."),
            ("Barque sous le Pont (River Underpass Boat)", "Sous les arches centrales près du donjon de Jacques Folly."),
            ("Rempart Sud de la Tour (Watchtower South)", "Bastion Sud en hauteur, surplombe la berge.")
        ]
    },
    "sombre": {
        "name": "Sombre Forest",
        "extracts": [
            ("Sentier de l'Ancienne Crypte (Old Crypt Path)", "Nord-Ouest, nécessite de traverser la ravine brumeuse."),
            ("Charrette du Bûcheron (Woodcutter's Cart)", "Sud-Est, extraction dégagée."),
            ("Palissade Frontalière (Forest Border)", "Sud-Ouest, sortie discrète le long de la palissade de pierre.")
        ]
    }
}

def answer_extraction_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Provide tactical extraction locations and requirements for any map."""
    lowered = query.lower()
    if not any(w in lowered for w in ["extraction", "extractions", "extraire", "extract", "extracts", "sortie", "sorties", "sortir"]):
        return None

    target = "sarlat"
    if any(w in lowered for w in ["jacques", "pont", "bridge"]):
        target = "jacques"
    elif any(w in lowered for w in ["sombre", "forest", "forêt", "foret"]):
        target = "sombre"

    data = EXTRACTIONS_DATA[target]
    m_name = data["name"]

    if is_french:
        lines = [f"• 🚪 **{ex[0]}** : {ex[1]}" for ex in data["extracts"]]
        spoken = f"Sur {m_name}, vous avez 3 extractions principales : {data['extracts'][0][0]} à l'est, et {data['extracts'][1][0]} au nord."
        display = (
            f"🚪 **POINTS D'EXTRACTION : {m_name.upper()}**\n\n" +
            "\n\n".join(lines) +
            f"\n\n💡 *Conseil tactique : Rejoignez l'extraction avec au moins 30 secondes d'endurance d'avance pour éviter d'être encerclé.*"
        )
    else:
        lines = [f"• 🚪 **{ex[0]}** : {ex[1]}" for ex in data["extracts"]]
        spoken = f"On {m_name}, you have 3 primary extractions: {data['extracts'][0][0]} and {data['extracts'][1][0]}."
        display = (
            f"🚪 **EXTRACTION POINTS : {m_name.upper()}**\n\n" +
            "\n\n".join(lines) +
            f"\n\n💡 *Tactical Tip: Arrive at extraction with at least 30s of stamina to spare to prevent ambush.*"
        )

    return {"spoken_text": spoken, "display_text": display}


# ---------------------------------------------------------------------------
# 11. TALENT ADVICE & BUILDS
# ---------------------------------------------------------------------------

def answer_talent_advice_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answers queries regarding the user's authentic Hunger Companion talent build (91 points)."""
    lowered = query.lower()
    if not any(w in lowered for w in ["talent", "talents", "build", "arbre", "competence", "compétence", "stats", "maîtrise", "maitrise"]):
        return None

    from co_pilot.card_renderer import render_talent_build_cards_both
    p1, p2 = render_talent_build_cards_both()
    card_path = p1

    if is_french:
        spoken = (
            "Voici votre arbre de talents officiel à 91 points : "
            "37 points en Arms avec Deft Strikes à 5 sur 5 pour le Zweihänder, "
            "36 points en Survival avec Surgeon à 5 sur 5, et 18 points en Physiology. Fiche transmise."
        )
        display = (
            "🌲 **VOTRE ARBRE DE TALENTS ACTUEL (91 POINTS DÉPENSÉS) :**\n\n"
            "• 🗡️ **ARMS (37 / 71) — Focus Armes Lourdes & Mêlée :**\n"
            "  - **Deft Strikes (5/5) :** -25% d'énergie sur les attaques légères à 2 mains (parfait pour le Zweihänder).\n"
            "  - Paliers I à VII complétés avec **Maîtrise Tier VIII d'Armes débloquée**.\n\n"
            "• 💉 **SURVIVAL (36 / 78) — Résilience & Soutien d'Escouade :**\n"
            "  - **Surgeon (5/5) :** Relève les coéquipiers au sol 25% plus vite en combat.\n"
            "  - Soins au feu de camp, résistance et **Maîtrise Tier VIII de Survie débloquée**.\n\n"
            "• 🏃 **PHYSIOLOGY (18 / 83) — Mobilité & Vitalité :**\n"
            "  - Sprint prolongé (5/5), Vitalité max (5/5), Agilité au saut (5/5), Coagulation (3/5).\n\n"
            "• 🔒 **MARTIAL (0/74) & CUNNING (0/72) :** Aucun point investi (focus pur mêlée et survie).\n\n"
            "💡 *Fiche haute résolution reproduisant fidèlement l'arbre Hunger Companion jointe ci-dessous.*"
        )
    else:
        spoken = (
            "Here is your official 91-point Hunger Companion talent build: "
            "37 points in Arms with Deft Strikes at 5 out of 5 for two-handed melee, "
            "36 points in Survival with Surgeon at 5 out of 5, and 18 points in Physiology. Card dispatched."
        )
        display = (
            "🌲 **YOUR CURRENT TALENT BUILD (91 POINTS ALLOCATED) :**\n\n"
            "• 🗡️ **ARMS (37 / 71) :** Deft Strikes (5/5) -25% energy for 2H melee + Tier VIII Mastery.\n"
            "• 💉 **SURVIVAL (36 / 78) :** Surgeon (5/5) +25% revive speed + Tier VIII Mastery.\n"
            "• 🏃 **PHYSIOLOGY (18 / 83) :** Sprint stamina (5/5), Max health (5/5), Jump agility (5/5), Clotting (3/5).\n"
            "• 🔒 **MARTIAL (0/74) & CUNNING (0/72) :** 0 points allocated."
        )

    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path, "image_attachments": [p1, p2]}

# ---------------------------------------------------------------------------
# 11. COMBAT TTK & HIT CALCULATOR ("combien de coups pour tuer X")
# ---------------------------------------------------------------------------

def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Calculates exact strikes / hits required to down enemies based on weapon and armor/creature HP."""
    lowered = query.lower()
    
    cleaned = re.sub(r"\blash\b", "lasher", lowered.replace("borondi", "borodino").replace("uer", "tuer").replace("brown betty", "brown-betty"))
    
    is_hit_query = any(w in cleaned for w in [
        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de tire", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un",
        "tuer en vert", "tuer en bleu", "tuer du violet", "tuer en violet", "joueur en vert", "joueur en cuir",
        "en combien de coup", "en combien de tire", "en combien de coups", "en combien de tir", "en combien de hit",
        "combien de hit", "combien de hits", "how many hit", "hit to kill", "htk", "ttk"
    ])
    if not is_hit_query:
        return None

    from universal_v8_engine import (
        render_pure_english_firearm_card,
        render_pure_english_melee_card,
        get_firearms_database
    )

    # 1. Target HP and Name Detection (All 6 Armor Tiers + Raid Creatures)
    is_naked = any(w in cleaned for w in ["sans armure", "nu", "naked", "no armour"])
    is_grey = any(w in cleaned for w in ["gris", "grise", "grey", "gray", "commune", "common", "padded", "en gris", "du gris"])
    is_green = any(w in cleaned for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert", "du vert"])
    is_blue = any(w in cleaned for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "du bleu"])
    is_epic = any(w in cleaned for w in ["violet", "violette", "pourpre", "épique", "epique", "en violet", "du violet", "epic"])
    is_legend = any(w in cleaned for w in ["légendaire", "legendaire", "legendary", "doré", "dore", "jaune", "en or", "du or", "gold"])
    is_brute = any(w in cleaned for w in ["brute", "gros"]) and not any(w in cleaned for w in ["joueur", "player"])
    is_drooler = any(w in cleaned for w in ["baveux", "drooler"]) and not any(w in cleaned for w in ["joueur", "player"])

    if is_naked:
        target_name = "Naked Player (100 HP)"
        target_hp = 100
    elif is_grey:
        target_name = "Grey / Common Armor Player (120 HP)"
        target_hp = 120
    elif is_green:
        target_name = "Green / Leather Armor Player (140 HP)"
        target_hp = 140
    elif is_blue:
        target_name = "Blue / Sapper Armor Player (160 HP)"
        target_hp = 160
    elif is_epic:
        target_name = "Epic Reinforced Armor Player (180 HP)"
        target_hp = 180
    elif is_legend:
        target_name = "Full Legendary Armor Player (200 HP)"
        target_hp = 200
    elif is_brute:
        target_name = "Brute Elite Creature (900 HP)"
        target_hp = 900
    elif is_drooler:
        target_name = "Drooler Creature (450 HP)"
        target_hp = 450
    else:
        target_name = "Green / Leather Armor Player (140 HP)"
        target_hp = 140

    # 2. Check Firearms FIRST (Borodino, Volcan, Vepr, Marengo, Drak, etc.)
    f_db = get_firearms_database()
    firearm_slug = None
    for slug, f_info in f_db.items():
        if slug in cleaned or f_info["name"].lower() in cleaned:
            if slug == "deux" and ("deux main" in cleaned or "deux-main" in cleaned):
                continue
            firearm_slug = slug
            break

    if firearm_slug:
        f_info = f_db[firearm_slug]
        card_path = render_pure_english_firearm_card(firearm_slug, is_french=False)
        f_name = f_info["name"]
        f_dmg = float(f_info["damage"])
        f_head = float(f_info["headshot"])

        t_head = max(1, math.ceil(target_hp / f_head))
        t_body = max(1, math.ceil(target_hp / f_dmg))

        if is_french:
            spoken = f"Avec {f_name}, il faut {t_head} tir(s) dans la tête ou {t_body} tir(s) au corps pour neutraliser un {target_name}."
            display = (
                f"🎯 **SIMULATEUR DE TIR & HTK : {f_name.upper()} vs {target_name.upper()}**\n\n"
                f"• 🔫 **Arme :** **{f_name}** ({f_info['rarity']} {f_info['type']}) — Dégâts : **{int(f_dmg)}** (Crit tête : **{int(f_head)}**)\n"
                f"• 🎯 **Cible :** **{target_name}**\n"
                f"• 💥 **Tirs Tête (Headshots) :** **{t_head} tir(s)**\n"
                f"• 🛡️ **Tirs Corps (Body) :** **{t_body} tir(s)**\n\n"
                f"🖼️ *(Fiche balistique officielle jointe ci-dessous)*"
            )
        else:
            spoken = f"With {f_name}, it takes {t_head} headshot(s) or {t_body} body shot(s) to eliminate a {target_name}."
            display = (
                f"🎯 **FIREARM HTK SIMULATOR : {f_name.upper()} vs {target_name.upper()}**\n\n"
                f"• 🔫 **Weapon :** **{f_name}** ({f_info['rarity']} {f_info['type']}) — Damage : **{int(f_dmg)}** (Headshot : **{int(f_head)}**)\n"
                f"• 🎯 **Target :** **{target_name}**\n"
                f"• 💥 **Headshots :** **{t_head} shot(s)**\n"
                f"• 🛡️ **Body Shots :** **{t_body} shot(s)**\n\n"
                f"🖼️ *(Authentic firearm card attached below)*"
            )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 3. Check Melee Weapons (Mace, Club, Longsword, Zweihander, Spear, Rapier, Axe, etc.)
    w_slug = None
    w_name = None

    if any(w in cleaned for w in ["club", "gourdin", "massue"]):
        w_slug, w_name = "club", "Club"
    elif any(w in cleaned for w in ["shortsword", "short-sword", "short sword", "epee courte", "épée courte"]):
        w_slug, w_name = "short-sword", "Short Sword"
    elif any(w in cleaned for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
    elif any(w in cleaned for w in ["hallebarde", "halberd"]):
        w_slug, w_name = "halberd", "Halberd"
    elif any(w in cleaned for w in ["sabre", "saber"]):
        w_slug, w_name = "sabre", "Sabre"
    elif any(w in cleaned for w in ["rapier", "rapiere", "rapière"]):
        w_slug, w_name = "rapier", "Rapier"
    elif any(w in cleaned for w in ["war-axe", "war axe", "hache de guerre"]):
        w_slug, w_name = "war-axe", "War Axe"
    elif any(w in cleaned for w in ["axe", "hache"]):
        w_slug, w_name = "axe", "Axe"
    elif any(w in cleaned for w in ["mace", "masse"]):
        w_slug, w_name = "mace", "Mace"
    elif any(w in cleaned for w in ["dagger", "dague"]):
        w_slug, w_name = "dagger", "Dagger"
    elif any(w in cleaned for w in ["pricker", "perce-armure"]):
        w_slug, w_name = "pricker", "Pricker"
    elif any(w in cleaned for w in ["spear", "lance"]):
        w_slug, w_name = "spear", "Spear"
    elif any(w in cleaned for w in ["longsword", "epee batarde", "épée bâtarde", "epee", "épée"]):
        w_slug, w_name = "longsword", "Longsword"

    if not w_slug:
        w_slug = "longsword"
        w_name = "Longsword"

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM weapons WHERE slug = ?", (w_slug,))
    w_row = c.fetchone()
    conn.close()

    if not w_row:
        w = {"light_damage": 38.0, "heavy_damage": 49.0, "thrust_damage": 38.0, "rarity_en": "Uncommon"}
    else:
        w = dict(w_row)

    l_dmg = float(w.get("light_damage", 38.0))
    h_dmg = float(w.get("heavy_damage", 49.0))
    rarity = w.get("rarity_en", "Uncommon")

    t_head = max(1, int(math.ceil(target_hp / (h_dmg * 1.5))))
    t_body_light = max(1, int(math.ceil(target_hp / l_dmg)))
    t_body_heavy = max(1, int(math.ceil(target_hp / h_dmg)))

    card_path = render_pure_english_melee_card(w_slug)

    spoken = f"With {w_name}, it takes {t_head} headshot(s) or {t_body_light} body hit(s) to eliminate a {target_name}."
    display = (
        f"⚔️ **COMBAT SIMULATOR & HTK : {w_name.upper()} vs {target_name.upper()}**\n\n"
        f"• 🗡️ **Weapon :** **{w_name}** ({rarity})\n"
        f"• 🎯 **Target :** **{target_name}**\n"
        f"• 💥 **Headshots (Crit x1.5) :** **{t_head} strike(s)**\n"
        f"• 🛡️ **Body Hits :** **{t_body_light} light hit(s)** (or **{t_body_heavy} heavy strike(s)**)\n"
        f"• ⚡ **Tactical Advice :** Prioritize heavy overheads to stagger and finish with rapid light strikes.\n\n"
        f"🖼️ *(Authentic Hunger Companion weapon dossier attached below)*"
    )
    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}


def answer_squad_item_needs_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answers which active or future quests require a specific loot item, and whether to safe-pouch it."""
    lowered = query.lower()
    is_needs_query = any(w in lowered for w in [
        "qui a besoin", "qui cherche", "qui demande", "who needs", "who wants", "besoin de", "besoin d",
        "est-ce que j'ai besoin", "est ce que jai besoin", "est ce que j'ai besoin",
        "a besoin de", "a besoin d", "dois-je garder", "dois je garder",
        "je dois garder", "utile pour", "je garde ou je jette", "garder ou jeter",
        "faut il garder", "faut-il garder", "do i need", "should i keep"
    ])
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "peasant", "bacchus", "loup", "basilisk", "solstice"]):
        return None
    if not is_needs_query:
        return None

    # 1. Try Player-specific / Squad DB Quest Sync check
    from co_pilot.quest_sync import check_player_item_need
    import re
    # Check if a user name is mentioned
    player_match = re.search(r"(?:est-ce que|est ce que|qui)\s+([a-zA-Z0-9_-]+)\s+a besoin", lowered)
    target_player = player_match.group(1) if player_match else "Abdallah"

    # Extract target item word
    it_cand = None
    for item_k in ["farine", "flour", "bezoar", "bague", "ring", "salpetre", "salpêtre", "saltpetre", "charbon", "charcoal", "pouch", "moist"]:
        if item_k in lowered:
            it_cand = item_k
            break
    
    if it_cand:
        sync_res = check_player_item_need(target_player, it_cand)
        if sync_res.get("needed"):
            spoken = f"Oui ! {sync_res['message']}" if is_french else f"Yes! {sync_res['message']}"
            display = (
                f"📜 **SYNCHRONISATION DES QUÊTES DE L'ESCOUADE :**\n\n"
                f"{sync_res['message']}\n\n"
                f"🔒 **Consigne :** Gardez cet item dans votre besace sécurisée ou stockez-le dans votre coffre de Stash !"
            )
            return {"spoken_text": spoken, "display_text": display}

    # Detect item
    item_detected = "farine"
    item_en = "flour"
    giver = "Éloïse (Château Hub)"
    quest_name = "Making Dough"
    quantity = "20x Sacs de Farine"
    importance = "CRITIQUE (Débloque le pain et les rations au Château)"
    location_hint = "Trouvable en abondance au Moulin de Sarlat Farm (sacs de farine et caisses du meunier, taux 47.6%)."

    if any(w in lowered for w in ["family ring", "bague", "anneau de famille"]):
        item_detected, item_en = "anneau de famille (family ring)", "family-ring"
        giver = "Louis"
        quest_name = "The Last Prisoner"
        quantity = "1 Anneau de Famille"
        importance = "QUÊTE HISTOIRE UNIQUE (Indispensable pour valider The Last Prisoner)"
        location_hint = "Défini pour les armoires et conteneurs résidentiels de Jacques Bridge et Sarlat Farm."
    elif any(w in lowered for w in ["salpêtre", "salpetre", "saltpetre"]):
        item_detected, item_en = "salpêtre", "saltpetre"
        giver = "Le Forgeron Paul"
        quest_name = "Poudre Noire & Défense"
        quantity = "4 poudres de salpêtre"
        importance = "ÉLEVÉE (Nécessaire pour forger munitions et bombes)"
        location_hint = "Se récolte dans les caches de terre noire du Camp des Bûcherons sur Sombre Forêt."
    elif any(w in lowered for w in ["charbon", "charcoal"]):
        item_detected, item_en = "charbon", "charcoal"
        giver = "L'Armurier Jean"
        quest_name = "La Forge du Pont"
        quantity = "6 morceaux de charbon"
        importance = "MOYENNE (Nécessaire pour tremper l'acier des armures)"
        location_hint = "Piles de charbon et braseros autour de la Garnison du Pont Jacques."
    elif any(w in lowered for w in ["champignon", "fungus", "champignons"]):
        item_detected, item_en = "champignon", "fungus"
        giver = "L'Alchimiste Marie"
        quest_name = "Élixirs de Vigueur"
        quantity = "8 champignons sombres"
        importance = "ÉLEVÉE (Permet de brasser des antidotes contre le poison)"
        location_hint = "Pousse sur les troncs moussus et près des ruisseaux de Sombre Forêt."
    elif any(w in lowered for w in ["os", "bone", "bones"]):
        item_detected, item_en = "os", "bone"
        giver = "L'Arbalétrier"
        quest_name = "Pointe de Flèche"
        quantity = "10 fragments d'os"
        importance = "MOYENNE (Artisanat de carreaux et pointes d'armes)"
        location_hint = "Squelettes et autels sacrificiels de Sombre Forêt et catacombes."
    elif any(w in lowered for w in ["folly", "clef de jacques", "clé de jacques", "jacques folly key"]):
        item_detected, item_en = "clé de la folie de jacques", "jacques folly key"
        giver = "Capitaine Claude"
        quest_name = "Sous les Voûtes de Jacques"
        quantity = "1 Clé de la folie"
        importance = "LÉGENDAIRE (Ouvre la crypte et le coffre scellé du donjon)"
        location_hint = "Spawn rare (1/133) sur les bureaux du Pont Jacques ou butin (1/226) sur les Brutes/Baveux."
    elif any(w in lowered for w in ["clé", "clef", "key"]):
        item_detected, item_en = "clé de donjon", "dungeon key"
        giver = "Explorateurs du Château"
        quest_name = "Exploration Souterraine"
        quantity = "1 Clé"
        importance = "LÉGENDAIRE (Ouvre les salles scellées du Puits ou du Sous-sol)"
        location_hint = "À placer OBLIGATOIREMENT dans votre besace sécurisée dès ramassage !"

    if is_french:
        spoken = f"OUI, gardez {item_detected} ! Requis par {giver} pour la quête {quest_name}. À mettre en priorité dans votre besace !"
        display = (
            f"🎒 **ANALYSE DE BESACE & QUÊTES : {item_detected.upper()}**\n\n"
            f"• ✅ **Verdict :** **À GARDER ABSOLUMENT DANS LA BESACE SÉCURISÉE !**\n"
            f"• 📜 **Quête Associée :** **{quest_name}**\n"
            f"• 👤 **Commanditaire :** **{giver}** au Château\n"
            f"• 📦 **Quantité Requise :** **{quantity}**\n"
            f"• ⚡ **Priorité :** **{importance}**\n"
            f"• 📍 **Emplacement :** {location_hint}\n\n"
            f"💡 *Conseil de survie : En cas de mort, seuls les objets placés dans votre besace sécurisée retournent au Château avec vous.*"
        )
    else:
        spoken = f"YES, keep {item_en}! Required by {giver} for quest {quest_name}. Safe pouch priority!"
        display = (
            f"🎒 **SAFE POUCH & QUEST PRIORITY : {item_en.upper()}**\n\n"
            f"• ✅ **Verdict :** **KEEP IN SAFE POUCH!**\n"
            f"• 📜 **Quest :** **{quest_name}** ({giver})\n"
            f"• 📦 **Required :** **{quantity}**\n"
            f"• 📍 **Location :** {location_hint}"
        )
    card_img = None
    try:
        from co_pilot.card_renderer import render_item_card
        card_img = render_item_card(item_en)
    except Exception:
        pass
    res_dict = {"spoken_text": spoken, "display_text": display}
    if card_img:
        res_dict["image_attachment"] = card_img
    return res_dict


# ---------------------------------------------------------------------------
# 13. IN-RAID LOOTING & SAFE POUCH ADVICE ("quoi mettre dans ma besace")
# ---------------------------------------------------------------------------

def answer_safe_pouch_priority_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Gives top loot priority rules for safe pouch vs backpack."""
    lowered = query.lower()
    is_pouch_ask = any(w in lowered for w in [
        "besace", "besace sécurisée", "poche sécurisée", "safe pouch", "quoi prioriser",
        "priorité loot", "que garder dans ma besace", "quoi mettre dans ma besace", "ordre de priorité"
    ])
    if not is_pouch_ask:
        return None

    if is_french:
        spoken = "Priorité absolue dans la besace : d'abord les clés de donjon, puis les objets de quête uniques comme l'anneau de Gavroche, puis le salpêtre."
        display = (
            f"🔒 **ORDRE DE PRIORITÉ POUR LA BESACE SÉCURISÉE :**\n\n"
            f"1. 🔑 **Priorité 1 (Absolue) : Clés de Donjon**\n"
            f"   • *Clé de Jacques Folly, Clé du Puits, Clé de Bronze* (Inestimables, indispensables pour les donjons).\n\n"
            f"2. 📜 **Priorité 2 (Critique) : Objets de Quête Uniques**\n"
            f"   • *Family Ring (Gavroche), Reliques sacrées* (Taux de spawn limité, introuvables chez les marchands).\n\n"
            f"3. 🧪 **Priorité 3 (Élevée) : Matériaux Non-Achetables**\n"
            f"   • *Salpêtre (Saltpetre), Sève alchimique, Lingots d'argent* (Artisanat de haut niveau).\n\n"
            f"4. 📦 **Priorité 4 (Dans le Sac classique) : Ravitaillement Courant**\n"
            f"   • *Farine, Charbon, Os, Baumes* (Peuvent être rachetés au Château auprès de Denis ou Paul)."
        )
    else:
        spoken = "Safe pouch priority: 1. Dungeon keys, 2. Unique quest items like Family Ring, 3. Saltpetre, 4. Crafting supplies."
        display = (
            f"🔒 **SAFE POUCH LOOT PRIORITY :**\n\n"
            f"1. 🔑 **Top 1 : Dungeon Keys** (Jacques Folly, Sarlat Pit Keys)\n"
            f"2. 📜 **Top 2 : Unique Quest Items** (Family Ring, Relics)\n"
            f"3. 🧪 **Top 3 : Unbuyable Crafting** (Saltpetre, Silver)\n"
            f"4. 📦 **Backpack : Common Supplies** (Flour, Charcoal - buyable at Chateau)"
        )
    return {"spoken_text": spoken, "display_text": display}


# ---------------------------------------------------------------------------
# 14. PRECISE MAP & QUEST LOCATION ENGINE ("où se trouve X", "where is X")
# ---------------------------------------------------------------------------

def answer_location_query(query: str, is_french: bool) -> Optional[Dict[str, Any]]:
    """
    Delivers exact tactical locations and coordinates with map overlays for any quest,
    campsite, landmark, dungeon entrance, or resource on the maps.
    """
    lowered = query.lower()
    is_loc_ask = any(w in lowered for w in [
        "ou se trouve", "où se trouve", "ou trouver", "où trouver", "ou est", "où est",
        "ou sont", "où sont", "trouve ou", "trouver ou", "trouve où", "trouver où",
        "localisation", "emplacement", "position de", "position du", "where is", "where are",
        "where to find", "how to find", "location of"
    ])
    if not is_loc_ask:
        return None

    # Cosmetic skins and blueprints are handled by the dedicated skin crafting engine!
    if any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "outfit", "apparence", "peasant burden", "bacchus", "loup", "basilisk", "solstice"]):
        return None

    # Gathering nodes are handled by the dedicated gathering engine!
    if any(w in lowered for w in [
        "garlic", "lavender", "clove", "rosemary", "cinnamon", "yarrow", "fungi", "saffron",
        "poppy", "peppercorn", "twine", "screws", "gunpowder", "striker", "lever arm", "lodestone",
        "whale oil", "quicksilver", "burlap", "lead ore", "copper ore", "linen", "cotton", "iron ore",
        "silver ore", "gold ore", "silk"
    ]):
        return None

    from co_pilot.map_generator import generate_location_poi_map, generate_dungeon_tactical_map, generate_item_farm_map

    # 1. The Gavroche Family Camp & Quest Location
    if any(w in lowered for w in ["gavroche", "family gavroche", "famille gavroche", "camp gavroche", "the gavroche family"]):
        img_path, intel = generate_location_poi_map("gavroche", "Jacques Bridge")
        if is_french:
            spoken = (
                "Le camp de la famille Gavroche se trouve sur Pont Jacques, près des berges Est au niveau des ruines. "
                "Carte tactique transmise avec le repère exact."
            )
            display = (
                "📍 **LOCALISATION EXACTE : CAMP DE LA FAMILLE GAVROCHE (PONT JACQUES)**\n\n"
                "• 🗺️ **Carte Tactique :** **Jacques Bridge (Pont Jacques)**\n"
                "• 📌 **Emplacement :** Ruines du campement sur les berges Est (`X: 1479.01, Y: 313.35`)\n"
                "• 📜 **Quête Associée :** **The Gavroche Family** (Commanditaire : Éloïse au Château)\n"
                "• 🎯 **Objectif :** *Locate the Gavroche Family Camp.* (Préréquis : avoir terminé *Making Dough*)\n"
                "• 🎁 **Récompense :** 3 Pommes Cuites (Stewed Apples)\n"
                "• 💡 **À savoir :** Si vous cherchez l'**Anneau de Famille (Family Ring)** pour la quête *The Last Prisoner*, "
                "il se fouille dans les armoires et tiroirs des habitations sur cette carte.\n\n"
                "🖼️ *Carte tactique haute résolution générée ci-dessous avec le point de repère exact.*"
            )
        else:
            spoken = "The Gavroche Family Camp is located on Jacques Bridge along the East riverbanks. Tactical map dispatched."
            display = (
                "📍 **EXACT LOCATION : GAVROCHE FAMILY CAMP (JACQUES BRIDGE)**\n\n"
                "• 🗺️ **Map :** **Jacques Bridge**\n"
                "• 📌 **Coordinates :** `X: 1479.01, Y: 313.35` (East riverbank ruins)\n"
                "• 📜 **Quest :** **The Gavroche Family** (Giver: Eloise at Chateau)"
            )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

    # 2. Subterranean Dungeons (Jacques Folly, The Pit, The Undercroft)
    if any(w in lowered for w in ["folly", "jacques folly", "donjon de jacques", "puits", "pit", "undercroft", "crypte", "sous-sol", "sous sol"]):
        img_path, intel = generate_dungeon_tactical_map(lowered)
        target_name = intel.get("title", "Donjon")
        if is_french:
            spoken = f"Les entrées du donjon {target_name} sont indiquées sur la carte tactique transmise."
            display = f"🏰 **ACCÈS ET ENTRÉES : {target_name.upper()}**\n\n🎯 **Points d'accès :**\n" + "\n".join(intel.get("drops", []))
        else:
            spoken = f"Dungeon entrances for {target_name} marked on the map dispatched."
            display = f"🏰 **DUNGEON ENTRANCES : {target_name.upper()}**"
        return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        # 2.5 Item Location & Raid Drops (e.g. "ou est ce que je peux trouver heavy ammo")
    if any(w in lowered for w in ["ammo", "munition", "munitions", "flour", "farine", "charcoal", "charbon", "saltpetre", "salpetre", "bezoar", "chiffon", "balm", "baume"]):
        from co_pilot.companion_intel import get_companion_item_intel
        from co_pilot.card_renderer import render_item_card
        
        cand_slug = "heavy-ammunition" if any(w in lowered for w in ["heavy ammo", "munitions lourdes", "heavy ammunition"]) else "flour" if "farine" in lowered or "flour" in lowered else "charcoal" if "charbon" in lowered or "charcoal" in lowered else "saltpetre"
        intel = get_companion_item_intel(cand_slug)
        if intel:
            card_p = render_item_card(intel["name_en"], rarity=intel.get("rarity", "Common"),
                                      sell_silver=intel.get("sell_silver", 0), sell_copper=intel.get("sell_copper", 2),
                                      item_type=intel.get("category", "Ammunition"), desc=intel.get("lore_desc", "Essential raid ammunition."),
                                      best_source=intel.get("best_container", "Munitions Crate (1/108)"), drop_rate="High",
                                      buy_vendor=intel.get("vendor_buy", "Voyant the Rifleman, Piro, Reynauld (0s 2c)"))
            spoken = f"{intel['name_en']} can be purchased at Chateau Hub from Voyant the Rifleman, Piro, and Reynauld, or scavenged from Munitions Crates in raid."
            display = (
                f"📦 **LOOT & VENDOR LOCATIONS : {intel['name_en'].upper()}**\n\n"
                f"• 🏰 **Château Hub Traders :** Available from **{intel.get('vendor_buy', 'Voyant the Rifleman, Piro, Reynauld')}** (0 Silver, 2 Copper).\n"
                f"• 📦 **Best Raid Containers :** **{intel.get('best_container', 'Munitions Crate (1/108)')}** on Sarlat Farm, Jacques Bridge, and Sombre Forest.\n"
                f"• 👾 **Creature Drop :** Scavenged from Brutes (1/52 drop rate).\n\n"
                f"*(Authentic Hunger Companion item card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

    # 3. Dynamic POI Search in Database (map_points & Piro's Convoy)
    img_path, intel = generate_location_poi_map(query)
    title = intel.get("title", "Tactical Waypoint")
    m_name = intel.get("map_name", "Jacques Bridge")
    drops_txt = "\n".join(intel.get("drops", []))
    spoken = f"Location for {title} on {m_name} marked on map."
    display = f"📍 **LOCATION : {title.upper()} ({m_name.upper()})**\n\n{drops_txt}"
    return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}
