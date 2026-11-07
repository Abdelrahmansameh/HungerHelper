import os
import re
import sqlite3
from typing import Optional, Dict, Any, Tuple

LORE_DATABASE = {
    "the_hunger": {
        "slug": "the-hunger-calamity",
        "title_en": "The Hunger Calamity & The Great Fall",
        "title_fr": "Le Fléau de la Faim et la Grande Chute",
        "category": "World History & Setting",
        "spoken_en": "The Hunger is a supernatural Napoleonic-era affliction that collapsed 19th-century Europe into ruin, transforming the starved and deceased into mutated horrors.",
        "spoken_fr": "La Faim est un fléau surnaturel de l'ère napoléonienne ayant dévasté l'Europe du XIXe siècle, transformant les défunts et affamés en abominations mutées.",
        "lore_en": (
            "During the twilight of the Napoleonic Wars around 1815, an apocalyptic biological and supernatural plague known as **The Hunger** (La Faim) swept across Europe. "
            "Agricultural systems collapsed, famine consumed populations, and a foul miasma seeped from the earth. "
            "Those who died from starvation did not stay dead: they rose as Dregs and Shamblers, while ambient corruption birthed grotesque predators like Bloaters and Brutes. "
            "Civilization fractured, leaving only isolated fortified enclaves struggling for raw survival."
        ),
        "lore_fr": (
            "Au crépuscule des guerres napoléoniennes vers 1815, une peste biologique et surnaturelle connue sous le nom de **La Faim** a ravagé l'Europe. "
            "Les récoltes ont pourri, les armées se sont effondrées et une corruption obscure a émergé des terres. "
            "Les morts de faim ne reposent plus en paix : ils se relèvent sous forme de Miséreux et Titubants, tandis que la corruption donne naissance aux Boursouflés et aux Colosses."
        ),
        "tactical_en": "Scavengers must venture into quarantine sectors (Sarlat Farm, Jacques Bridge, Sombre Forest) to harvest food, gunpowder, and medicinal components.",
        "tactical_fr": "Les pillards doivent s'aventurer dans les secteurs de quarantaine (Sarlat, Pont Jacques, Sombre Forêt) pour glaner vivres, salpêtre et remèdes."
    },

    "chateau": {
        "slug": "chateau-sanctuary",
        "title_en": "The Château Sanctuary",
        "title_fr": "Le Sanctuaire du Château",
        "category": "Main Bastion & Hub",
        "spoken_en": "The Château is humanity's fortified bastion in the region, housing craft guilds, traders, and expeditionary staging grounds.",
        "spoken_fr": "Le Château est le dernier bastion fortifié de l'humanité dans la région, abritant les guildes d'artisans, marchands et préparatifs de raid.",
        "lore_en": (
            "Perched atop ancient defensive ramparts, **The Château** stands as the last organized haven in a broken world. "
            "Here, remnants of the military, guild artisans, and scavengers form an uneasy alliance. "
            "The upper ramparts host command operations, while the subterranean lower levels house the Forge, Outfitter workshops, and deep catacombs. "
            "It is the central nexus where survivors store their Stash, trade sovereign currency, and plan high-risk incursions into raid sectors."
        ),
        "lore_fr": (
            "Bâti sur d'anciens remparts défensifs, **Le Château** est l'ultime refuge organisé dans ce monde dévasté. "
            "Militaires, maîtres artisans et survivants y maintiennent une trêve fragile. "
            "Les ateliers de forge et de confection y côtoient les catacombes souterraines où les commandants gèrent leur réserve (Stash) et préparent leurs incursions."
        ),
        "tactical_en": "Safe zone. Zero combat danger. Key NPCs include Henri, Sirene, Voyant, Mr. Sweet, and your tactical archivist Eloise.",
        "tactical_fr": "Zone sécurisée sans danger de combat. Marchands clés : Henri, Sirène, Voyant le Fusilier, Mr Sweet et votre archiviste Éloïse."
    },

    "marie": {
        "slug": "operative-marie",
        "title_en": "Sister Marie — The Apothecary Nun",
        "title_fr": "Sœur Marie — La Nonne Apothicaire",
        "category": "Operative Lore",
        "spoken_en": "Sister Marie is a former convent herbalist turned battle medic, wielding corrosive acid flasks and healing salves to cleanse the blight.",
        "spoken_fr": "Sœur Marie est une ancienne herboriste de couvent devenue médecin de guerre, utilisant des fioles d'acide corrosif et des baumes curatifs.",
        "lore_en": (
            "When the convent of Saint-Lazare fell to the infected hordes, Sister Marie cast aside her vows of non-violence to save wounded survivors. "
            "Mastering field chemistry and botanical extracts, she formulates caustic acid mixtures that disintegrate hardened chitin and armored dregs. "
            "Her passive alchemical pouch allows her to carry extra medical vials, making her the ultimate frontline survivability specialist."
        ),
        "lore_fr": (
            "Quand le couvent de Saint-Lazare fut submergé par les infectés, Sœur Marie abandonna ses vœux de non-violence pour sauver les blessés. "
            "Maîtrisant l'alchimie botanique, elle conçoit des fioles d'acide corrosif brisant les armures ennemies. "
            "Sa besace alchimique passive lui permet de transporter 2 fioles de médecine supplémentaires en raid."
        ),
        "tactical_en": "Class: Support / Combat Medic. Ultimate: Acid Flask (shatters enemy armor). Tactical: Healing Salve (75 HP regen).",
        "tactical_fr": "Classe : Soutien / Médecin de combat. Ultime : Fiole d'Acide (brise l'armure). Tactique : Baume Curatif (75 PV)."
    },

    "otto": {
        "slug": "operative-otto",
        "title_en": "Otto — The Veteran Armorer",
        "title_fr": "Otto — Le Vétéran Armurier",
        "category": "Operative Lore",
        "spoken_en": "Otto is a hardened veteran armorer whose mastery of steel gives him unrivaled defense and fortification skills.",
        "spoken_fr": "Otto est un maître armurier endurci dont l'expertise de l'acier confère une durabilité et une résistance défensive inégalées.",
        "lore_en": (
            "A veteran of grueling continental sieges, Otto understands that survival is dictated by steel thickness and joint articulation. "
            "Having lost his regiment to a night assault by Droolers, he retreated to the Château Forge. "
            "His passive skill slows armor degradation by 30%, allowing his squad to endure protracted firefights without structural suit failure."
        ),
        "lore_fr": (
            "Vétéran des sièges continentaux, Otto sait que la survie dépend de l'épaisseur de l'acier. "
            "Après la perte de son régiment face aux Baveux, il a perfectionné son art à la forge. "
            "Son passif réduit l'usure de l'armure de 30%, permettant à son escouade d'encaisser des affrontements prolongés."
        ),
        "tactical_en": "Class: Tank / Defense. Passive: Armor Smith (-30% wear rate). Ultimate: Fortify / Shield Wall.",
        "tactical_fr": "Classe : Tank / Défenseur. Passif : Maître Armurier (-30% usure). Ultime : Fortification et maintien de ligne."
    },

    "eva": {
        "slug": "operative-eva",
        "title_en": "Eva — The Duelist Infiltrator",
        "title_fr": "Eva — La Duelliste Infiltrée",
        "category": "Operative Lore",
        "spoken_en": "Eva is an agile skirmisher and former duelist who blinds enemies with flashbangs to strike lethal weak points.",
        "spoken_fr": "Eva est une escarmoucheuse agile et ancienne duelliste qui aveugle les ennemis avec des grenades incapacitantes pour frapper les points faibles.",
        "lore_en": (
            "Born to aristocratic fencing lineage, Eva adapted the precision of courtly rapier dueling to the brutal realities of urban combat. "
            "Light on her feet and deadly at close quarters, she disorients pursuers with improvised flashbangs before lunging with pinpoint thrusts."
        ),
        "lore_fr": (
            "Issue d'une lignée d'escrimeurs aristocratiques, Eva a adapté la précision du fleuret aux combats brutaux des ruines. "
            "D'une agilité hors pair, elle aveugle les poursuivants avec des grenades Flashbang avant d'asséner des coups d'estoc mortels."
        ),
        "tactical_en": "Class: High-Mobility Duelist. Ultimate: Flashbang (blinds enemies). Specializes in Rapier and lightweight armor.",
        "tactical_fr": "Classe : Duelliste / Infiltration. Ultime : Grenade Aveuglante (Flashbang). Spécialiste de la Rapière et armures légères."
    },

    "hugo": {
        "slug": "operative-hugo",
        "title_en": "Hugo — The Maniac Berserker",
        "title_fr": "Hugo — Le Maniaque",
        "category": "Operative Lore",
        "spoken_en": "Hugo is an unhinged frontline berserker with unnatural pain tolerance whose terrifying war cries empower his squad.",
        "spoken_fr": "Hugo est un berserker de première ligne doté d'une tolérance surnaturelle à la douleur dont les cris de guerre galvanisent son escouade.",
        "lore_en": (
            "Driven half-mad by years of solitude in the Sombre Forest, Hugo turned his agony into unmatched ferocity. "
            "His thick calloused skin naturally absorbs 15% of physical impact damage, and his thunderous War Cry triggers an adrenaline surge that boosts melee attack speed."
        ),
        "lore_fr": (
            "Devenu à demi-fou après des années de solitude dans la forêt sombre, Hugo a fait de sa douleur une force destructrice. "
            "Sa peau épaisse absorbe 15% des dégâts physiques et son Cri de Guerre galvanise l'escouade en augmentant la cadence de corps à corps."
        ),
        "tactical_en": "Class: Frontline Brawler. Passive: Thick Skin (15% damage reduction). Ultimate: War Cry (squad melee speed surge).",
        "tactical_fr": "Classe : Bagarreur de choc. Passif : Cuir Épais (-15% dégâts reçus). Ultime : Cri de Guerre (cadence d'attaque accrue)."
    },

    "eloise": {
        "slug": "npc-eloise",
        "title_en": "Éloïse — The Tactical Archivist",
        "title_fr": "Éloïse — L'Archiviste Tactique",
        "category": "Allied NPC & Co-Pilot",
        "spoken_en": "Éloïse is the Château's tactical archivist, mapping safe routes, tracking bounties, and preserving humanity's lost knowledge.",
        "spoken_fr": "Éloïse est l'archiviste tactique du Château, cartographiant les routes sûres, suivant les primes et préservant les savoirs perdus.",
        "lore_en": (
            "Stationed at the Outer Ramparts of the Château, **Éloïse** serves as mission control and intelligence coordinator for all expeditionary squads. "
            "Daughter of a royal cartographer, she painstakingly documents every creature weak point, container spawn, and extract route across the provinces. "
            "Her personal quest chain guides commanders through recovery of the 7 sacred Mount Sinai manuscripts."
        ),
        "lore_fr": (
            "Établie aux Remparts Extérieurs du Château, **Éloïse** est la coordinatrice de renseignement de toutes les escouades d'expédition. "
            "Fille d'un cartographe royal, elle répertorie chaque point faible des monstres, chaque conteneur et chaque route d'extraction. "
            "Sa suite de quêtes personnelles mène les commandants à retrouver les 7 Livres sacrés du Mont Sinaï."
        ),
        "tactical_en": "Your live voice co-pilot. She delivers instantaneous voice briefings, weapon HTK math, stash scans, and tactical map overlays.",
        "tactical_fr": "Votre co-pilote vocale en direct. Elle fournit calculs de TTK, cartes sans indication, analyses de réserve et dossiers de butin."
    },

    "mr_sweet": {
        "slug": "npc-mr-sweet",
        "title_en": "Mr. Sweet — The Black-Market Broker",
        "title_fr": "Mr Sweet — Le Trafiquant du Marché Noir",
        "category": "Château NPC",
        "spoken_en": "Mr. Sweet is a shrewd contraband dealer operating in the shadows of the Château, trading opium, luxury curios, and high-value silver.",
        "spoken_fr": "Mr Sweet est un trafiquant avisé opérant dans les ombres du Château, négociant opium, curiosités de luxe et pièces d'argent.",
        "lore_en": (
            "Unmoved by ideological causes, **Mr. Sweet** deals strictly in commodities that retain value in a broken world: refined opium, tobacco, silver bowls, and illicit relics. "
            "He tasks scavengers with contracts like *A Touch of Bribery* and *Down from Mount Sinai*, rewarding those who keep his smuggling pipeline flowing."
        ),
        "lore_fr": (
            "Insensible aux grands discours, **Mr Sweet** ne s'intéresse qu'aux denrées de valeur : opium raffiné, tabac, bols en argent et reliques illicites. "
            "Il confie des contrats lucratifs comme *A Touch of Bribery* et *Down from Mount Sinai*, récompensant grassement les pillards audacieux."
        ),
        "tactical_en": "Quest Giver: Key contracts for opium and church curios. Essential progression step to unlock mid-tier trade routes.",
        "tactical_fr": "Commanditaire de quêtes : Nécessaire pour la progression des quêtes d'opium et curiosités d'église."
    },

    "dregs": {
        "slug": "bestiary-dregs",
        "title_en": "The Dregs (Les Miséreux)",
        "title_fr": "Les Miséreux (Dregs)",
        "category": "Bestiary Lore",
        "spoken_en": "Dregs are the tragic remnants of common villagers and soldiers, starving and half-feral, attacking in packs with farm tools.",
        "spoken_fr": "Les Miséreux sont les vestiges tragiques de paysans et soldats affamés, redevenus sauvages et attaquant en meute avec des outils agricoles.",
        "lore_en": (
            "The most widespread victims of The Hunger. Retaining only vestigial human intelligence, Dregs wander farmlands muttering fragmented memories. "
            "Some still wear military coats (Voltigeurs) or tattered aprons (Dreg Farmers). While individually weak (60-80 HP), they swarm relentlessly and can overwhelm solitary scavengers."
        ),
        "lore_fr": (
            "Les victimes les plus nombreuses du Fléau. Ne conservant qu'une lueur de conscience, les Miséreux errent en marmonnant des souvenirs brisés. "
            "Certains portent encore des uniformes (Voltigeurs) ou des tabliers souillés (Fermiers). Bien que fragiles (60-80 PV), ils attaquent en meutes vicieuses."
        ),
        "tactical_en": "Weakness: Headshots kill instantly. The Dreg Farmer at Garnier's Farm has a 100% Always Drop rate for the Peasant's Burden spear schema.",
        "tactical_fr": "Faiblesse : Tirs à la tête mortels. Le Fermier Miséreux de Garnier Farm lâche à 100% le schéma Peasant's Burden pour la lance."
    },

    "bloaters": {
        "slug": "bestiary-bloaters",
        "title_en": "The Bloaters (Les Boursouflés)",
        "title_fr": "Les Boursouflés (Bloaters)",
        "category": "Bestiary Lore",
        "spoken_en": "Bloaters are putrid corpses swollen with toxic gas and volatile bile that explode upon death, covering the area in acid mist.",
        "spoken_fr": "Les Boursouflés sont des cadavres putrides gonflés de gaz toxique et de bile acide qui explosent à leur mort en nuages mortels.",
        "lore_en": (
            "A gruesome byproduct of waterborne contagion. Decomposing viscera generate explosive internal pressures. "
            "Bloaters waddle toward the living with horrifying determination before self-detonating in a shower of corrosive venom."
        ),
        "lore_fr": (
            "Produit répugnant de la contamination des eaux. Leurs organes en décomposition génèrent une pression interne phénoménale. "
            "Les Boursouflés titubent vers les vivants pour exploser en un nuage de poison toxique corrosif."
        ),
        "tactical_en": "Health: 60 HP. Weakness: Swollen acid sacs. Shoot from a distance to cause a chain explosion among neighboring monsters.",
        "tactical_fr": "Points de vie : 60 PV. Faiblesse : Sacs d'acide. Tirez à distance pour les faire exploser sans subir les éclaboussures."
    },

    "brutes": {
        "slug": "bestiary-brutes",
        "title_en": "The Brutes (Les Colosses)",
        "title_fr": "Les Brutes (Colosses)",
        "category": "Bestiary Lore",
        "spoken_en": "Brutes are massive mutated abominations boasting 900 HP and devastating sweeps, vulnerable only to critical back strikes.",
        "spoken_fr": "Les Brutes sont de colossales abominations mutées de 900 PV aux balayages dévastateurs, vulnérables uniquement aux coups critiques dans le dos.",
        "lore_en": (
            "Formed by extreme biological hypertrophy under the plague's influence, Brutes tower over mortal men. "
            "Their frontal bone plating deflects standard ammunition, but their deformed spinal column remains completely exposed."
        ),
        "lore_fr": (
            "Nées d'une hypertrophie musculaire monstrueuse causée par la Faim, les Brutes dépassent les hommes de plusieurs têtes. "
            "Leurs plaques osseuses frontales dévient les tirs, mais leur colonne vertébrale est à nu et vulnérable aux attaques dorsales."
        ),
        "tactical_en": "Health: 900 HP. Frontal hits deal only 50% damage. Flank and strike their exposed spine for 2x Critical Damage.",
        "tactical_fr": "Points de vie : 900 PV. Dégâts frontaux réduits de 50%. Contournez-les pour frapper la colonne dorsale à 2x dégâts critiques."
    },

    "pale_lady": {
        "slug": "bestiary-pale-lady",
        "title_en": "The Pale Lady (La Dame Pâle)",
        "title_fr": "La Dame Pâle (The Pale Lady)",
        "category": "Bestiary Lore & Elite Boss",
        "spoken_en": "The Pale Lady is a tragic ghostly specter channeling devastating weeping incantations, requiring heavy stagger to interrupt.",
        "spoken_fr": "La Dame Pâle est un spectre tragique canalisant des incantations de désespoir mortelles, nécessitant des attaques lourdes pour être interrompue.",
        "lore_en": (
            "Legend speaks of an aristocratic bride whose wedding carriage was ambushed during the first week of The End. "
            "Consolidated by sorrow and dark miasma, she haunts forgotten ruins, weeping mournfully before unleashing telekinetic shockwaves."
        ),
        "lore_fr": (
            "La légende raconte qu'elle était une jeune mariée noble dont le convoi fut massacré aux premiers jours de la Grande Chute. "
            "Nourrie par le désespoir et le miasme, elle hante les ruines en pleurant avant de libérer des ondes de choc dévastatrices."
        ),
        "tactical_en": "Health: 900 HP. Primary Weakness: Channeled Incantation Stagger. Strike with heavy overhead melee blows to break her chant.",
        "tactical_fr": "Points de vie : 900 PV. Faiblesse majeure : Interruption d'incantation. Assénez des attaques lourdes pour stopper son chant."
    },

    "sarlat_farm": {
        "slug": "location-sarlat-farm",
        "title_en": "Sarlat Farm — The Breadbasket Ruins",
        "title_fr": "Ferme de Sarlat — Les Greniers Meurtris",
        "category": "Raid Sector Lore",
        "spoken_en": "Sarlat Farm was once the agricultural breadbasket of the valley, now overrun by Dregs, roaming Brutes, and fertile grain silos.",
        "spoken_fr": "La ferme de Sarlat était autrefois le grenier à blé de la vallée, aujourd'hui envahie par les Miséreux, les Brutes et les silos de grain.",
        "lore_en": (
            "Spanning rolling hills, ancient stone windmills, and the grand Garnier estate, Sarlat Farm fed thousands before the calamity. "
            "Today, it is the primary raid sector for novice scavengers seeking Flour, Garlic, Lavender, and agricultural blueprints."
        ),
        "lore_fr": (
            "Étendue sur des collines vallonnées, des moulins de pierre et le domaine Garnier, la ferme de Sarlat nourrissait la province. "
            "C'est aujourd'hui le secteur de raid de prédilection pour récolter Farine, Ail, Lavande et pièces de forgeron."
        ),
        "tactical_en": "Difficulty: Low to Moderate. Key landmarks: Garnier's Windmill, Dupo Farrier workshop, Central Granary.",
        "tactical_fr": "Difficulté : Faible à moyenne. Points d'intérêt clés : Moulin de Garnier, atelier Dupo Farrier, Grenier central."
    },

    "jacques_bridge": {
        "slug": "location-jacques-bridge",
        "title_en": "Jacques Bridge & The Folly",
        "title_fr": "Pont Jacques & La Folie",
        "category": "Raid Sector Lore",
        "spoken_en": "Jacques Bridge is a strategic stone crossing over deep gorges, hiding the submerged ruins of the subterranean Jacques Folly fortress.",
        "spoken_fr": "Pont Jacques est un passage stratégique au-dessus de gorges escarpées, dissimulant l'accès à la forteresse souterraine de la Folie de Jacques.",
        "lore_en": (
            "Constructed by military engineers to secure the river transit, Jacques Bridge became a death trap when retreating armies detonated its arches. "
            "Deep in the northern ridge lies the descent into **Jacques Folly**, an underground redoubt filled with 174 locked treasure caches."
        ),
        "lore_fr": (
            "Édifié pour verrouiller le transit fluvial, le pont Jacques est devenu un charnier lors de la retraite des armées impériales. "
            "Sous sa crête nord se trouve l'entrée de la **Folie de Jacques**, un complexe souterrain abritant 174 caches de ravitaillement scellées."
        ),
        "tactical_en": "Difficulty: High. Heavy chokepoints and sniper perches. Entrance to Jacques Folly requires a Jacques Folly Key.",
        "tactical_fr": "Difficulté : Élevée. Nombreux goulets d'étranglement. Accès à la Folie de Jacques requiert une Clé de la Folie."
    },

    "sombre_forest": {
        "slug": "location-sombre-forest",
        "title_en": "Sombre Forest — The Primordial Wilderness",
        "title_fr": "Sombre Forêt — Les Bois Primordiaux",
        "category": "Raid Sector Lore",
        "spoken_en": "Sombre Forest is an ancient, mist-choked woodland harboring dark monoliths, lumberjack outposts, and lethal Drooler packs.",
        "spoken_fr": "Sombre Forêt est un bois antique noyé de brume abritant d'anciens monolithes, des camps de bûcherons et des meutes de Baveux mortelles.",
        "lore_en": (
            "Dating back to pre-Roman pagan eras, the Sombre Forest resisted human conquest for centuries. "
            "When The Hunger arrived, the trees grew twisted and perpetual darkness enveloped the groves. "
            "Scavengers venture here for Saltpetre, Charcoal, and rare herbal flora, but many never return."
        ),
        "lore_fr": (
            "Remontant aux époques païennes, la forêt sombre a toujours résisté à l'homme. "
            "Avec la Faim, ses arbres se sont tordus dans une obscurité perpétuelle. "
            "Les pillards s'y risquent pour le Salpêtre, le Charbon et les plantes rares, mais peu en reviennent."
        ),
        "tactical_en": "Difficulty: Extreme. Poor visibility, roaming elite beasts, and hidden bear traps.",
        "tactical_fr": "Difficulté : Extrême. Faible visibilité, prédateurs féroces et pièges à ours dissimulés dans les fourrés."
    }
}

