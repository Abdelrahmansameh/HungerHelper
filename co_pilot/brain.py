import perfect_briefings_core_v25 as core
import re
import os
import sys
import time
import sqlite3
from typing import Dict, Any, Optional, Tuple, List

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

from co_pilot.knowledge_db import search_items, search_quests, search_talents, search_npcs, get_connection
from co_pilot.profile_store import (
    get_or_create_profile,
    set_quest_status,
    allocate_talent_points,
    update_user_level,
    get_user_progression_summary,
    get_needed_quest_items
)
from co_pilot.map_generator import (
    generate_speedrun_raid_map,
    generate_creatures_map,
    generate_dungeon_folly_map,
    generate_dungeon_tactical_map,
    generate_item_farm_map,
    render_dynamic_v25_briefing,
    resolve_map_image
)
from co_pilot.card_renderer import (
    render_item_card,
    render_weapon_card,
    render_quest_card,
    render_character_card,
    render_creature_card,
    render_dungeon_card,
    render_skin_card,
    render_talent_build_card,
    CREATURES_DATA
)
from co_pilot.game_knowledge import (
    get_learned_terms,
    save_learned_term,
    add_custom_farm_item,
    get_custom_farm_items,
    answer_weapon_query,
    answer_effect_query,
    answer_dungeon_key_query,
    answer_merchant_query,
    answer_random_fact_query,
    answer_best_containers_query,
    answer_extraction_query,
    answer_talent_advice_query,
    answer_combat_ttk_query,
    answer_squad_item_needs_query,
    answer_safe_pouch_priority_query,
    answer_location_query,
    get_or_render_items_to_keep
)

FRENCH_GAME_TRANSLATIONS = {
    "miel": "honey",
    "salpetre": "saltpetre",
    "salpêtre": "saltpetre",
    "champignon": "fungus",
    "champignons": "fungus",
    "os": "bone",
    "charbon": "charcoal",
    "farine": "flour",
    "pain": "bread",
    "eau": "water",
    "ferme": "farm",
    "foret": "forest",
    "forêt": "forest",
    "sombre": "sombre",
    "pont": "bridge",
    "lance": "spear",
    "dague": "dagger",
    "baveux": "drooler",
    "rebut": "dreg",
    "boursoufle": "bloat",
    "boursouflé": "bloat"
}

def extract_key_search_terms(text: str) -> List[str]:
    """Clean natural language stopwords to extract search entity candidates."""
    stop_phrases = [
        "what is", "what are", "what do", "tell me about", "where is", "where can i find",
        "how do i get", "how do i find", "how to complete", "how do i complete", "who is",
        "who sells", "who are", "c'est quoi", "c quoi", "que represente", "que représente", "qu'est ce que",
        "quest ce que", "parle moi de", "où se trouve", "ou se trouve", "où trouver", "ou trouver",
        "qui est", "qui sont", "qui vend", "comment obtenir", "comment faire", "the", "a", "an", "de",
        "du", "des", "la", "le", "les", "sur", "on", "in", "at", "about", "for", "pour",
        "tu as mis", "you put", "shown on", "qui", "sont", "est", "c'est", "c est", "un", "une", "ce", "ces", "cet",
        "show me every", "show me all", "show me", "give me", "every", "tous les", "toutes les",
        "montre moi tout", "montre moi tous", "montre moi toute", "montre moi", "donne moi",
        "2 hand", "1 hand", "two hand", "one hand", "2-hand", "1-hand", "2 mains", "1 main", "deux mains", "une main",
        "armes a", "arme a", "melee", "weapons", "weapon", "armes", "arme"
    ]
    cleaned = text.lower()
    for sp in stop_phrases:
        cleaned = re.sub(r"\b" + re.escape(sp) + r"\b", " ", cleaned)
    
    for fr, en in FRENCH_GAME_TRANSLATIONS.items():
        cleaned = re.sub(r"\b" + re.escape(fr) + r"\b", en, cleaned)

    cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
    banned_tokens = {"hand", "hands", "main", "mains", "melee", "weapon", "weapons", "arme", "armes", "every", "all", "show", "give", "item", "items"}
    tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1 and t.strip().lower() not in banned_tokens]
    
    candidates = []
    full_phrase = " ".join(tokens)
    if full_phrase:
        candidates.append(full_phrase)
    for t in tokens:
        if len(t) >= 3 and t not in candidates and t not in banned_tokens:
            candidates.append(t)
    return candidates


