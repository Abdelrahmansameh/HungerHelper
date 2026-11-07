# MASTER REQUIREMENTS & ARCHITECTURAL SPECIFICATION: ELOISE TACTICAL CO-PILOT
**Project:** Hunger Helper / Eloise Tactical Assistant for *The Hunger*  
**Codified Date:** 2026-11-05  
**Permanent Anchor:** Codifies all 69 conversation turns, user instructions, bug fixes, design guidelines, and system architectures.

---

## 1. Persona, Vocal Interaction & Voice Pipeline
1. **Identity & Avatar:**
   - Name: **Éloïse** (The official Château Hub Provisioner / Companion).
   - Portrait: Official Éloïse NPC art (`assets/npcs/eloise.png`).
2. **Audio Stack & Latency (RTX 3070 CUDA):**
   - **STT (Speech-to-Text):** Faster-Whisper `large-v3-turbo` (809M) running locally on CUDA fp16 for instantaneous turnaround (<150ms).
   - **TTS (Text-to-Speech):** Microsoft Edge-TTS `fr-FR-VivienneMultilingualNeural` (or `fr-FR-EloiseNeural`), high clarity, natural French/English accent.
   - **VAD & Energy Gating:** Adaptive ambient RMS noise floor calibration with automatic headset mic sensitivity thresholding.
   - **Barge-In (Interruptibility):** Uttering the wake word **« Éloïse »** at any millisecond immediately halts active audio playback (`active_voice_client.stop()`) and prepares the bot to accept the new tactical command without desyncing state.
   - **Voice Turnaround Rule:** Vocal answers must be **concise and punchy** (1 to 2 short tactical sentences max) so team comms remain clear during high-intensity raids. Detailed stats, ingredients, and tables are offloaded to visual Discord embeds.
3. **Language Rules:**
   - **Default Language:** **PURE ENGLISH** for all card titles, headers, data pills, text embeds, and spoken responses.
   - **French Exception:** Speak/render in French **ONLY** when the user explicitly requests it (e.g. `en français`, `en francais`, `traduis en français`). Even if the user asks a question in French (e.g., `montre moi les skins de la rapier`), the assistant responds in English unless French is requested.

---

## 2. Universal 100% Hunger Companion Database Ingestion
Based on the official Hunger Companion browse map:
1. **Items (700 Total Entries):**
   - 37 Weapons (Melee weapons & Firearms)
   - 29 Bags (Pockets, Backpacks, Pouch, Satchels)
   - 67 Containers (Safes, Strongboxes, Munition Crates, Sacks, Cabinets, Furniture)
   - 258 Materials & Expedition Loot
   - 176 Schemas & Crafting Recipes
   - 102 Quest Items
   - 13 Keys (Gold, Silver, Bronze, Dungeon Keys)
   - 13 Armour Pieces (Helmets, Cuirasses, Greaves)
   - 13 Medicine Vials & Balms
   - 17 Food Provisions
   - 12 Drinks & Spirits
   - 10 Tools (Lockpicks, Tongs, Needles)
   - 10 Trinkets
   - 5 Ammunition Flasks & Types
   - 4 Currencies (Copper, Silver, Gold, Sovereign)
   - 1 Misc