def resolve_lore_topic(query: str) -> Optional[Dict[str, Any]]:
    """Determine matching lore topic from user query string."""
    q = query.lower()
    
    # Character Lore
    if any(w in q for w in ["marie", "soeur marie", "sister marie"]): return LORE_DATABASE["marie"]
    if any(w in q for w in ["otto", "armurier otto"]): return LORE_DATABASE["otto"]
    if any(w in q for w in ["eva", "duelliste eva"]): return LORE_DATABASE["eva"]
    if any(w in q for w in ["hugo", "maniaque hugo", "berserker hugo"]): return LORE_DATABASE["hugo"]
    if any(w in q for w in ["eloise", "éloïse", "qui es tu", "qui es-tu", "who are you"]): return LORE_DATABASE["eloise"]
    if any(w in q for w in ["mr sweet", "monsieur sweet", "sweet"]): return LORE_DATABASE["mr_sweet"]
    
    # Bestiary Lore
    if any(w in q for w in ["dreg", "dregs", "misereux", "miséreux", "farmer dreg"]): return LORE_DATABASE["dregs"]
    if any(w in q for w in ["bloat", "bloater", "bloaters", "boursoufle", "boursouflé", "boursoufles", "boursouflés"]): return LORE_DATABASE["bloaters"]
    if any(w in q for w in ["brute", "brutes", "colosse", "colosses"]): return LORE_DATABASE["brutes"]
    if any(w in q for w in ["pale lady", "dame pale", "dame pâle"]): return LORE_DATABASE["pale_lady"]

    # Location Lore
    if any(w in q for w in ["sarlat", "ferme de sarlat", "sarlat farm"]): return LORE_DATABASE["sarlat_farm"]
    if any(w in q for w in ["jacques bridge", "pont jacques", "jacques folly", "folie de jacques"]): return LORE_DATABASE["jacques_bridge"]
    if any(w in q for w in ["sombre", "sombre forest", "foret sombre", "forêt sombre"]): return LORE_DATABASE["sombre_forest"]

    # World & Setting Lore
    if any(w in q for w in ["chateau", "château", "sanctuaire", "sanctuary"]): return LORE_DATABASE["chateau"]
    if any(w in q for w in ["hunger", "faim", "histoire du jeu", "lore", "calamite", "calamité", "fleau", "fléau", "apocalypse", "monde", "world"]): return LORE_DATABASE["the_hunger"]

    return None

