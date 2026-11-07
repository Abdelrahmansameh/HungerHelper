with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_block = '''        # 1. CHARACTER KITS & ABILITIES ("ult de marie", "passif de marie", "sort d'eva", "fiche de marie")
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
                    f"⚡ **SPECIAL / ULTIMATE ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 💥 **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_pass:
                ab_name, ab_desc = kit["passive"]
                spoken = f"{kit['name']}'s Passive ability is {ab_name}: {ab_desc}"
                display = (
                    f"🛡️ **PASSIVE ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 🛡️ **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            elif is_tact:
                ab_name, ab_desc = kit["tactical"]
                spoken = f"{kit['name']}'s Tactical ability is {ab_name}: {ab_desc}"
                display = (
                    f"✨ **TACTICAL ABILITY : {kit['name'].upper()}**\\n\\n"
                    f"• 🗡️ **Ability :** **{ab_name}**\\n"
                    f"• 🎯 **Combat Effect :** {ab_desc}\\n\\n"
                    f"*(Full hero dossier & prestige skins attached below)*"
                )
            else:
                spoken = f"Tactical operative profile for {kit['name']} dispatched."
                display = (
                    f"⚔️ **OFFICIAL HERO PROFILE : {kit['name'].upper()} ({kit['title'].upper()})**\\n\\n"
                    f"• 🛡️ **Passive :** **{kit['passive'][0]}** — {kit['passive'][1]}\\n"
                    f"• 🗡️ **Tactical [Q] :** **{kit['tactical'][0]}** — {kit['tactical'][1]}\\n"
                    f"• 💥 **Special / Ult [E] :** **{kit['ultimate'][0]}** — {kit['ultimate'][1]}\\n\\n"
                    f"*(Full abilities kit & unlocked prestige skins attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}
'''

# Find index of line 399
idx_start = -1
for i, l in enumerate(lines):
    if "# 1. CHARACTER" in l:
        idx_start = i
        break

idx_end = -1
for i in range(idx_start, len(lines)):
    if "# 1.1 SKINS & COSMETICS" in lines[i]:
        idx_end = i
        break

print(f"Replacing lines {idx_start} to {idx_end}")
new_lines = lines[:idx_start] + [new_block + "\n"] + lines[idx_end:]

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Hero abilities block patched in brain.py successfully!")