class CoPilotBrain:
    def __init__(self):
        # Contextual conversation memory
        self.last_map_info: Dict[str, Any] = {}
        self.map_context_by_user: Dict[str, Dict[str, Any]] = {}
        self.last_active_quest: Optional[str] = None
        self.last_queried_item: Optional[str] = None
        
        # Two-step confirmation verbal learning state
        self.pending_term: Optional[str] = None
        self.pending_term_time: float = 0.0
        self.pending_confirmation: Optional[Tuple[str, str]] = None

        # Live Raid Mission Timer State
        self.raid_active: bool = False
        self.raid_start_time: float = 0.0
        self.raid_map_name: str = "Sarlat Farm"
        self.raid_duration: float = 20 * 60.0  # 20 minutes default extraction raid timer

    def process_message(self, user_id: str, username: str, text: str) -> Dict[str, Any]:
        """
        Main cognitive loop for Eloise.
        Strictly responds in French or English matching user input language.
        Keeps verbal speech ultra-concise while delivering rich visual cards & text to Discord.
        """
        clean_text = text.strip()
        normalized = re.sub(r"[?!.,;]+$", "", clean_text).strip()
        lowered = normalized.lower()

        # Language Detection: Default to ENGLISH! French ONLY when explicitly asked!
        is_french = any(w in lowered for w in ["en français", "en francais", "in french", "traduis en français", "traduis en francais", "réponds en français", "reponds en francais"])

        # -------------------------------------------------------------------
        # 0. FORGET / RESET COMMANDS ("oublie", "recommence", "laisse tomber", "annule")
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["oublie", "oublie ça", "oublie ca", "recommence", "laisse tomber", "annule", "forget", "forget it", "nevermind", "cancel"]):
            self.pending_term = None
            self.pending_term_time = 0.0
            self.pending_confirmation = None
            self.map_context_by_user.pop(user_id, None)
            self.last_map_info = {}
            spoken = "Entendu, j'oublie et on repart de zéro. De quoi avez-vous besoin ?" if is_french else "Understood, forgotten. Starting fresh. What do you need, Commander?"
            display = "🔄 **Demande Annulée & Mémoire Réinitialisée :** Éloïse est prête pour votre prochaine demande."
            return {"spoken_text": spoken, "display_text": display}

        # Explicit maps take precedence over broad item, creature and dungeon keywords.
        from co_pilot.map_requests import handle_map_request
        map_result = handle_map_request(clean_text, self.map_context_by_user.get(user_id))
        if map_result is not None:
            self.pending_term = None
            self.pending_confirmation = None
            response, context = map_result
            if context is not None:
                self.map_context_by_user[user_id] = context
                self.last_map_info = context
            return response

        # -------------------------------------------------------------------
        # 0.1 TWO-STEP CONFIRMATION FOR LEARNED TERMS
        # -------------------------------------------------------------------
        if self.pending_confirmation:
            p_term, p_meaning = self.pending_confirmation
            self.pending_confirmation = None
            if any(w in lowered for w in ["confirmer", "confirme", "oui", "valide", "d'accord", "yes", "confirm", "ok"]):
                save_learned_term(p_term, p_meaning, username)
                spoken = f"C'est confirmé, j'ai enregistré que '{p_term}' signifie '{p_meaning}'." if is_french else f"Confirmed, recorded that '{p_term}' means '{p_meaning}'."
                display = f"🧠 **Terme Appris & Enregistré :**\n• **'{p_term}'** = *\"{p_meaning}\"*"
                return {"spoken_text": spoken, "display_text": display}
            else:
                # If user did not confirm, discard and proceed
                pass

        # If user starts a new question, clear pending term immediately
        is_new_question = any(clean_text.lower().startswith(w) for w in [
            "c'est quoi", "c quoi", "qu'est ce que", "quest ce que", "ou ", "ou est", "combien",
            "montre", "quel", "quelle", "quels", "quelles", "carte", "stats", "degat", "degats",
            "who", "where", "what", "how", "show", "give", "tell"
        ])
        if is_new_question:
            self.pending_term = None
            self.pending_confirmation = None

        # If user was explaining a term after Eloise asked (within 25s window):
        if self.pending_term and (time.time() - self.pending_term_time < 25.0):
            cand_term = self.pending_term
            self.pending_term = None
            self.pending_confirmation = (cand_term, clean_text)
            if is_french:
                spoken = f"Voulez-vous que j'associe '{cand_term}' à '{clean_text}' ? Dites 'confirmer' pour valider ou 'oublie' pour annuler."
                display = f"❓ **Confirmation d'Association Requise :**\n• Voulez-vous associer **'{cand_term}'** à **\"{clean_text}\"** ?\n🗣️ *Dites **'Confirmer'** ou **'Oublie'**.*"
            else:
                spoken = f"Do you want me to associate '{cand_term}' with '{clean_text}'? Say 'confirm' to save or 'forget' to cancel."
                display = f"❓ **Association Confirmation Required :**\n• Associate **'{cand_term}'** with **\"{clean_text}\"**?\n🗣️ *Say **'Confirm'** or **'Forget'**.*"
            return {"spoken_text": spoken, "display_text": display}
        else:
            self.pending_term = None

        # -------------------------------------------------------------------
        # 0.2 SILENCE / STOP COMMANDS ("stop", "arrête", "chut", "tais-toi")
        # -------------------------------------------------------------------
        is_silence_command = any(w in lowered for w in [
            "silence", "stop", "stoppe", "arrête", "arrete", "arrête-toi", "arrete-toi",
            "tais-toi", "tais toi", "chut", "shut up", "ferme-la", "ferme la", "pause", "annule"
        ])
        if is_silence_command:
            self.pending_term = None
            self.pending_term_time = 0.0
            self.pending_confirmation = None
            # Absolute silence: spoken_text must be empty so she never utters another syllable!
            display = "🤫 **Mode Silence Activé (Voix coupée)** *(Prête pour votre prochaine question dès que vous direz 'Éloïse')*"
            return {"spoken_text": "", "display_text": display}

        # -------------------------------------------------------------------
        # 0.3 SMALL TALK & COURTESY
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["merci", "thank you", "thanks", "thx"]) and len(clean_text.split()) <= 4:
            spoken = "À votre service, monsieur. Bonne chance pour votre raid !" if is_french else "Always at your service, Commander. Good luck on your raid!"
            display = "✨ **À votre service, Commandant.**"
            return {"spoken_text": spoken, "display_text": display}

        if any(w in lowered for w in ["comment vas-tu", "comment ca va", "comment tu vas", "how are you", "ca va", "ça va"]) and len(clean_text.split()) <= 4:
            spoken = "Tous les systèmes tactiques sont opérationnels. Prête pour votre prochain raid !" if is_french else "All tactical systems are operational. Ready for your next raid, Commander!"
            display = "🛡️ **Systèmes Tactiques Opérationnels**"
            return {"spoken_text": spoken, "display_text": display}

        # -------------------------------------------------------------------
        # 0.4 RAID MISSION TIMER & EXTRACTION TRACKER
        # -------------------------------------------------------------------
        is_raid_start = any(w in lowered for w in ["lance un raid", "lance le raid", "start raid", "commence le raid", "démarre le raid", "demarre le raid", "on part en raid", "part en raid"])
        if is_raid_start:
            target_map = "Sarlat Farm"
            if any(k in lowered for k in ["sombre", "forest", "forêt"]): target_map = "Sombre Forest"
            elif any(k in lowered for k in ["jacques", "pont", "bridge"]): target_map = "Jacques Bridge"

            self.raid_active = True
            self.raid_start_time = time.time()
            self.raid_map_name = target_map

            if is_french:
                spoken = f"Raid lancé sur {target_map} ! Chronomètre de déploiement activé. Je compte le temps écoulé depuis notre insertion."
                display = (
                    f"⏱️ **CHRONOMÈTRE DE RAID ACTIVÉ : {target_map.upper()}**\n\n"
                    f"• 🚀 **Insertion d'Escouade :** `00:00` (Chronomètre en marche)\n"
                    f"• 💡 **Rappel Serveur :** L'insertion se fait aléatoirement dans les 10 premières minutes de vie de la partie.\n"
                    f"• 🗣️ **Commandes :** Demandez *« Combien de temps est passé ? »* ou *« Temps de raid ? »* pour suivre votre temps d'engagement !\n"
                    f"• 🚪 **Extractions :** Rivière Nord & Sentier Sud (Se déverrouillent au fil du temps)."
                )
            else:
                spoken = f"Raid deployed on {target_map}! Elapsed deployment timer started."
                display = f"⏱️ **RAID TIMER ACTIVE : {target_map.upper()} (Elapsed Time Tracking)**"
            return {"spoken_text": spoken, "display_text": display}

        is_raid_time_check = any(w in lowered for w in [
            "combien de temps on est", "combien de temps est passé", "combien de temps est passer",
            "temps passé", "temps passe", "temps de raid", "temps du raid", "chrono", "chrono de raid",
            "combien de temps il reste", "combien de temps reste", "time left", "raid time", "how long in raid"
        ])
        if is_raid_time_check:
            if not self.raid_active:
                spoken = "Le chronomètre n'a pas encore été lancé. Dites 'lance un raid' dès votre déploiement sur la carte !" if is_french else "Raid timer not active. Say 'start raid' when deployed!"
                display = "⏱️ **Aucun raid actif** *(Dites 'lance un raid' pour commencer à mesurer votre temps de survie)*"
                return {"spoken_text": spoken, "display_text": display}

            elapsed = time.time() - self.raid_start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)

            if is_french:
                if elapsed < 300:
                    spoken = f"Vous êtes dans le raid depuis {mins} minutes et {secs} secondes. Phase initiale : fouillez les conteneurs et restez discrets."
                    tactics = "🟢 **Phase Initiale (< 5 min)** : Fouille tranquille des conteneurs prioritaires. Extractions calmes."
                elif elapsed < 600:
                    spoken = f"Vous êtes dans le raid depuis {mins} minutes et {secs} secondes. Les élites patrouillent et les portes d'extraction s'ouvrent."
                    tactics = "🟡 **Phase Médiane (5-10 min)** : Patrouilles de Brutes actives. Les portes d'extraction commencent à s'activer."
                else:
                    spoken = f"Vous êtes déployés depuis {mins} minutes et {secs} secondes. Phase avancée : forte probabilité d'affrontements d'escouades vers les sorties. Pensez à extraire."
                    tactics = "🔴 **Phase Avancée (+10 min)** : Risque élevé de rencontres PvP aux abords des extractions. Repli conseillé !"

                display = (
                    f"⏱️ **CHRONOMÈTRE DE DÉPLOIEMENT : {self.raid_map_name.upper()}**\n\n"
                    f"• ⏳ **Temps Écoulé depuis l'Insertion :** **{mins:02d}:{secs:02d}**\n"
                    f"• 🛡️ **Statut Tactique :** {tactics}\n"
                    f"• 🚪 **Extractions :** Rivière Nord & Sentier Boisé Sud"
                )
            else:
                spoken = f"You have been in the raid for {mins} minutes and {secs} seconds on {self.raid_map_name}."
                display = f"⏱️ **ELAPSED RAID TIME : {mins:02d}:{secs:02d} ({self.raid_map_name.upper()})**"
            return {"spoken_text": spoken, "display_text": display}

        is_raid_end = any(w in lowered for w in ["raid terminé", "on a extrait", "extraction réussie", "raid fini", "fin du raid", "extracted"])
        if is_raid_end and self.raid_active:
            self.raid_active = False
            elapsed_m = int((time.time() - self.raid_start_time) // 60)
            elapsed_s = int((time.time() - self.raid_start_time) % 60)
            spoken = f"Extraction confirmée après {elapsed_m} minutes et {elapsed_s} secondes de raid ! Félicitations escouade. Débriefing prêt au Château." if is_french else "Extraction confirmed! Great raid, squad."
            display = f"🏆 **EXTRACTION RÉUSSIE : {self.raid_map_name.upper()}**\n• ⏱️ Durée totale de l'opération : **{elapsed_m}m {elapsed_s}s**\n• 🏰 **Retour au Château :** Vous pouvez rendre vos quêtes auprès des marchands !"
            return {"spoken_text": spoken, "display_text": display}

        # -------------------------------------------------------------------

        # -------------------------------------------------------------------
        # 0.40 PIRO'S LENS VS PIRO'S CONVOY ROUTER (ABSOLUTE PRIORITY)
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["lens", "lentille", "piro's lens", "piros lens", "seeing clearly"]):
            from co_pilot.map_generator import generate_location_poi_map
            img_path, intel = generate_location_poi_map("piro's lens")
            card_p = render_item_card("Piro's Lens", rarity="Uncommon", item_type="Quest Item", is_french=is_french)
            spoken = "Piro's Lens is located in the subterranean Rat's Nest Cave at Jacques Bridge South-East ruins."
            display = (
                "🔍 **QUEST ITEM LOCATION : PIRO'S LENS (QUEST: SEEING CLEARLY)**\n\n"
                "• 📍 **Cave Entrance :** `X: 1602.00, Y: 3552.00` (Subterranean Rat's Nest Cave).\n"
                "• 🎯 **Exact Item Coordinates :** `X: 1491.15, Y: 3535.74` (on the ground inside).\n"
                "• 📜 **Quest Giver :** Piro (The Leper Physician at Chateau Hub) — Quest *Seeing Clearly*.\n"
                "• 🔒 **Security Protocol :** Keep in **Secure Pouch** (Non-droppable quest item).\n\n"
                "*(Authentic tactical cave map & item card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [img_path, card_p], "image_attachment": img_path}

        elif any(w in lowered for w in ["convoy", "convoi", "remains of the day", "return to the convoy"]) or ("piro" in lowered and any(w in lowered for w in ["ruine", "ruins", "charette", "wagon", "site", "quete", "quête"])):
            from co_pilot.map_generator import generate_location_poi_map
            img_path, intel = generate_location_poi_map("piro's convoy")
            spoken = "Piro's Convoy ruins are situated on the Jacques Bridge southwest riverbank road."
            display = (
                "📍 **QUEST LOCATION : PIRO'S CONVOY RUINS (JACQUES BRIDGE)**\n\n"
                "• 📍 **Wagon Coordinates :** `X: 848.20, Y: 3084.90` (Southwest Riverbank Road).\n"
                "• 📜 **Quests :** *Remains of the Day* & *Return to the Convoy*.\n"
                "• 🎁 **Objective :** Retrieve Crude Ampoules from the overturned supply cart.\n\n"
                "*(Tactical convoy recon map attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        # -------------------------------------------------------------------
        # 0.42 FARMER DREG (ELITE DREG VARIANT SPAWN & RECON)
        # -------------------------------------------------------------------
        is_farmer_dreg = any(w in lowered for w in ["farmer dreg", "dreg farmer", "dreg fermier", "fermier dreg"])
        if is_farmer_dreg:
            from co_pilot.map_generator import generate_farmer_dreg_spawn_map
            img_path, intel = generate_farmer_dreg_spawn_map()
            if is_french:
                spoken = "Le Dreg Fermier est un variant élite apparaissant à la Ferme Garnier sur Sarlat Farm (taux 1 raid sur 20). Il lâche à 100% le schéma de la lance Fardeau du Paysan. Carte tactique transmise."
                display = (
                    "📍 **RECONNAISSANCE TACTIQUE : SPAWN DU DREG FERMIER (SARLAT FARM)**\n\n"
                    "• 👾 **Identité de la Créature :** **Dreg Fermier** (*Farmer Dreg*, Variant Élite de Rebut)\n"
                    "• 🗺️ **Emplacement Principal :** **Ferme Garnier** (Centre de Sarlat Farm · `X: 2313, Y: 1517`)\n"
                    "• 🎲 **Taux d'Apparition :** **1 raid sur 20** (~5% de chance par partie)\n"
                    "• 🎁 **Loot Garanti à 100% :**\n"
                    "  - 💎 **Fardeau du Paysan - Lance** (Schéma cosmétique · **100% TOUJOURS**)\n"
                    "  - 💀 **Tête de Dreg** (Trophée Rebut)\n"
                    "• ⚔️ **Conseil Tactique :** Équipé d'une fourche de paysan. Frappez d'estoc ou avec des attaques lourdes pour le chanceler avant qu'il n'enchaîne ses coups rapides.\n\n"
                    "🖼️ *(Carte tactique haute résolution générée ci-dessous)*"
                )
            else:
                spoken = "Farmer Dreg is an elite Dreg variant spawning at Garnier's Farm on Sarlat Farm with a 1 in 20 raid chance. He always drops the Peasant's Burden Spear schema. Tactical spawn map dispatched."
                display = (
                    "📍 **TACTICAL RECON : FARMER DREG SPAWN (SARLAT FARM)**\n\n"
                    "• 👾 **Creature Identity :** **Farmer Dreg** (*Dreg Farmer*, Elite Variant of Dreg)\n"
                    "• 🗺️ **Primary Spawn Location :** **Garnier's Farm** (Central Sarlat Farm · `X: 2313, Y: 1517`)\n"
                    "• 🎲 **Spawn Chance :** **1 in 20 raids** (~5% raid encounter rate)\n"
                    "• 🎁 **Guaranteed 100% Drop :**\n"
                    "  - 💎 **Peasant's Burden - Spear** (Cosmetic Schema · **100% ALWAYS**)\n"
                    "  - 💀 **Dreg Head** (Uncommon Trophy)\n"
                    "• ⚔️ **Tactical Advice :** Armed with a rusty farming pitchfork. Stagger with heavy overhead strikes or firearms from range before he closes the distance.\n\n"
                    "🖼️ *(High-resolution tactical spawn map generated below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        # -------------------------------------------------------------------
        # 0.45 MAP & TACTICAL NAVIGATION ROUTER
        # Handles pure blank base maps & dungeon layouts
        # -------------------------------------------------------------------
        is_dungeon = any(w in lowered for w in ["dungeon", "donjon", "folly", "pit", "puits", "entree", "entrée", "entrées", "entrances"])
        is_exact_map_name = lowered.strip() in [
            "sarlat", "sarlat farm", "ferme de sarlat",
            "sombre", "sombre forest", "foret sombre", "forêt sombre",
            "jacques", "jacques bridge", "pont jacques",
            "chateau", "le chateau", "le château", "the chateau"
        ]
        is_pure_map_query = (
            any(w in lowered for w in ["map", "carte", "plan"]) and
            not any(w in lowered for w in [
                "poi", "point", "trouver", "drop", "coffre", "container", "clef", "clé", "key",
                "creature", "créature", "baveux", "brute", "drooler", "farm", "route", "speedrun",
                "guide", "tactique", "stratégie", "strat", "skin", "arme", "weapon", "degat"
            ])
        ) or any(w in lowered for w in ["carte sans indication", "map sans indication", "blank map", "pure map", "carte de base"]) or is_exact_map_name

        if is_dungeon and re.search(r"\bfolly\b", lowered):
            from universal_v8_engine import render_authentic_dungeon_card
            img_path = render_authentic_dungeon_card(is_french=is_french)
            spoken = "Jacques Folly subterranean dungeon map dispatched with authentic entrance coordinates."
            display = (
                "🏰 **DUNGEON ACCESS : JACQUES FOLLY (AUTHENTIC NORTHERN RIDGE SITES)**\n\n"
                "• 📍 **Authentic Location :** Northwest of Vairon Quarry on northern wooded ridge.\n"
                "• 🚪 **Official Entrance Coordinates (Jacques Bridge - Raid 2) :**\n"
                "  1. **Jacques Folly Main Descent** (X: 1680.4, Y: 197.1)\n"
                "  2. **The Last Prisoner Crypt** (X: 1530.5, Y: 315.4)\n"
                "• 🔑 **Required Key :** Jacques Folly Key (3 Uses)\n"
                "• 📦 **Loot Capacity :** 174 reinforced subterranean containers.\n\n"
                "🖼️ *(Authentic clean map inset attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        elif is_pure_map_query:
            from universal_v8_engine import get_pure_blank_map
            is_jb = any(w in lowered for w in ["jaque", "jaques", "jacques", "jb", "pont jacques", "jacques bridge"])
            is_sf = any(w in lowered for w in ["sarlat", "sf", "ferme de sarlat", "sarlat farm", "moulin"])
            is_sombre = any(w in lowered for w in ["sombre", "forest", "foret", "forêt", "sombre forest"])

            if is_sombre or "sombre" in lowered:
                p_map = get_pure_blank_map("sombre")
                spoken = "Official blank vintage Sombre Forest map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SOMBRE FOREST (AUTHENTIC BLANK BASE MAP)**\n\n"
                    "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\n\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
            elif is_sf or "sarlat" in lowered:
                p_map = get_pure_blank_map("sarlat")
                spoken = "Official blank vintage Sarlat Farm map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SARLAT FARM (AUTHENTIC BLANK BASE MAP)**\n\n"
                    "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\n\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
            elif is_jb or "jacques" in lowered or "jaque" in lowered or "jb" in lowered:
                p_map = get_pure_blank_map("jacques")
                spoken = "Official blank vintage Jacques Bridge map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : JACQUES BRIDGE (AUTHENTIC BLANK BASE MAP)**\n\n"
                    "• 📍 **Zone :** Fortified bridge, garrison ruins & East riverbank.\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\n\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
        
        # 0.5 COMBAT TTK & HIT CALCULATOR ("combien de coups pour tuer X")
        # -------------------------------------------------------------------
        ttk_res = answer_combat_ttk_query(clean_text, is_french)
        if ttk_res:
            return ttk_res

        # -------------------------------------------------------------------
        # 0.6 PRECISE LOCATION / OÙ SE TROUVE QUERY ("ou se trouve family gavroche")
        # -------------------------------------------------------------------
        loc_res = answer_location_query(clean_text, is_french)
        if loc_res:
            if "jacques" in clean_text.lower() or "gavroche" in clean_text.lower():
                self.last_map_info["map_name"] = "Jacques Bridge"
            elif any(k in clean_text.lower() for k in ["sombre", "forest", "forêt"]):
                self.last_map_info["map_name"] = "Sombre Forest"
            return loc_res

        # -------------------------------------------------------------------
        # 0.7 SQUAD ITEM & QUEST NEEDS CHECKER ("qui a besoin de farine", "est-ce que j'ai besoin de")
        # -------------------------------------------------------------------
        squad_res = answer_squad_item_needs_query(clean_text, is_french)
        if squad_res:
            return squad_res

        # -------------------------------------------------------------------
        # 0.8 SAFE POUCH LOOT PRIORITY ("quoi mettre dans ma besace")
        # -------------------------------------------------------------------
        pouch_res = answer_safe_pouch_priority_query(clean_text, is_french)
        if pouch_res:
            return pouch_res

        # Expand any previously verified learned terms in query
        learned_dict = get_learned_terms()
        for lt, meaning in learned_dict.items():
            if lt in lowered:
                lowered = lowered.replace(lt, f"{lt} ({meaning})")

        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        # 1. CHARACTER KITS & ABILITIES ("ult de marie", "passif de marie", "sort d'eva", "fiche de marie")
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = [
            "ult", "ultime", "ultimate", "passif", "passive", "tactical", "tactique",
            "capacité", "capacite", "capacités", "capacites", "ability", "abilities",
            "skill", "skills", "personnage", "survivor", "hero", "héros", "heros",
            "classe", "sort", "sorts", "pouvoir", "pouvoirs", "competence", "compétence",
            "compétences", "profil", "profile", "fiche", "kit", "stats", "stat"
        ]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and (any(w in lowered for w in hero_keywords) or len(clean_text.split()) <= 4):
            from universal_v8_engine import render_clean_character_card
            card_path = render_clean_character_card(matched_hero, is_french=is_french)
            
            HERO_KITS = {
                "marie": {
                    "name": "Marie", "title": "Warrior Nun / Apothecary",
                    "passive": ("Alchemical Pouch (Besace d'Alchimiste)", "Can carry 2 additional medicine vials in secure belt without risk of loot drop."),
                    "tactical": ("Healing Salve (Baume Curatif) [Q]", "Restores 75 HP over 6 seconds and immediately stops hemorrhaging bleed."),
                    "ultimate": ("Acid Flask (Fiole d'Acide) [E / ULT]", "Shatters enemy armor durability by 40% and deals heavy corrosive acid splash damage.")
                },
                "eva": {
                    "name": "Eva", "title": "Vagabond Huntress",
                    "passive": ("Lightfoot (Pied Léger)", "Footstep audio reduced by 35% and crouch movement speed increased by 25%."),
                    "tactical": ("Caltrops (Chausse-trappes) [Q]", "Scatters spiked caltrops slowing enemy movement by 60% and causing light bleed."),
                    "ultimate": ("Flashbang (Grenade Aveuglante) [E / ULT]", "Blinds and disorients all targets within 8 meters for 4 seconds.")
                },
                "hugo": {
                    "name": "Hugo", "title": "The Maniac",
                    "passive": ("Thick Skin (Cuir Épais)", "Passively absorbs 15% physical impact damage and shortens stun recovery."),
                    "tactical": ("Fortify (Fortification) [Q]", "Deploys a temporary personal barrier absorbing 120 damage."),
                    "ultimate": ("War Cry (Cri de Guerre) [E / ULT]", "Increases squad melee attack speed by 20% and stagger poise for 8 seconds.")
                },
                "otto": {
                    "name": "Otto", "title": "Sergeant-at-Arms",
                    "passive": ("Armor Smith (Maître Armurier)", "Equipped armor durability depletes 30% slower during raid combat."),
                    "tactical": ("Siegebreaker (Brise-Siège) [Q]", "Heavy shoulder charge knocking down foes and instantly breaking wooden doors."),
                    "ultimate": ("Iron Will (Volonté de Fer) [E / ULT]", "Grants immunity to stagger, knockback, and bleed for 10 seconds.")
                },
                "gabriel": {
                    "name": "Gabriel", "title": "Soldier of Fortune",
                    "passive": ("Line Infantry (Ligne d'Infanterie)", "Gain +15% damage resistance and stamina efficiency near allies."),
                    "tactical": ("Bayonet Charge (Charge à la Baïonnette) [Q]", "High-velocity forward sprint thrust dealing high penetration and heavy stagger."),
                    "ultimate": ("Sadist's Surge (Ferveur Sadique) [E / ULT]", "Downing an opponent instantly restores 35 HP and refreshes stamina pool.")
                },
                "serine": {
                    "name": "Serine", "title": "Vodou Poisoner",
                    "passive": ("Vodou Spirit (Esprit Vaudou)", "Total immunity to environmental and creature poisons; regenerates in toxic pools."),
                    "tactical": ("Corrosive Rush (Ruée Corrosive) [Q]", "Rapid evasive dash leaving a toxic wake blurring enemy vision."),
                    "ultimate": ("Vodou Bomb (Bombe Vaudou) [E / ULT]", "Heavy noxious explosive dealing massive area corrosion and lingering poison.")
                }
            }

            kit = HERO_KITS.get(matched_hero, HERO_KITS["marie"])
            
            # Check specific ability query
            is_ult = any(w in lowered for w in ["ult", "ultime", "ultimate", "special", "spécial", "touche e", "sort e"])
            is_pass = any(w in lowered for w in ["passif", "passive"])
            is_tact = any(w in lowered for w in ["tactique", "tactical", "touche q", "sort q", "sort", "premier sort"])

            if is_ult:
                ab_name, ab_desc = kit["ultimate"]
                spoken = f"{kit['name']}'s Ultimate ability is {ab_name}: {ab_desc}"
                display = (
                    f"⚡ **SPECIAL / ULTIMATE ABILITY : {kit['name'].upper()}**\n\n"
                    f"• 💥 **Ability :** **{ab_name}**\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\n\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_pass:
                ab_name, ab_desc = kit["passive"]
                spoken = f"{kit['name']}'s Passive ability is {ab_name}: {ab_desc}"
                display = (
                    f"🛡️ **PASSIVE ABILITY : {kit['name'].upper()}**\n\n"
                    f"• 🛡️ **Ability :** **{ab_name}**\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\n\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_tact:
                ab_name, ab_desc = kit["tactical"]
                spoken = f"{kit['name']}'s Tactical ability is {ab_name}: {ab_desc}"
                display = (
                    f"✨ **TACTICAL ABILITY : {kit['name'].upper()}**\n\n"
                    f"• 🗡️ **Ability :** **{ab_name}**\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\n\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            else:
                spoken = f"Tactical operative profile for {kit['name']} dispatched."
                display = (
                    f"⚔️ **OFFICIAL HERO PROFILE : {kit['name'].upper()} ({kit['title'].upper()})**\n\n"
                    f"• 🛡️ **Passive :** **{kit['passive'][0]}** — {kit['passive'][1]}\n"
                    f"• 🗡️ **Tactical [Q] :** **{kit['tactical'][0]}** — {kit['tactical'][1]}\n"
                    f"• 💥 **Special / Ult [E] :** **{kit['ultimate'][0]}** — {kit['ultimate'][1]}\n\n"
                    f"*(Full abilities kit & unlocked prestige skins attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # 1.05 RECIPES & SCHEMAS (UNIVERSAL FOR ALL 110 CRAFTING RECIPES)
        # -------------------------------------------------------------------
        is_recipe_query = any(w in lowered for w in ["recipe", "recette"]) or (
            any(w in lowered for w in ["metallurgist", "gunsmith", "outfitter", "artificer", "physician", "cook"]) and
            any(w in lowered for w in ["spear", "brioche", "armour", "plate", "carry", "helmet", "pack", "cuirass", "potion", "salve", "craft"])
        )
        if is_recipe_query:
            from universal_v8_engine import get_universal_recipe
            rec_res = get_universal_recipe(clean_text)
            if rec_res and rec_res["found"]:
                spoken = f"Crafting recipe dossier for {clean_text} dispatched. Placed loot and vendor intel attached."
                display = f"📜 **{rec_res['title']}**\n\n{rec_res['text']}\n\n*(Official recipe card attached below)*"
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": [rec_res["card"]],
                    "image_attachment": rec_res["card"]
                }

        # 1.1 SKINS & COSMETICS (UNIVERSAL FOR ALL WEAPONS & CHARACTERS)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft", "craft quel"]) or any(w in lowered for w in [
            "peasant burden", "peasant's burden", "bacchus wand", "recluse", "partisan", "hybernia", "loup", "basilisk", "solstice"
        ])
        if is_skin_query:
            from universal_v8_engine import get_universal_skins
            skin_res = get_universal_skins(clean_text)
            
            if skin_res["found"]:
                spoken = f"Cosmetic skins for {clean_text} dispatched."
                display = f"🎨 **{skin_res['title']}**\n\n{skin_res['text']}\n\n*(Visual crafting cards attached below)*"
                cards = skin_res["cards"]
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": cards,
                    "image_attachment": cards[0] if cards else None
                }
            else:
                # Direct, clear message when weapon has no skins (e.g. Rapier, Shortsword)
                spoken = f"No craftable skins currently exist for this weapon in Hunger."
                display = f"🎨 **{skin_res['title']}**\n\n{skin_res['text']}"
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": [],
                    "image_attachment": None
                }

        # -------------------------------------------------------------------
        # 1.2 STASH & INVENTORY ANALYSIS (TWO IMAGES: Highlighted Grid + Sell Manifest)
        # -------------------------------------------------------------------
        is_stash_query = any(w in lowered for w in ["stash", "réserve", "reserve", "mon coffre", "inventaire"]) and any(w in lowered for w in ["analyse", "vendre", "rapport", "combien", "valeur", "trier", "estimer", "garder"])
        if is_stash_query:
            from universal_v8_engine import render_universal_stash_analysis
            p1, p2 = render_universal_stash_analysis(is_french=is_french)
            spoken = "Stash analysis complete: letters and sealed documents are strictly preserved for late-game character EXP. Two visual appraisal cards dispatched."
            display = (
                "📦 **STASH & INVENTORY TACTICAL APPRAISAL**\n\n"
                "• 🔒 **STRICT EXP RULE :** All letters, sealed documents, and books are **PRESERVED** for major late-game XP progression!\n"
                "• 🛡️ **Gear Preserved :** All meds, armors, bags, ammo, and tools kept.\n"
                "• 🛒 **Recommended to Sell :** Superfluous curios, church ornaments, duplicate orphan keys.\n"
                "• 💰 **Estimated Net Proceeds :** `2 Silver 5 Copper`\n\n"
                "*(Two visual cards attached: 1. Modified screenshot with sell items highlighted in gold | 2. Clean liquidation manifest)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [p1, p2], "image_attachment": p1}

        # -------------------------------------------------------------------
        # 1.21 BAGS & CAPACITY (ALL 29 BAGS - CAPACITY, SLOTS & RESALE VALUES)
        # e.g. "combien de slots a coldstream pack", "ludwig's drumcase", "moist pouch"
        # -------------------------------------------------------------------
        conn_b = sqlite3.connect("hunger_helper.db")
        c_b = conn_b.cursor()
        c_b.execute("SELECT slug, name, rarity, slots, sell_silver, sell_copper FROM bags_full")
        all_bags = c_b.fetchall()
        conn_b.close()

        matched_bag = None
        for b_slug, b_name, b_rar, b_slots, b_ss, b_sc in all_bags:
            b_name_clean = b_name.lower().replace("'", "").replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("'", "").replace("-", " ")
            if (re.search(r'\b' + re.escape(b_slug) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(b_name.lower()) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(b_name_clean) + r'\b', clean_q_spaced) or
                (b_slug.replace("-", " ") in clean_q_spaced and len(b_slug) > 5)):
                # If asking about recipe or craft, let recipe handler take it
                if any(w in lowered for w in ["recette", "recipe", "craft quel skin", "sert a craft"]):
                    continue
                matched_bag = (b_slug, b_name, b_rar, b_slots, b_ss, b_sc)
                break

        if matched_bag:
            b_slug, b_name, b_rar, b_slots, b_ss, b_sc = matched_bag
            self.last_queried_item = b_name
            from universal_v8_engine import render_bag_card
            card_path = render_bag_card(b_slug)
            val_txt = f"{b_ss} silver {b_sc} copper" if b_ss > 0 else f"{b_sc} copper"
            val_txt_fr = f"{b_ss} argent {b_sc} cuivre" if b_ss > 0 else f"{b_sc} cuivre"
            if is_french:
                spoken = f"Le {b_name} ({b_rar}) possède {b_slots} emplacements d'inventaire et se revend {val_txt_fr} aux marchands du Château."
                display = (
                    f"🎒 **FICHE DE BESACE : {b_name.upper()}**\n\n"
                    f"• Rareté : **{b_rar}**\n"
                    f"• Capacité : **{b_slots} Emplacements d'inventaire**\n"
                    f"• Prix de Revente : **{val_txt_fr}** (aux marchands)\n"
                    f"• Règle de Sécurité : Besace standard (perdable à la mort). Placez les clés et items vitaux dans la besace sécurisée !\n\n"
                    f"🖼️ *(Fiche de besace haute résolution jointe ci-dessous)*"
                )
            else:
                spoken = f"{b_name} ({b_rar}) provides {b_slots} inventory slots and sells for {val_txt} to Chateau vendors."
                display = (
                    f"🎒 **OFFICIAL BAG DOSSIER : {b_name.upper()}**\n\n"
                    f"• Rarity : **{b_rar}**\n"
                    f"• Capacity : **{b_slots} Inventory Slots**\n"
                    f"• Resale Value : **{val_txt}** (To Merchants)\n"
                    f"• Loss Rules : Standard Backpack (Droppable on death). Place vital keys and quest tokens in your Safe Pouch!\n\n"
                    f"🖼️ *(High-resolution bag card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.22 TRAPS & FIELD HAZARDS (ALL 12 TRAPS)
        # e.g. "explosive trap", "piege explosif", "poison trap", "broken glass"
        # -------------------------------------------------------------------
        conn_t = sqlite3.connect("hunger_helper.db")
        c_t = conn_t.cursor()
        c_t.execute("SELECT slug, name, damage, radius, spots FROM traps_full")
        all_traps = c_t.fetchall()
        conn_t.close()

        matched_trap = None
        for t_slug, t_name, t_dmg, t_rad, t_spots in all_traps:
            t_name_clean = t_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\b' + re.escape(t_slug) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(t_name.lower()) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(t_name_clean) + r'\b', clean_q_spaced)):
                if "strap" in clean_q_spaced and "trap" not in clean_q_spaced:
                    continue
                matched_trap = (t_slug, t_name, t_dmg, t_rad, t_spots)
                break

        if matched_trap:
            t_slug, t_name, t_dmg, t_rad, t_spots = matched_trap
            from universal_v8_engine import render_trap_hazard_card
            card_path = render_trap_hazard_card(t_slug)
            dmg_str = f"deals {t_dmg} damage" if t_dmg != "N/A" else "acts as an environmental hazard"
            dmg_str_fr = f"inflige {t_dmg} dégâts" if t_dmg != "N/A" else "agit comme piège d'alerte environnemental"
            rad_str = f"with a {t_rad} radius" if t_rad != "N/A" else ""
            rad_str_fr = f"avec un rayon de {t_rad}" if t_rad != "N/A" else ""
            if is_french:
                spoken = f"{t_name} {dmg_str_fr} {rad_str_fr} sur {t_spots} emplacements de raid."
                display = (
                    f"💥 **DOSSIER PIÈGE & DANGER : {t_name.upper()}**\n\n"
                    f"• Dégâts : **{t_dmg} DMG**\n"
                    f"• Rayon d'Activation : **{t_rad}**\n"
                    f"• Fréquence Mondiale : **{t_spots} Emplacements répertoriés**\n"
                    f"• Conseil Tactique : Déclenchez à distance avec des armes à feu ou cailloux pour éviter les dégâts d'escouade.\n\n"
                    f"🖼️ *(Fiche tactique de piège jointe ci-dessous)*"
                )
            else:
                spoken = f"{t_name} {dmg_str} {rad_str} across {t_spots} world locations."
                display = (
                    f"💥 **HAZARD DOSSIER : {t_name.upper()}**\n\n"
                    f"• Base Damage : **{t_dmg} DMG**\n"
                    f"• Blast Radius : **{t_rad}**\n"
                    f"• World Locations : **{t_spots} Map Spots**\n"
                    f"• Tactical Protocol : Trigger remotely with ranged fire or throwables to secure chokepoints.\n\n"
                    f"🖼️ *(Hazard intel card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.23 STATUS EFFECTS & COMBAT CONDITIONS (ALL 36 EFFECTS)
        # e.g. "c'est quoi light bleed", "heavy poison", "status effect blind"
        # -------------------------------------------------------------------
        conn_e = sqlite3.connect("hunger_helper.db")
        c_e = conn_e.cursor()
        c_e.execute("SELECT slug, name, category, effect_type FROM status_effects_full")
        all_effects = c_e.fetchall()
        conn_e.close()

        matched_eff = None
        for e_slug, e_name, e_cat, e_type in all_effects:
            e_name_clean = e_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\b' + re.escape(e_slug) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(e_name.lower()) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(e_name_clean) + r'\b', clean_q_spaced)):
                matched_eff = (e_slug, e_name, e_cat, e_type)
                break

        if matched_eff:
            e_slug, e_name, e_cat, e_type = matched_eff
            from universal_v8_engine import render_status_effect_card
            card_path = render_status_effect_card(e_slug)
            if is_french:
                spoken = f"{e_name} est un effet de statut ({e_cat}). {e_type[:60]}."
                display = (
                    f"🩸 **EFFET DE STATUT : {e_name.upper()}**\n\n"
                    f"• Catégorie : **{e_cat}**\n"
                    f"• Mécaniques : **{e_type}**\n"
                    f"• Traitement : Appliquez des bandages propres ou onguents de médecin immédiatement.\n\n"
                    f"🖼️ *(Fiche de statut jointe ci-dessous)*"
                )
            else:
                spoken = f"{e_name} is a {e_cat} condition. {e_type[:60]}."
                display = (
                    f"🩸 **STATUS EFFECT DOSSIER : {e_name.upper()}**\n\n"
                    f"• Classification : **{e_cat}**\n"
                    f"• Impact & Dynamics : **{e_type}**\n"
                    f"• Treatment : Apply Clean Bandage for Bleed or Physician Antivenom for Poison.\n\n"
                    f"🖼️ *(High-resolution status card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.24 GATHERING NODES & NATURAL RESOURCES (ALL 32 NODES)
        # e.g. "ou trouver garlic bulb", "cueillette lavender", "clove bud"
        # -------------------------------------------------------------------
        conn_g = sqlite3.connect("hunger_helper.db")
        c_g = conn_g.cursor()
        c_g.execute("SELECT slug, name, chance, yield_range FROM gathering_full")
        all_nodes = c_g.fetchall()
        conn_g.close()

        matched_node = None
        for g_slug, g_name, g_chance, g_yield in all_nodes:
            g_name_clean = g_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\b' + re.escape(g_slug) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(g_name.lower()) + r'\b', clean_text.lower()) or
                re.search(r'\b' + re.escape(g_name_clean) + r'\b', clean_q_spaced)):
                matched_node = (g_slug, g_name, g_chance, g_yield)
                break

        if matched_node:
            g_slug, g_name, g_chance, g_yield = matched_node
            from universal_v8_engine import render_gathering_card
            card_path = render_gathering_card(g_slug)
            if is_french:
                spoken = f"{g_name} a un taux de récolte de {g_chance} et donne {g_yield} unités par plante. Récoltable principalement à Sarlat Farm et Sombre Forest."
                display = (
                    f"🌿 **RESSOURCE & CUEILLETTE : {g_name.upper()}**\n\n"
                    f"• Chance de Récolte : **{g_chance}**\n"
                    f"• Rendement par Récolte : **{g_yield} Unités**\n"
                    f"• Zones Principales : **Sarlat Farm, Garnier's Fields, Sombre Forest**\n"
                    f"• Métiers : Ingrédient indispensable pour les recettes de Cuisinier et Apothicaire.\n\n"
                    f"🖼️ *(Fiche de cueillette jointe ci-dessous)*"
                )
            else:
                spoken = f"{g_name} has a {g_chance} harvest chance yielding {g_yield} units per node. Plentiful at Sarlat Farm."
                display = (
                    f"🌿 **GATHERING RECON : {g_name.upper()}**\n\n"
                    f"• Harvest Rate : **{g_chance} Success**\n"
                    f"• Yield Range : **{g_yield} Units Per Harvest**\n"
                    f"• Primary Habitats : **Sarlat Farm, Garnier's Fields, Sombre Forest**\n"
                    f"• Profession Utility : High-tier Cook provisions and Physician remedies.\n\n"
                    f"🖼️ *(Gathering reconnaissance card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.25 CONTAINERS & FIELD LOOT (ALL 67 CONTAINERS)
        # e.g. "munitions crate", "spots oak barrel", "armour chest"
        # -------------------------------------------------------------------
        conn_cnt = sqlite3.connect("hunger_helper.db")
        c_cnt = conn_cnt.cursor()
        c_cnt.execute("SELECT slug, name, spots, items_count FROM containers_full")
        all_containers = c_cnt.fetchall()
        conn_cnt.close()

        matched_cont = None
        for c_slug, c_name, c_spots, c_icnt in all_containers:
            c_name_clean = c_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if any(w in lowered for w in ["conteneur", "container", "caisse", "coffre", "baril", "spots"]):
                if (re.search(r'\b' + re.escape(c_slug) + r'\b', clean_text.lower()) or
                    re.search(r'\b' + re.escape(c_name.lower()) + r'\b', clean_text.lower()) or
                    re.search(r'\b' + re.escape(c_name_clean) + r'\b', clean_q_spaced)):
                    matched_cont = (c_slug, c_name, c_spots, c_icnt)
                    break
            elif len(c_name.split()) >= 2:
                if (re.search(r'\b' + re.escape(c_slug) + r'\b', clean_text.lower()) or
                    re.search(r'\b' + re.escape(c_name.lower()) + r'\b', clean_text.lower()) or
                    re.search(r'\b' + re.escape(c_name_clean) + r'\b', clean_q_spaced)):
                    matched_cont = (c_slug, c_name, c_spots, c_icnt)
                    break

        if matched_cont:
            c_slug, c_name, c_spots, c_icnt = matched_cont
            from universal_v8_engine import render_container_card
            card_path = render_container_card(c_slug)
            if is_french:
                spoken = f"{c_name} apparaît sur {c_spots} emplacements de raid et contient {c_icnt} types d'objets."
                display = (
                    f"📦 **CONTENEUR DE RAID : {c_name.upper()}**\n\n"
                    f"• Emplacements Mondiaux : **{c_spots} Spawns répertoriés**\n"
                    f"• Variété de Butin : **{c_icnt} Variétés d'objets**\n"
                    f"• Cartes Recommandées : Sarlat Farm, Jacques Bridge, Sombre Forest.\n\n"
                    f"🖼️ *(Fiche de conteneur jointe ci-dessous)*"
                )
            else:
                spoken = f"{c_name} appears in {c_spots} world spots containing {c_icnt} loot varieties."
                display = (
                    f"📦 **CONTAINER INTEL : {c_name.upper()}**\n\n"
                    f"• World Locations : **{c_spots} Spawn Points**\n"
                    f"• Loot Variety : **{c_icnt} Unique Item Types**\n"
                    f"• Best Maps : Sarlat Farm, Jacques Bridge, Sombre Forest.\n\n"
                    f"🖼️ *(Container reconnaissance card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 2. ITEM SELL PRICE & VALUE CARD (e.g. "combien se vend cet item", "combien coute le deux")
        # -------------------------------------------------------------------
        is_price_query = any(w in lowered for w in [
            "combien se vend", "prix de vente", "prix de revente", "valeur", "combien vaut",
            "combien coute", "combien coûte", "combien vaux", "prix du", "prix de", "quel est le prix",
            "sell price", "how much sells", "se vend", "how much is", "cost"
        ])
        if is_price_query:
            # 1. Check if asking about keys
            conn = get_connection()
            c = conn.cursor()
            
            # Check keys
            c.execute("SELECT * FROM keys_data")
            keys_rows = c.fetchall()
            matched_key = None
            for kr in keys_rows:
                if kr["slug"] in lowered or kr["name_en"].lower() in lowered or kr["name_fr"].lower() in lowered:
                    matched_key = kr
                    break
            if not matched_key and any(w in lowered for w in ["clef", "clé", "key"]):
                matched_key = keys_rows[0] if keys_rows else None

            if matched_key:
                conn.close()
                self.last_queried_item = matched_key["name_fr"] if is_french else matched_key["name_en"]
                card_path = render_item_card(
                    item_name=matched_key["name_fr"] if is_french else matched_key["name_en"],
                    rarity=matched_key["rarity"],
                    sell_silver=82 if "folly" in matched_key["slug"] else 25 if "gold" in matched_key["slug"] else 12,
                    sell_copper=12 if "folly" in matched_key["slug"] else 60,
                    item_type=f"Clé de donjon ({matched_key['uses']} usages)",
                    desc=f"Ouvre les portes verrouillées et coffres du Pont Jacques. Utilisations : {matched_key['uses']}.",
                    icon_name="flour.png",
                    best_source="Spawns du Pont Jacques (1/133) ou Baveux/Brutes (1/226)"
                )
                if is_french:
                    spoken = f"La {matched_key['name_fr']} se vend {matched_key['sell_price']}. Fiche visuelle transmise."
                    display = f"🔑 **VALEUR MARCHANDE : {matched_key['name_fr'].upper()}**\n• Revente : **{matched_key['sell_price']}**\n• Usages : **{matched_key['uses']}**\n*(Fiche d'inventaire jointe ci-dessous)*"
                else:
                    spoken = f"The {matched_key['name_en']} sells for {matched_key['sell_price']}. Card dispatched."
                    display = f"🔑 **MARKET VALUE : {matched_key['name_en'].upper()}**\n• Sell Price: **{matched_key['sell_price']}**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

            # 2. Check weapons
            matched_weapon = None
            for w_name in ["zweihander", "zwei", "deux mains", "deux-mains", "spear", "lance", "hallebarde", "halberd", "dagger", "dague", "sword", "épée", "axe", "hache", "mace", "masse"]:
                if w_name in lowered:
                    t_w = "zweihander" if w_name in ["zweihander", "zwei", "deux mains", "deux-mains"] else "spear" if w_name in ["spear", "lance"] else w_name
                    c.execute("SELECT * FROM weapons WHERE slug = ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1", (t_w, f"%{t_w}%", f"%{t_w}%"))
                    matched_weapon = c.fetchone()
                    if matched_weapon:
                        break

            if matched_weapon:
                conn.close()
                w_row = matched_weapon
                self.last_queried_item = w_row["name_fr"] if is_french else w_row["name_en"]
                raw_price = w_row["sell_price"] or "0 0"
                parts = raw_price.strip().split()
                s_silver, s_copper = (int(parts[0]), int(parts[1])) if len(parts) >= 2 else (3, 80)
                card_path = render_weapon_card(w_row["slug"], is_french)
                if is_french:
                    spoken = f"La {w_row['name_fr']} {w_row['rarity_fr']} se vend {s_silver} argent {s_copper} cuivre. Fiche transmise."
                    display = f"💰 **VALEUR MARCHANDE : {w_row['name_fr'].upper()}**\n• Revente : **{s_silver} Argent {s_copper} Cuivre**\n• Dégâts : **{w_row['thrust_damage']} Estoc | {w_row['heavy_damage']} Attaque Lourde**\n*(Fiche d'arme Hunger Companion jointe ci-dessous)*"
                    if "deux" in lowered:
                        display += "\n\n💡 *Note : Si vous parliez du pistolet « Deux » (arme à feu rare), il s'achète auprès de Voyant le Fusilier au Château.*"
                else:
                    spoken = f"The {w_row['name_en']} sells for {s_silver} silver {s_copper} copper. Weapon card dispatched."
                    display = f"💰 **MARKET VALUE : {w_row['name_en'].upper()}**\n• Sell Price: **{s_silver} Silver {s_copper} Copper**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

            # 3. Check live Hunger Companion intel first
            conn.close()
            from co_pilot.companion_intel import get_companion_item_intel, normalize_query_to_slug
            comp_slug = normalize_query_to_slug(clean_text)
            comp_intel = get_companion_item_intel(comp_slug)
            if comp_intel:
                self.last_queried_item = comp_intel["name_en"]
                card_path = render_item_card(comp_intel["slug"])
                s_s = comp_intel["sell_silver"]
                s_c = comp_intel["sell_copper"]
                if is_french:
                    v_str = f" Achat disponible chez {comp_intel['vendor_buy']}." if comp_intel.get("vendor_buy") else ""
                    spoken = f"Le {comp_intel['name_en']} ({comp_intel['rarity']}) se vend {s_s} argent {s_c} cuivre.{v_str} Fiche transmise."
                    display = (
                        f"💰 **FICHE OFFICIELLE : {comp_intel['name_en'].upper()}**\n\n"
                        f"• Rareté : **{comp_intel['rarity']}** | Catégorie : **{comp_intel['category']}**\n"
                        f"• Valeur de Revente : **{s_s} Argent {s_c} Cuivre**\n"
                        f"• Achat Château : **{comp_intel.get('vendor_buy') or 'Loot exclusif en raid'}**\n"
                        f"• Butin & Conteneurs : **{comp_intel.get('best_container') or 'Conteneurs de raid'}**\n"
                        f"• Description In-Game : *« {comp_intel.get('lore_desc', '')[:100]} »*\n\n"
                        f"🖼️ *Fiche visuelle Hunger Companion jointe ci-dessous.*"
                    )
                else:
                    v_str = f" Available from {comp_intel['vendor_buy']}." if comp_intel.get("vendor_buy") else ""
                    spoken = f"The {comp_intel['name_en']} ({comp_intel['rarity']}) sells for {s_s} silver {s_c} copper.{v_str} Card dispatched."
                    display = (
                        f"💰 **OFFICIAL ITEM PROFILE : {comp_intel['name_en'].upper()}**\n\n"
                        f"• Rarity : **{comp_intel['rarity']}** | Category : **{comp_intel['category']}**\n"
                        f"• Resale Value : **{s_s} Silver {s_c} Copper** (To Vendors)\n"
                        f"• Chateau Availability : **{comp_intel.get('vendor_buy') or 'Not sold by merchants (Raid Loot Exclusive)'}**\n"
                        f"• Best Drop Source : **{comp_intel.get('best_container') or 'Expedition Loot Containers'}**\n"
                        f"• Lore : *« {comp_intel.get('lore_desc', '')[:120]} »*\n\n"
                        f"🖼️ *(High-resolution Hunger Companion item card attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

            conn = get_connection()
            c = conn.cursor()
            cand_items = extract_key_search_terms(clean_text)
            matched_item = None
            for cand in cand_items:
                c.execute("SELECT * FROM items WHERE slug = ? OR name LIKE ? LIMIT 1", (cand, f"%{cand}%"))
                it_row = c.fetchone()
                if it_row:
                    matched_item = it_row
                    break
            conn.close()

            if matched_item:
                self.last_queried_item = matched_item["name"]
                card_path = render_item_card(matched_item["name"])
                if is_french:
                    spoken = f"{matched_item['name']} ({matched_item['rarity']}). Fiche détaillée transmise."
                    display = (
                        f"💰 **VALEUR & BUTIN : {matched_item['name'].upper()}**\n\n"
                        f"• Catégorie : **{matched_item['type'].title()}** | Rareté : **{matched_item['rarity'].title()}**\n"
                        f"• Règle de Besace : Placez en priorité dans la besace sécurisée si requis pour vos quêtes.\n\n"
                        f"🖼️ *Fiche visuelle d'inventaire jointe ci-dessous.*"
                    )
                else:
                    spoken = f"{matched_item['name']} item card dispatched."
                    display = f"💰 **ITEM VALUE : {matched_item['name'].upper()}**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 3. EXPLAIN MAP POINTS (Highest conversational priority)
        # e.g. "c'est quoi les points que tu as mis sur", "que representent les points"
        # -------------------------------------------------------------------
        point_words = [
            "point", "points", "rond", "ronds", "dot", "dots", "marker", "markers",
            "repère", "repere", "repères", "reperes", "badge", "badges", "icône", "icone", "icônes", "icones"
        ]
        ask_words = [
            "c'est quoi", "c quoi", "que represente", "que représente", "qu'est ce que", "quest ce que",
            "what are", "what is", "what do", "explain", "expliquer", "explique", "signifie", "signifient",
            "veut dire", "veulent dire", "pourquoi", "indique", "indiquent", "sert", "servent", "mean", "meaning"
        ]
        has_point_ask = (
            any(pw in lowered for pw in point_words) and 
            (any(aw in lowered for aw in ask_words) or 
             "tu as mis" in lowered or "you put" in lowered or 
             "sur la map" in lowered or "sur la carte" in lowered or "on the map" in lowered)
        )
        # Also catch standalone queries like "les points sur sarlat", "les ronds de la map"
        if not has_point_ask and any(pw in lowered for pw in ["les points", "les ronds", "le point", "le rond", "the points", "the dots"]) and any(w in lowered for w in ["sarlat", "sombre", "jacques", "folly", "carte", "map"]):
            has_point_ask = True

        if has_point_ask:
            context = self.map_context_by_user.get(user_id)
            description = context.get("points_description") if context else None
            message = description or "No map has been generated for you yet. Which map and objective do you mean?"
            return {"spoken_text": message, "display_text": message}

        # -------------------------------------------------------------------
        # 4. CUSTOM KEEP / FARM ITEMS LIST (ADD ITEM)
        # -------------------------------------------------------------------
        if ("ajoute" in lowered or "add" in lowered) and any(w in lowered for w in ["garder", "farm", "liste", "keep"]):
            m_item = re.search(r"(?:ajoute|add)\s+(?:l'|le\s+|la\s+|les\s+|the\s+)?(.+?)(?:\s+(?:à|a|to)\s+ma\s+liste|\s+pour\s+(.+)|$)", lowered)
            item_candidate = m_item.group(1).strip() if m_item else "item"
            reason = m_item.group(2).strip() if m_item and m_item.group(2) else "Farm cosmétique / personnel"
            add_custom_farm_item(user_id, item_candidate, reason)
            
            if is_french:
                spoken = f"C'est noté ! '{item_candidate}' est ajouté à votre liste d'items à garder."
                display = f"🎒 **Item Ajouté à la Liste :**\n• **Item :** {item_candidate.title()}\n• **Raison :** {reason}\n*(Inclus dans vos briefings de raid personnalisés)*"
            else:
                spoken = f"Noted! Added '{item_candidate}' to your keep list."
                display = f"🎒 **Item Added to Keep List :**\n• **Item :** {item_candidate.title()}\n• **Reason :** {reason}"
            return {"spoken_text": spoken, "display_text": display}

        # -------------------------------------------------------------------
        # 5. ITEMS TO KEEP INFOGRAPHIC IMAGE GUIDE
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["item que je dois garder", "items que je dois garder", "objets à garder", "items to keep", "ce que je dois garder", "image de tout les item", "image des items"]):
            img_path, spoken, display = get_or_render_items_to_keep(user_id, is_french)
            # Ultra concise verbal
            spoken = "Guide visuel des 27 items à garder transmis sur Discord." if is_french else "Visual guide of items to keep dispatched to Discord."
            return {
                "spoken_text": spoken,
                "display_text": display,
                "image_attachment": img_path
            }

        # -------------------------------------------------------------------
                # 4.9 QUEST CHAINING / NEXT QUEST IN PROGRESSION ("quel quete viens apres...")
        if any(w in lowered for w in ["apres celle de", "après celle de", "qui vient après", "qui viens après", "apres", "après", "after"]) and any(w in lowered for w in ["sweet", "opium", "pipe", "bowl", "china", "bribery"]):
            from universal_v8_engine import render_dynamic_quest_contract_card
            card_p = render_dynamic_quest_contract_card("down-from-mount-sinai")
            spoken = "The quest following Mr Sweet's 'A Touch of Bribery' is 'Down From Mount Sinai' given by Eloise at Chateau."
            display = (
                "📜 **QUEST PROGRESSION : NEXT CONTRACT (HUNGER COMPANION)**\n\n"
                "• ⬅️ **Completed Prerequisite :** **A Touch of Bribery** (Mr Sweet · Gather 1x Opium, 1x Opium Pipe, 1x China Bowl)\n"
                "• ➡️ **Next Unlocked Quest :** **Down From Mount Sinai** (Giver: Eloise at Chateau Hub)\n"
                "• 🎯 **Mission Objectives :** Recover the 7 lost treatises and historical records:\n"
                "  1. *Catechisme of Christian Doctrine (1567)*\n"
                "  2. *Census of 1806*\n"
                "  3. *The Spirit of the Laws (Montesquieu)*\n"
                "  4. *Course in Agriculture (Rozier)*\n"
                "  5. *Codex Medicamentarius (Mortuary Record)*\n"
                "  6. *Course in Civil Architecture (Rondelet)*\n"
                "  7. *Natural History (Buffon)*\n"
                "• 🗺️ **Raid Maps :** Search book cabinets across Jacques Bridge, Sarlat Farm, and Sombre Forest.\n\n"
                "*(Authentic mission contract card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

        # 5.0 QUEST INTEL CARD ("quête the gavroche family", "quête making dough")
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["quête", "quete", "quest"]) and not any(w in lowered for w in ["prochaine", "mes quête", "mes quete", "fini", "terminé", "complete"]):
            matched_q_list = search_quests(clean_text, limit=1)
            if matched_q_list:
                mq = matched_q_list[0]
                q_card = render_quest_card(mq["slug"], is_french)
                if is_french:
                    spoken = f"Fiche de la quête {mq['name']} transmise avec la checklist des objectifs et les récompenses complètes."
                    display = (
                        f"📜 **FICHE TECHNIQUE DE MISSION : {mq['name'].upper()}**\n\n"
                        f"• 👤 **Commanditaire :** **{mq['giver']}** (Château)\n"
                        f"• 🗺️ **Carte :** **{mq['location']}**\n"
                        f"• 🎯 **Objectif :** *{mq.get('objectives', [{'description': 'Objectif de quête'}])[0]['description']}*\n"
                        f"• 🎁 **Récompense :** **{mq.get('reward_quantity', 1)}x {mq.get('reward_item', 'Butin')}**\n\n"
                        f"🖼️ *Fiche visuelle détaillée (Hunger Companion) jointe ci-dessous.*"
                    )
                else:
                    spoken = f"Quest card for {mq['name']} dispatched."
                    display = f"📜 **QUEST PROFILE : {mq['name'].upper()}**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": q_card}

        # -------------------------------------------------------------------
        # 5.1 QUEST PROGRESSION & NEXT OBJECTIVES ("quelles sont mes prochaines quêtes")
        # -------------------------------------------------------------------
        is_quest_query = any(w in lowered for w in ["prochaine quête", "prochaines quêtes", "prochaine quete", "prochaines quetes", "next quest", "mes quêtes", "mes quetes", "quoi faire", "quelle quête", "progression"])
        if is_quest_query and not any(w in lowered for w in ["fini", "terminé", "complete", "mark", "rendu"]):
            summary = get_user_progression_summary(user_id)
            active_q = summary.get("active_quests", [])
            avail_q = summary.get("available_quests", [])
            needed_items = get_needed_quest_items(user_id)
            custom_items = get_custom_farm_items(user_id)

            if is_french:
                if active_q:
                    q_names = ", ".join([q["name"] for q in active_q[:2]])
                    spoken = f"Vos quêtes actives sont {q_names}. Briefing complet et liste de courses affichés sur Discord."
                elif avail_q:
                    q_names = ", ".join([q["name"] for q in avail_q[:2]])
                    spoken = f"Vos prochaines quêtes disponibles sont {q_names}. Détails affichés sur Discord."
                else:
                    spoken = "Toutes vos quêtes actuelles sont terminées. Prête pour le prochain raid !"

                lines = ["🎯 **VOS QUÊTES ACTIVES & OBJECTIFS :**\n"]
                for q in active_q:
                    lines.append(f"• ⚔️ **{q['name']}** (Donneur : {q['giver']} à {q['location']})")
                for q in avail_q[:3]:
                    lines.append(f"• 📜 **{q['name']}** *(Disponible auprès de {q['giver']})*")

                if needed_items:
                    lines.append("\n🎒 **ITEMS REQUIS POUR VOS QUÊTES :**")
                    for it in needed_items[:5]:
                        if it.get("buyable_in_town"):
                            merch_names = ", ".join([m["npc_slug"].title() for m in it["merchants"][:2]])
                            lines.append(f"• 🛒 **{it['item_slug'].title()}** : **Achetable au Château** auprès de {merch_names} *(Inutile de risquer un raid !)*")
                        else:
                            lines.append(f"• 🌲 **{it['item_slug'].title()}** : **À looter en raid** (Requis pour {it['quest_name']})")

                if custom_items:
                    lines.append("\n💎 **VOS ITEMS DE FARM PERSONNALISÉS (SKINS/COSMÉTIQUES) :**")
                    for cit in custom_items:
                        lines.append(f"• 💎 **{cit['name']}** ({cit['reason']})")

                display = "\n".join(lines)
            else:
                spoken = f"Active quests: {', '.join([q['name'] for q in active_q[:2]])}. Full briefing posted."
                display = "🎯 **QUEST PROGRESSION & OBJECTIVES**"

            return {"spoken_text": spoken, "display_text": display}

        # -------------------------------------------------------------------
        # 6. WEAPON STATS (Thrust Damage, Best Thrust Weapon, Spear Stats, Firearms, 2H Arsenal)
        # -------------------------------------------------------------------
        weapon_res = answer_weapon_query(clean_text, is_french)
        if weapon_res:
            return weapon_res

        # -------------------------------------------------------------------
        # 7. STATUS EFFECTS (Poison Antiheal, Duration, Mechanics)
        # -------------------------------------------------------------------
        effect_res = answer_effect_query(clean_text, is_french)
        if effect_res:
            return effect_res

        # -------------------------------------------------------------------
        # 8. EXTRACTION INTEL (Locations, Requirements, Routes)
        # -------------------------------------------------------------------
        ext_res = answer_extraction_query(clean_text, is_french)
        if ext_res:
            return ext_res

        # -------------------------------------------------------------------
        # 8.1 CREATURE & MINIBOSS COMBAT INTEL (Bloaters, Shamblers, Droolers, Brutes, Minibosses)
        # -------------------------------------------------------------------
        creature_keywords = [
            "bloat", "bloater", "boursouflé", "boursoufle", "shambler", "titubant", "traîne-pas",
            "traine-pas", "iron-shambler", "drooler", "drawler", "baveux", "brute", "pitchskin",
            "peau-de-poix", "peau de poix", "pale lady", "dame pale", "dame pâle", "dreg", "waif",
            "miséreux", "misereux", "hound", "miniboss", "monstre", "créature", "creature", "boss"
        ]
        is_creature_query = any(ck in lowered for ck in creature_keywords) and (
            any(w in lowered for w in [
                "pv", "vie", "degat", "dégât", "battre", "tuer", "vaincre", "comment", "c'est quoi",
                "stats", "faiblesse", "faiblesses", "point faible", "points faibles", "loot", "drop",
                "info", "boss", "qui est", "quels sont", "tactique", "fiche", "astuce", "conseil",
                "stratégie", "strategie", "montre moi", "montre", "show"
            ]) or "baveux" in lowered or "drooler" in lowered or "brute" in lowered or "bloater" in lowered or "bloat" in lowered or "shambler" in lowered or "monstre" in lowered
        )

        if is_creature_query and not any(w in lowered for w in ["map", "carte"]):
            from universal_v8_engine import render_universal_creature_card, CREATURES_DATABASE

            c_target = "drooler"
            if any(w in lowered for w in ["bloat", "bloater", "boursoufl"]):
                c_target = "bloat"
            elif any(w in lowered for w in ["shambler", "titubant", "traîne", "traine"]):
                c_target = "shambler"
            elif "brute" in lowered:
                c_target = "brute"
            elif any(w in lowered for w in ["drooler", "drawler", "baveux"]):
                c_target = "drooler"
            elif any(w in lowered for w in ["pitchskin", "peau"]):
                c_target = "pitchskin"
            elif any(w in lowered for w in ["pale", "pâle", "dame"]):
                c_target = "pale-lady"
            elif "dreg" in lowered:
                c_target = "dreg"
            elif "waif" in lowered:
                c_target = "waif"

            card_path = render_universal_creature_card(c_target, is_french=False)
            c_info = CREATURES_DATABASE.get(c_target, CREATURES_DATABASE["bloat"])

            spoken = f"{c_info['name_en']} has {c_info['health']} HP. Primary weak point is {c_info['weak_point']}. Creature profile dispatched."
            display = (
                f"👾 **CREATURE PROFILE : {c_info['name_en'].upper()} (HUNGER COMPANION)**\n\n"
                f"• 🩸 **Health Pool :** **{c_info['health']} HP**\n"
                f"• 🎯 **Critical Weak Point :** **{c_info['weak_point']}**\n"
                f"• 💥 **Attack Damage :** **{c_info['damage']}** | ⚡ **Movement Speed :** {c_info['speed']}\n"
                f"• 🎁 **Trophy & Drops :** **{c_info['trophy_name']}** ({c_info['trophy_rate']})\n"
                f"• 💡 **Combat Tactics :** {c_info['tactics']}\n\n"
                f"*(Authentic 3D creature render & harvest card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # 9. TALENT ADVICE & BUILDS (Thrust Master, Scavenger, Juggernaut)
        # -------------------------------------------------------------------
        tal_res = answer_talent_advice_query(clean_text, is_french)
        if tal_res:
            from co_pilot.card_renderer import render_talent_build_cards_both
            char_target = "Hugo"
            for c_cand in ["hugo", "marie", "eva", "otto", "gabriel", "serine"]:
                if c_cand in lowered:
                    char_target = c_cand.capitalize()
                    break
            p1, p2 = render_talent_build_cards_both(char_target, 100)
            tal_res["image_attachment"] = p1
            tal_res["image_attachments"] = [p1, p2]
            return tal_res

        # -------------------------------------------------------------------
        # 10. MERCHANT STOCK QUERY ("dit moi quel marchand vend...")
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["marchand", "marchant", "vendeur", "vend", "achete", "acheter", "vendor", "merchant"]):
            merch_res = answer_merchant_query(clean_text, is_french)
            if merch_res:
                return merch_res

        # -------------------------------------------------------------------
        # 10.1 TOP 3 BEST CONTAINERS FOR AN ITEM (with dynamic map if requested)
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["meilleur container", "meilleurs conteneurs", "best container", "meilleur conteneur"]):
            item_match = re.search(r"(?:pour|for|drop)\s+(?:l'|le\s+|la\s+|les\s+|the\s+)?([a-z\s]+)", lowered)
            item_query = item_match.group(1).strip() if item_match else clean_text
            res = answer_best_containers_query(item_query, is_french)
            if res:
                if any(w in lowered for w in ["map", "carte"]):
                    map_path, _ = generate_item_farm_map(item_query, "Sarlat Farm")
                    res["image_attachment"] = map_path
                return res

        # -------------------------------------------------------------------
        # 11. DUNGEONS & KEYS (Jacques Folly, The Pit, The Undercroft)
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["map", "carte"]) and any(w in lowered for w in ["folly", "dungeon", "donjon", "spawn de clef", "spawn de clé", "clef pour le gros chest", "puits", "pit", "undercroft", "sous-sol", "crypte"]):
            img_path, intel = generate_dungeon_tactical_map(clean_text)
            self.last_map_info = {
                "map_name": intel["map_name"],
                "type": "dungeon",
                "points_description": f"les accès du donjon {intel['title']} et les points clés",
                "intel": intel
            }
            spoken = f"Carte du donjon {intel['title']} transmise sur Discord." if is_french else "Dungeon map dispatched."
            display = f"🏰 **CARTE DU DONJON : {intel['title'].upper()}**\n\n🎯 **Objectifs :**\n" + "\n".join(intel["drops"])
            return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        dungeon_res = answer_dungeon_key_query(clean_text, is_french)
        if dungeon_res or any(w in lowered for w in ["donjon", "dungeon", "entrées du donjon", "entrees du donjon", "puits", "pit", "undercroft"]):
            card_path = render_dungeon_card(clean_text, is_french)
            if not dungeon_res:
                spoken = "Fiche tactique du donjon souterrain transmise sur Discord." if is_french else "Dungeon profile card dispatched."
                display = "🏰 **FICHE TECHNIQUE DU DONJON :**\n*(Accès et portes verrouillées affichés ci-dessous)*"
                dungeon_res = {"spoken_text": spoken, "display_text": display}
            dungeon_res["image_attachment"] = card_path
            return dungeon_res

        # -------------------------------------------------------------------
        # 12. CANONICAL GAME LORE & WORLDBUILDING (THE HUNGER UNIVERSE)
        # e.g. "c'est quoi the hunger", "qui est marie", "histoire du chateau", "lore des dregs"
        # -------------------------------------------------------------------
        from co_pilot.lore_engine import answer_lore_query
        lore_res = answer_lore_query(clean_text, is_french)
        if lore_res:
            return lore_res

        if any(w in lowered for w in ["fait aleatoire", "fait aléatoire", "random fact", "saviez-vous", "saviez vous"]):
            return answer_random_fact_query(is_french)

        # -------------------------------------------------------------------
        # 18. LEVEL UPDATE & QUEST COMPLETION
        # -------------------------------------------------------------------
        lvl_match = re.search(r"\b(?:i(?:'m| am)|level|lvl|niveau)\s+(\d+)\b", lowered)
        if lvl_match and any(w in lowered for w in ["hit level", "i'm level", "i am level", "set level", "niveau"]):
            new_lvl = int(lvl_match.group(1))
            update_user_level(user_id, new_lvl)
            spoken = f"Niveau mis à jour : {new_lvl}." if is_french else f"Updated to level {new_lvl}."
            return {"spoken_text": spoken, "display_text": f"📈 **Level Updated:** Level {new_lvl} for **{username}**."}

        comp_match = re.search(r"(?:finished|completed|turned in|done with|mark|fini|terminé|termine|complete)\s+(?:quest\s+|quête\s+)?(.+?)(?:\s+(?:as\s+)?(?:done|complete|terminée)|$)", lowered)
        if comp_match and any(w in lowered for w in ["finish", "complet", "turn", "done", "mark", "fini", "termine"]):
            query_q = comp_match.group(1).replace("done", "").replace("complete", "").replace("terminée", "").strip()
            if query_q and len(query_q) > 2:
                res = set_quest_status(user_id, query_q, "completed")
                if res.get("success"):
                    spoken = f"Quête {res['quest_name']} terminée." if is_french else f"Marked {res['quest_name']} complete."
                    return {"spoken_text": spoken, "display_text": f"✅ **Quest Completed:** {res['quest_name']}"}

        # -------------------------------------------------------------------
        # 19. KNOWLEDGE DB FALLBACK (NPCs, Items)
        # -------------------------------------------------------------------
        candidates = extract_key_search_terms(clean_text)
        for cand in candidates:
            # 1. Check quests first
            quests = search_quests(cand, limit=1)
            if quests and (re.search(r"\b(qu[eèé]te|quest|quests)\b", lowered) or "gavroche" in lowered):
                card_path = render_quest_card(q["slug"], is_french)
                self.last_active_quest = q["name"]
                spoken = f"La quête {q['name']} est donnée par {q['giver']} sur {q['location']}. Fiche de quête transmise." if is_french else f"Quest {q['name']} card dispatched."
                obj_lines = "\n".join([f"• 🎯 {o['description']}" for o in q.get("objectives", [])])
                display = (
                    f"📜 **FICHE TECHNIQUE DE MISSION : {q['name'].upper()}**\n\n"
                    f"• 👤 **Commanditaire :** {q['giver']} (Lieu : {q['location']})\n"
                    f"• 🎯 **Objectifs :**\n{obj_lines}\n"
                    f"• 🎁 **Récompense :** {q.get('reward_quantity', 1)}x {q.get('reward_item', 'Butin')}\n\n"
                    f"🖼️ *Fiche de mission Hunger Companion jointe ci-dessous.*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

            # 2. Check NPCs
            npcs = search_npcs(cand)
            if npcs:
                n = npcs[0]
                spoken = f"{n['name']} est {n.get('role', 'un PNJ')} au Château." if is_french else f"{n['name']} is {n.get('role', 'an NPC')} at Chateau."
                return {"spoken_text": spoken, "display_text": f"👤 **{n['name']}** ({n.get('role', 'NPC')})\n📍 Lieu : {n.get('location', 'Chateau')}\n{n.get('description', '')}"}

            # 3. Check items (factual data)
            STOPWORDS = {
                "moi", "toi", "lui", "eux", "mon", "ton", "son", "mes", "tes", "ses",
                "les", "des", "une", "pour", "par", "qui", "que", "quoi", "est", "sont",
                "avec", "sans", "dans", "sur", "sous", "vers", "chez", "tout", "tous",
                "toute", "toutes", "quel", "quels", "quelle", "quelles", "combien",
                "montre", "montrer", "affiche", "afficher", "donne", "donner", "voir",
                "skills", "skill", "sort", "sorts", "classe", "classes", "hero", "heros",
                "héros", "perso", "persos", "personnage", "personnages", "carte", "cartes",
                "map", "maps", "skin", "skins", "arbre", "arbres", "build", "builds",
                "stats", "stat", "loot", "item", "items", "objet", "objets", "truc", "trucs",
                "the", "and", "for", "with", "from", "show", "tell", "what", "how", "give"
            }
            if len(cand) >= 3 and cand.lower() not in STOPWORDS:
                items = search_items(cand, limit=1)
                if items:
                    it = items[0]
                    self.last_queried_item = it["name"]
                    c_conn = get_connection()
                    c_cur = c_conn.cursor()
                    c_cur.execute("SELECT * FROM weapons WHERE slug = ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1", (it["slug"], f"%{it['slug']}%", f"%{it['slug']}%"))
                    w_match = c_cur.fetchone()
                    c_conn.close()

                    if w_match:
                        raw_p = w_match["sell_price"] or "3 80"
                        parts = raw_p.split()
                        s_s, s_c = (int(parts[0]), int(parts[1])) if len(parts) >= 2 else (3, 80)
                        card_path = render_item_card(
                            w_match["name_fr"] if is_french else w_match["name_en"],
                            w_match["rarity_fr"] if is_french else w_match["rarity_en"],
                            s_s, s_c, "Arme",
                            f"Arme infligeant {w_match['thrust_damage']} d'estoc et {w_match['heavy_damage']} d'attaque lourde.",
                            icon_name="longboy.png" if "deux" in it["slug"] else None
                        )
                        spoken = f"La {w_match['name_fr']} {w_match['rarity_fr']} se vend {s_s} argent {s_c} cuivre." if is_french else f"{w_match['name_en']} card dispatched."
                    else:
                        from co_pilot.companion_intel import get_companion_item_intel
                        c_info = get_companion_item_intel(it["slug"])
                        s_sil = c_info.get("sell_silver", 0) if c_info else 5
                        s_cop = c_info.get("sell_copper", 50) if c_info else 0
                        card_path = render_item_card(it["name"], is_french=is_french)
                        spoken = f"{it['name']} ({it['rarity']}) sells for {s_sil} silver {s_cop} copper. Card dispatched."
                        display = (
                            f"📦 **OFFICIAL ITEM PROFILE : {it['name'].upper()}**\n\n"
                            f"• Rarity : **{it['rarity'].title()}** | Category : **{it['type'].title()}**\n"
                            f"• Resale Value : **{s_sil} Silver {s_cop} Copper** (To Vendors)\n"
                            f"• Raid Security : Keep in Secure Pouch if required for active progression.\n\n"
                            f"🖼️ *(High-resolution item card attached below)*"
                        )
                    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 20. UNKNOWN TERM / UNPARSED INPUT
        # Strictly SILENT on casual chatter to avoid interrupting squad conversations!
        # Only asks for explanation if the user EXPLICITLY asked about a word.
        # -------------------------------------------------------------------
        is_explicit_term_query = any(w in lowered for w in [
            "c'est quoi", "c quoi", "qu'est ce que", "quest ce que", "que signifie",
            "tu connais", "tu sais ce que", "c'est quoi le terme", "c'est quoi ce mot",
            "what is", "what does", "do you know", "meaning of"
        ])

        if is_explicit_term_query and candidates:
            candidate_term = candidates[0]
            # Arm pending term with timestamp (timeout after 25s)
            self.pending_term = candidate_term
            self.pending_term_time = time.time()

            if is_french:
                spoken = f"Je ne connais pas encore le terme '{candidate_term}'. Qu'est-ce que cela signifie ? Dites 'oublie' pour ignorer."
                display = f"❓ **Terme Inconnu :** *\"{candidate_term}\"*\n🗣️ *Expliquez ce que cela signifie, ou dites **'Oublie'** pour annuler.*"
            else:
                spoken = f"I do not recognize '{candidate_term}' yet. What does it mean? Say 'forget it' to skip."
                display = f"❓ **Unknown Term :** *\"{candidate_term}\"*\n🗣️ *Explain verbally, or say **'Forget it'**.*"
            return {"spoken_text": spoken, "display_text": display}

        # Casual talk or unrecognized speech -> 100% SILENT in voice so squad talk is never disturbed!
        display_hint = f"ℹ️ *Entendu : « {clean_text} » (non reconnu — restée silencieuse pour ne pas déranger)*"
        return {"spoken_text": "", "display_text": display_hint}