def answer_lore_query(query: str, is_french: bool = False) -> Optional[Dict[str, Any]]:
    """Generate dual-modality response for canonical game lore."""
    lowered = query.lower()
    
    is_lore_query = any(w in lowered for w in [
        "lore", "histoire", "qui est", "qui sont", "c'est quoi l'histoire", "raconte moi", "raconte-moi",
        "who is", "who was", "who are", "what is the story", "tell me about", "background of", "origin of"
    ]) or any(lowered.strip() == k for k in [
        "histoire", "lore", "c'est quoi the hunger", "c'est quoi le chateau", "qui sont les dregs"
    ])

    if not is_lore_query:
        # Check if asking specifically about a character's history
        if not (any(w in lowered for w in ["qui est", "who is", "histoire de", "story of"]) and 
                any(c in lowered for c in ["marie", "otto", "eva", "hugo", "eloise", "sweet"])):
            return None

    topic = resolve_lore_topic(query)
    if not topic:
        return None

    from universal_v8_engine import render_lore_card
    card_path = render_lore_card(topic["slug"])

    title = topic["title_fr"] if is_french else topic["title_en"]
    spoken = topic["spoken_fr"] if is_french else topic["spoken_en"]
    body = topic["lore_fr"] if is_french else topic["lore_en"]
    tactical = topic["tactical_fr"] if is_french else topic["tactical_en"]

    if is_french:
        display = (
            f"📜 **ARCHIVE DU SAVOIR : {title.upper()}**\n\n"
            f"• 🏛️ **Catégorie :** *{topic['category']}*\n\n"
            f"{body}\n\n"
            f"⚔️ **Pertinence Tactique :**\n*{tactical}*\n\n"
            f"🖼️ *(Dossier historique haute résolution joint ci-dessous)*"
        )
    else:
        display = (
            f"📜 **LORE ARCHIVE : {title.upper()}**\n\n"
            f"• 🏛️ **Classification :** *{topic['category']}*\n\n"
            f"{body}\n\n"
            f"⚔️ **Tactical Relevance :**\n*{tactical}*\n\n"
            f"🖼️ *(High-resolution lore archive card attached below)*"
        )

    return {
        "spoken_text": spoken,
        "display_text": display,
        "image_attachment": card_path,
        "image_attachments": [card_path]
    }