2. **Skins (128+ Skins):**
   - Weapon skins (e.g., Peasant's Burden, Bacchus' Wand, Basilisk, Loup, Recluse, Partisan, Hybernia, Solstice, Hohenzollern, Medici, Argent and Vert, Frederick's Revenge).
   - Bag skins & character cosmetic outfits.
3. **Quests (99 Quests & 21 NPCs):**
   - Full quest chains, progression trees, givers, objectives, coordinates, items needed.
4. **Maps & Dungeons (4 Maps):**
   - Sarlat Farm, Jacques Bridge, Sombre Forest, The Château Hub.
   - Dungeons: The Pit, Jacques Folly, The Undercroft, Catacombs, Rat's Nest Cave.
5. **Characters & Mastery (6 Operatives):**
   - Marie, Otto, Eva, Gabriel, Hugo, Serine.
   - All 5 talent trees: Combat, Mobility, Survival, Tactics, Mastery.
   - Full combat kits: Passive, Tactical [Q], Special/Ultimate [E], prestige cosmetics.
6. **Bestiary (10 Enemy Archetypes + Variants):**
   - Dreg (Farmer, High Class, Military, Voltigeur), Shambler, Bloat, Drooler, Pale Lady, Pitchskin, Brute, Waif, Iron Shambler, Iron Dreg.
   - 12 Traps, 36 Status Effects.
7. **Crafting Disciplines (157 Recipes & 32 Gathering Nodes):**
   - Metallurgist, Gunsmith, Cook, Artificer, Outfitter, Physician.

---

## 3. Visual Card Rendering Engines & Standards
1. **Zero Tofu Glyphs:**
   - Absolute ban on unrendered unicode/emoji boxes (`[]`, `[][]`).
   - Use clean ASCII labels or verified icons (`[Secure]`, `[Droppable]`, bullets `•`, arrows `→`).
2. **Title & Header Formatting:**
   - Single clean lines with zero duplication (e.g. `ITEM PROFILE : HEAVY AMMUNITION`, never `HEAVY AMMUNITION (HEAVY AMMUNITION`).
   - All panel headers in Pure English:
     - `MARKET VALUE (CHATEAU TRADERS)`
     - `LOCATION & BEST RAID CONTAINERS`
     - `USAGE FOR QUESTS & CRAFTING`
     - `CRAFTING INGREDIENTS (HUNGER COMPANION)`
     - `EXPEDITION DISCOVERY & HIGH DROP INTEL`
3. **Resale Value vs. Vendor Stock Rework:**
   - The fee number next to Schemas/Skins is the **base resale value** when sold to vendors by a player.
   - Explicitly display: `Base Resale Value : X Copper (Sold to Vendors)`.
   - Never label resale value as "Crafting Fee".
   - If an item is an exclusive drop, clearly state: `Vendor Stock : Not Sold by Merchants (Raid Drop)`.
4. **High-Rate Drop Intel & Clutter Filtering:**
   - Filter out low-rate random container clutter (e.g. `1/9,361 Large Strongbox` or `1/11,646 Brute`).
   - Only surface high drop rates:
     - Mob drops: **Guaranteed or high probability** (e.g. **Dreg Farmer Always 100% Drop** at Garnier's Farm).
     - Placed world loot: **High rate static spawns** (e.g. **Dupo Farrier workshop 1/6.7 [14.9%]** on Sarlat Farm).
     - Hub vendors: **Henri (92 Silver)**.
5. **Pure Blank Maps Rule:**
   - When asked for a blank map (`carte sans indication`, `map de sombre sans rien`), provide the 100% clean, unannotated high-res map without sidebar or POI pins.

---

## 4. Query Routing & Dispatcher Architecture
1. **Priority 1: Dedicated Recipes & Schemas**
   - Queries with `recipe`, `recette`, or matching recipe titles route to `render_recipe_card` and `get_universal_recipe`.
   - Avoids false routing to NPC masters or base weapons.
2. **Priority 2: Specific Skins & Weapon Cosmetics**
   - Specific skin queries (`peasant burden`, `bacchus wand`, `loup`, `basilisk`) match their individual dossiers directly rather than dumping all weapon skins.
   - Weapon skin lists (`skins de la rapier`) dispatch all skins for that specific weapon with clean visual cards.
3. **Priority 3: Hero Abilities & Combat Dossiers**
   - Instant response for `ult`, `passif`, `tactique` across all 6 heroes without confirmation dialogs.
4. **Priority 4: Stash & Inventory Vision Scanning**
   - Generates two synchronized images:
     - Image 1: Highlighting items recommended for liquidation while strictly preserving books, sealed documents, and letters for late-game character XP.
     - Image 2: Clean appraisal manifest with item icons and net profit calculation.
5. **Priority 5: Universal 700-Item Lookup**
   - Any item queried returns a rich item profile card with dual currency resale values and vendor status.
6. **Priority 6: Quests & POI Recon**
   - Accurate quest navigation (e.g. `piro's lens` routes to Rat's Nest Cave `X: 1491.15, Y: 3535.74`, distinct from Piro's Convoy).

---

## 5. Architectural Upgrade Proposal Implementation
1. **Real-Time Dual-Modality Dispatcher:**
   - Decoupled voice emission: voice spoken text is dispatched immediately via streaming TTS while image cards render asynchronously in background threads.
2. **Semantic & Exact Matching Cache:**
   - Normalized multi-word matching with descending length priority and word boundary enforcement (`\b`).
3. **Continuous Automated Verification Loop (`test_suite.py`):**
   - Automated regression testing simulating all past user prompts, verifying text, cards, and spoken audio.
