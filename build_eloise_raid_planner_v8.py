import os, io, base64, json, re
from PIL import Image
import generate_perfect_briefings_v14 as gen

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
HTML_PATH = os.path.join(ART_DIR, "eloise_raid_planner.html")

print("1. Encoding 7 V14 Raid Maps to Base64 (Crisp 1920x1120)...")
raid_maps_b64 = {}
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    im = Image.open(p).resize((1920, 1120), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82, optimize=True)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    raid_maps_b64[i] = f"data:image/jpeg;base64,{b64_str}"
    print(f"  Raid {i}: {len(buf.getvalue())/1024:.1f} KB")

print("2. Encoding Icons to Base64...")
item_icons = [
    'flour', 'charcoal', 'damp_rag', 'saltpetre', 'tallow_balm',
    'china_bowl', 'opium_pipe', 'opium', 'votive_candle', 'silver_key', 'gold_key', 'book_rozier'
]
item_icons_b64 = {}
for name in item_icons:
    p = os.path.join(DOC_DIR, "assets", "items", f"{name}.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            item_icons_b64[name] = f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"

cont_icons = [
    'flour_sack', 'bullion_box', 'wall_cabinet', 'pile_of_ash', 'tooling_bin', 'strongbox', 'oak_barrel', 'ledger_desk'
]
cont_icons_b64 = {}
for name in cont_icons:
    p = os.path.join(DOC_DIR, "assets", "containers", f"{name}.webp")
    if os.path.exists(p):
        with open(p, "rb") as f:
            cont_icons_b64[name] = f"data:image/webp;base64,{base64.b64encode(f.read()).decode('ascii')}"

# Hub Setup (Raid 0)
HUB_CONFIG = {
    "id": 0,
    "phase": "HUB SETUP — ZERO RAIDS",
    "map_name": "Château Outer Ramparts",
    "quest_name": "Quest 1: A Warm Welcome",
    "active_label": "HUB SETUP: SPEAK TO LOUIS, PIRO & REYNAULD",
    "keyBadge": "No Keys Needed",
    "keyColor": "bg-slate-800 text-slate-300 border-slate-700",
    "story_pois": [],
    "active_objectives": [
        {
            "title": "Quest 1: Meet the Encampment Leaders",
            "npc": "Turn in to: Eloise at Château",
            "cont_name": "Louis, Piro, Reynauld (NPCs)",
            "cont_img": "ledger_desk.webp",
            "item_img": "silver_key.png",
            "drop_rate": "100%",
            "density": "3 Hub Leaders",
            "desc": "Speak with Louis (Stashmaster), Piro (Merchant), and Reynauld (Expeditions) to unlock raid expeditions."
        }
    ],
    "priority_focus": {
        "title": "⭐ HUB KEY CHECK: LOUIS VENDOR",
        "item": "Silver / Gold Key",
        "cont": "Louis Shop",
        "c_ico": "bullion_box.webp",
        "i_ico": "silver_key.png",
        "rate": "17.7% / 8.8%",
        "desc": "Buy Silver Key (12s 60c) or Gold Key (25s 60c) whenever Louis has stock."
    },
    "rotation_steps": [
        "1. Walk across the ramparts and speak with Louis (Stashmaster).",
        "2. Speak with Piro near the smoke fire for starter medical supplies.",
        "3. Head up the hill to Reynauld on his high platform to unlock expeditions.",
        "4. Check Louis's vendor shop immediately: Buy Silver Key or Gold Key if stocked!",
        "5. Talk to Eloise again to complete Quest 1 and unlock Quest 2: Making Dough."
    ],
    "directory": [
        {"shape": "diamond", "color": [192, 132, 252], "cont": "Louis Vendor", "c_ico": "bullion_box.webp", "item": "Silver Key", "i_ico": "silver_key.png", "loc": "Outer Ramparts Encampment (12s 60c)", "rate": "17.7%"},
        {"shape": "diamond", "color": [56, 189, 248], "cont": "Louis Vendor", "c_ico": "wall_cabinet.webp", "item": "Gold Key", "i_ico": "gold_key.png", "loc": "Outer Ramparts Encampment (25s 60c)", "rate": "8.8%"},
        {"shape": "circle", "color": [250, 204, 21], "cont": "Piro Vendor", "c_ico": "flour_sack.webp", "item": "Field Meds", "i_ico": "tallow_balm.png", "loc": "Outer Ramparts Leper Physician", "rate": "100%"}
    ],
    "roadmap": [
        {"quest": "Quest 2: Making Dough", "items": [("20x Flour", "flour.png")]},
        {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]}
    ]
}

FULL_RAIDS_DATA = [HUB_CONFIG] + gen.RAIDS_CONFIG

print("3. Building HTML Template...")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>HUNGER Companion — Eloise Fast-Track Raid Planner</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.1); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.15); border-radius: 3px; }}
  </style>
</head>
<body class="bg-[#0e1015] text-[#e2e8f0] font-sans antialiased p-4 md:p-6 min-h-screen">

  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Top Hero Banner -->
    <header class="bg-[#151921] border border-[#262f3d] rounded-2xl p-6 shadow-xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30">Wipe Speedrun</span>
            <span class="text-xs text-[#8e9cae]">Total Required Raids: <strong>7 Dedicated Deployments</strong></span>
          </div>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <span>Eloise Fast-Track Raid Planner</span>
          </h1>
          <p class="text-sm text-[#8e9cae] mt-1">
            Tactical terrain maps with high-focus objectives, container priorities, merchant shortcuts, and key requirements.
          </p>
        </div>

        <!-- Progress Mini Tracker -->
        <div class="flex items-center gap-4 bg-[#0e1015] border border-[#262f3d] rounded-xl p-3 px-4 shrink-0">
          <div class="text-right">
            <div class="text-xs text-[#8e9cae]">Quests Complete</div>
            <div id="stat-quests" class="text-lg font-bold text-amber-400">0 / 8</div>
          </div>
          <div class="h-8 w-px bg-[#262f3d]"></div>
          <div class="text-right">
            <div class="text-xs text-[#8e9cae]">Pre-Farm Stash</div>
            <div id="stat-items" class="text-lg font-bold text-emerald-400">0 / 9 Items</div>
          </div>
        </div>
      </div>

      <!-- Outer Ramparts Starting Merchants Directory (8 Full Hub Merchants) -->
      <div class="mt-4 pt-4 border-t border-[#262f3d] space-y-2">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="font-bold uppercase tracking-wider text-slate-300">Outer Ramparts Encampment Merchants (Pre-Cauldron Hub)</span>
          </div>
          <span class="text-[11px] text-[#8e9cae]">All 8 NPCs available immediately · Restock every raid</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs">
          <!-- Louis -->
          <div class="bg-amber-950/20 border border-amber-800/40 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-amber-300 flex items-center gap-1">🗝️ Louis</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 font-semibold border border-amber-500/30">Keys & Stash</span>
              </div>
              <p class="text-[11px] text-slate-300">
                <strong>Silver Key</strong> (17.7% stock, 12s 60c) & <strong>Gold Key</strong> (8.8% stock, 25s 60c). Also sells Bronze Key, Gunpowder & Screws.
              </p>
            </div>
            <div class="text-[10px] text-amber-400/80 mt-1 italic">★ Check every return to hub!</div>
          </div>

          <!-- Piro -->
          <div class="bg-emerald-950/20 border border-emerald-800/40 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-emerald-300 flex items-center gap-1">🩹 Piro</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30">Leper Physician</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Medical supplies (Robust Antidote, Bloodbags, Ampoules, Lambgut, Feverfew), Bronze Keys, starter armor & ammo.
              </p>
            </div>
            <div class="text-[10px] text-emerald-400/80 mt-1 italic">Primary field meds vendor</div>
          </div>

          <!-- Octave de Villiers -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-cyan-300 flex items-center gap-1">🎒 Octave</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30">Outfitter</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Backpacks (Burlap Haversack, Damp Knapsack, Moist Pouch), Iron Jugs & Pots, Coal Tar, Canvas Patches, Bog Iron, Leather armor.
              </p>
            </div>
            <div class="text-[10px] text-cyan-400/80 mt-1 italic">Inventory & pack upgrades</div>
          </div>

          <!-- Jean Fondeur -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-rose-300 flex items-center gap-1">⚔️ Jean Fondeur</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300 font-semibold border border-rose-500/30">Metallurgy</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Melee weapons (Longsword, Mace, Short Sword, Club, Dagger), Sturdy Axe Handles, Whetstones, Apprentice Materials, Tanned Hides.
              </p>
            </div>
            <div class="text-[10px] text-rose-400/80 mt-1 italic">Melee gear & weapon crafting</div>
          </div>

          <!-- Henriette -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-lime-300 flex items-center gap-1">🌿 Henriette</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-lime-500/20 text-lime-300 font-semibold border border-lime-500/30">Herbalist</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Foraging & Threshing Baskets, fresh herbs (Rosemary, Clove Bud, Lavender, Garlic Bulbs) and essential oils.
              </p>
            </div>
            <div class="text-[10px] text-lime-400/80 mt-1 italic">Baskets & gathering essentials</div>
          </div>

          <!-- Filthy François -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-yellow-300 flex items-center gap-1">⛏️ François</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-yellow-500/20 text-yellow-300 font-semibold border border-yellow-500/30">Miner & Scav</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Copper Ore, Lead Ore, Linen, Burlap, Rusty Buckets, and regional Mining Guides.
              </p>
            </div>
            <div class="text-[10px] text-yellow-400/80 mt-1 italic">Raw minerals & tailoring bases</div>
          </div>

          <!-- Mr Sweet -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-purple-300 flex items-center gap-1">🗺️ Mr Sweet</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-300 font-semibold border border-purple-500/30">Artificer</span>
              </div>
              <p class="text-[11px] text-slate-300">
                In-game Tactical Maps (Sarlat Farm, Jacques Bridge, Sombre Forest Maps), Spindle Pulleys, Latch Hooks, Wine/Mead, Grotesqueries.
              </p>
            </div>
            <div class="text-[10px] text-purple-400/80 mt-1 italic">★ Bribery Target (Sinai Map)</div>
          </div>

          <!-- Reynauld -->
          <div class="bg-slate-900/60 border border-slate-700/60 rounded-xl p-2.5 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-blue-300 flex items-center gap-1">🧭 Reynauld</span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-blue-500/20 text-blue-300 font-semibold border border-blue-500/30">Expeditions</span>
              </div>
              <p class="text-[11px] text-slate-300">
                Unlocks map deployments, expedition timers, extract permits, and regional access routes across the realm.
              </p>
            </div>
            <div class="text-[10px] text-blue-400/80 mt-1 italic">Expedition Gatekeeper</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs: 8 Deployment Phases (True Linear Progression) -->
    <nav class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none text-xs font-semibold">
      <button onclick="selectRaid(0)" id="tab-0" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Hub Setup · Ramparts
      </button>
      <button onclick="selectRaid(1)" id="tab-1" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 1 · Sarlat (Flour)
      </button>
      <button onclick="selectRaid(2)" id="tab-2" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 2 · Bridge (Gavroche Camp)
      </button>
      <button onclick="selectRaid(3)" id="tab-3" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 3 · Sarlat (Charcoal & Recon)
      </button>
      <button onclick="selectRaid(4)" id="tab-4" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 4 · Sarlat (Candle & Contraband)
      </button>
      <button onclick="selectRaid(5)" id="tab-5" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 5 · Sarlat (Sinai Books 1-3)
      </button>
      <button onclick="selectRaid(6)" id="tab-6" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 6 · Bridge (Sinai Books 4-5)
      </button>
      <button onclick="selectRaid(7)" id="tab-7" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white">
        Raid 7 · Forest (Sinai Books 6-7 & Finale)
      </button>
    </nav>

    <!-- Main Dynamic Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- Left Column: Tactical Map Layout & POI Discovery (7 Cols) -->
      <div class="lg:col-span-7 space-y-4">
        <div class="bg-[#151921] border border-[#262f3d] rounded-2xl p-5 shadow-lg flex flex-col">
          <div class="flex items-center justify-between pb-3 border-b border-[#262f3d]">
            <div>
              <span id="map-phase-badge" class="text-xs font-semibold uppercase tracking-wider text-amber-400">PHASE</span>
              <h2 id="map-title" class="text-lg font-bold text-white">Map View</h2>
            </div>
            <div id="map-key-badge" class="px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-800 text-slate-300 border border-slate-700">
              No Keys Needed
            </div>
          </div>

          <!-- Real In-Game Tactical Terrain Map Container -->
          <div class="relative w-full aspect-[16/10] bg-slate-950 rounded-xl my-4 overflow-hidden border border-[#262f3d] shadow-inner flex items-center justify-center group cursor-pointer" onclick="openZoomModal()">
            <!-- Images for Raids 1 to 7 -->
            <img id="map-img-1" class="map-view w-full h-full object-contain" src="{raid_maps_b64[1]}" alt="Raid 1 Map" onerror="this.src='raid1_map.jpg'">
            <img id="map-img-2" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[2]}" alt="Raid 2 Map" onerror="this.src='raid2_map.jpg'">
            <img id="map-img-3" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[3]}" alt="Raid 3 Map" onerror="this.src='raid3_map.jpg'">
            <img id="map-img-4" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[4]}" alt="Raid 4 Map" onerror="this.src='raid4_map.jpg'">
            <img id="map-img-5" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[5]}" alt="Raid 5 Map" onerror="this.src='raid5_map.jpg'">
            <img id="map-img-6" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[6]}" alt="Raid 6 Map" onerror="this.src='raid6_map.jpg'">
            <img id="map-img-7" class="map-view w-full h-full object-contain hidden" src="{raid_maps_b64[7]}" alt="Raid 7 Map" onerror="this.src='raid7_map.jpg'">
            
            <div id="hub-overlay" class="hidden text-center p-6 space-y-2">
              <div class="text-4xl">🏰</div>
              <h3 class="text-lg font-bold text-white">Château Outer Ramparts (Hub Base)</h3>
              <p class="text-xs text-slate-400 max-w-md mx-auto">
                No deployment required. Meet with Louis (Stash), Piro (Meds), and Reynauld (Expeditions).
              </p>
            </div>
            
            <div class="absolute top-3 right-3 bg-slate-900/80 hover:bg-slate-800 text-amber-300 text-xs px-3 py-1.5 rounded-lg border border-amber-500/30 flex items-center gap-1.5 shadow transition-all pointer-events-none">
              <span>🔍</span> Click Infographic for Fullscreen 2400x1400 View
            </div>
          </div>

          <!-- Story POIs & Key Landmarks Bar (Below Map) -->
          <div class="p-3 bg-[#0e121a] border border-[#262f3d] rounded-xl flex items-center justify-between text-xs">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">✦ STORY OBJECTIVE POI</span>
              <span id="hud-poi-text" class="text-slate-300 font-semibold">Discovery Landmark</span>
            </div>
            <div class="flex items-center gap-2 text-slate-400">
              <span class="text-amber-400">💡 Tip:</span> Click map for 2400x1400 fullscreen view
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: THE NEW DE-DUPLICATED 5-BLOCK SIDEBAR (5 Cols) -->
      <div class="lg:col-span-5 space-y-4">

        <!-- BLOCK 1: ACTIVE RAID OBJECTIVES -->
        <div class="bg-[#151921] border border-[#262f3d] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-start justify-between">
            <div>
              <div class="text-[11px] font-bold text-amber-400 uppercase tracking-wider">BLOCK 1 · ACTIVE RAID OBJECTIVE</div>
              <h3 id="brief-quest-name" class="text-base font-bold text-white">Quest Name</h3>
            </div>
            <button onclick="toggleActiveQuestComplete()" id="btn-complete-quest" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition-colors shadow">
              Mark Complete
            </button>
          </div>

          <!-- Dynamic Active Objective Cards -->
          <div id="block1-objective-cards" class="space-y-2.5">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- BLOCK 2: NEXT PRIORITY FOCUS -->
        <div class="bg-[#151921] border border-purple-900/40 rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 id="b2-title" class="text-xs font-bold uppercase tracking-wider text-purple-300 flex items-center gap-1.5">
              <span>⭐</span> NEXT QUEST FOCUS
            </h3>
            <span class="text-[10px] text-purple-400 font-semibold px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/20">Upcoming Priority</span>
          </div>

          <div id="b2-card" class="bg-[#1a1224] border border-purple-600/40 rounded-xl p-3 flex items-start gap-3 text-xs">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- BLOCK 3: TACTICAL PRIORITY EXECUTION STEPS -->
        <div class="bg-[#151921] border border-[#262f3d] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-amber-400">Tactical Priority Steps</h3>
            <span class="text-[11px] text-[#8e9cae]">Objective Priority (Spawn-Independent)</span>
          </div>
          <ol id="tactical-steps" class="space-y-2 text-xs text-slate-300">
            <!-- Rendered by JS with number badges -->
          </ol>
        </div>

        <!-- BLOCK 4: MAP CONTAINER DIRECTORY & DROP ODDS -->
        <div class="bg-[#151921] border border-[#262f3d] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300">Map Container Directory & Odds</h3>
            <span id="dir-map-name" class="text-[11px] text-amber-400 font-semibold">Terrain Directory</span>
          </div>

          <!-- Priority Color Order Legend Bar (Yellow -> Purple -> Blue -> Green -> Grey) -->
          <div class="p-2.5 rounded-lg bg-[#0e121a] border border-[#262f3d] flex flex-wrap items-center gap-3 text-[11px]">
            <span class="flex items-center gap-1 text-amber-400 font-semibold"><span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>● Yellow: Active</span>
            <span class="flex items-center gap-1 text-purple-400 font-semibold"><span class="w-2.5 h-2.5 rotate-45 bg-purple-500"></span>◆ Purple: Prio 2</span>
            <span class="flex items-center gap-1 text-sky-400 font-semibold"><span class="w-2.5 h-2.5 rotate-45 bg-sky-400"></span>◆ Blue: Prio 3</span>
            <span class="flex items-center gap-1 text-emerald-400 font-semibold"><span class="w-2.5 h-2.5 rotate-45 bg-emerald-400"></span>◆ Green: Prio 4</span>
            <span class="flex items-center gap-1 text-slate-400 font-semibold"><span class="w-2.5 h-2.5 rounded-full border border-slate-400"></span>◎ Grey: General</span>
          </div>

          <!-- Dynamic Container List (Big 44x44 Icons, Big Text, No Duplicates!) -->
          <div id="container-directory" class="space-y-2.5 text-xs">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- BLOCK 5: FUTURE STASH PRE-BANKER (CHECKLIST) -->
        <div class="bg-[#151921] border border-[#262f3d] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300">Upcoming Quest Stash Roadmap</h3>
            <span class="text-[11px] text-amber-400">Click to Mark Saved</span>
          </div>
          <div id="stash-checklist" class="grid grid-cols-2 gap-2 text-xs">
            <!-- Interactive Stash Checkboxes -->
          </div>
        </div>

      </div>

    </div>

  </div>

  <!-- Fullscreen Map Lightbox Modal -->
  <div id="zoom-modal" class="hidden fixed inset-0 z-50 bg-black/95 flex flex-col items-center justify-center p-3 backdrop-blur-md" onclick="closeZoomModal()">
    <div class="relative w-full max-w-[96vw] max-h-[94vh] flex flex-col items-center" onclick="event.stopPropagation()">
      <div class="flex items-center justify-between w-full pb-2 text-white px-2">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
          <h3 id="zoom-modal-title" class="font-bold text-sm text-amber-300">Tactical Raid Infographic (2400x1400 All-In-One HUD)</h3>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-xs text-slate-400">Press [ESC] or click outside to dismiss</span>
          <button onclick="closeZoomModal()" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-bold text-white transition-colors border border-slate-600">✕ Close</button>
        </div>
      </div>
      <img id="zoom-modal-img" src="" alt="Zoomed Tactical Map" class="max-h-[86vh] w-auto rounded-xl border border-slate-700 shadow-2xl object-contain">
    </div>
  </div>

  <!-- SCRIPT -->
  <script>
    const RAID_DATA = {json.dumps(FULL_RAIDS_DATA)};

    const EMBEDDED_MAPS = {{
"""
for k, v in raid_maps_b64.items():
    html_content += f'      {k}: "{v}",\n'
html_content += f"""    }};

    const EMBEDDED_ICONS = {{
"""
for k, v in item_icons_b64.items():
    html_content += f'      "{k}": "{v}",\n'
for k, v in cont_icons_b64.items():
    html_content += f'      "{k}": "{v}",\n'
html_content += f"""    }};

    let currentRaidIdx = 1;
    let completedQuests = JSON.parse(localStorage.getItem('hh_completed_quests') || '{{}}');
    let bankedItems = JSON.parse(localStorage.getItem('hh_banked_items') || '{{}}');

    const STASH_ITEMS = [
      {{ id: "flour", name: "20x Flour", quest: "Q2: Making Dough", icon: "flour" }},
      {{ id: "charcoal", name: "15x Charcoal", quest: "Q4: Last Embers", icon: "charcoal" }},
      {{ id: "saltpetre", name: "20x Saltpetre", quest: "Q6: Medical", icon: "saltpetre" }},
      {{ id: "damp_rag", name: "5x Damp Rag", quest: "Q6: Medical", icon: "damp_rag" }},
      {{ id: "tallow_balm", name: "10x Tallow Balm", quest: "Q6: Medical", icon: "tallow_balm" }},
      {{ id: "votive_candle", name: "1x Red Votive Candle", quest: "Q8: Candle", icon: "votive_candle" }},
      {{ id: "opium_pipe", name: "1x Opium Pipe", quest: "Q9: Bribery", icon: "opium_pipe" }},
      {{ id: "china_bowl", name: "1x China Bowl", quest: "Q9: Bribery", icon: "china_bowl" }},
      {{ id: "sinai_books", name: "7x Mount Sinai Books", quest: "Q10: Mount Sinai", icon: "book_rozier" }}
    ];

    function getShapeBadge(shape, colorHex) {{
      if (shape === 'star') return '<span class="text-amber-400 font-bold inline-block shrink-0 text-sm">✦</span>';
      if (shape === 'diamond') return `<span class="w-3.5 h-3.5 rotate-45 rounded-[1px] inline-block shrink-0" style="background-color: ${{colorHex || '#c084fc'}}"></span>`;
      if (shape === 'ring') return '<span class="w-3.5 h-3.5 rounded-full border-2 border-slate-400 inline-block shrink-0"></span>';
      return '<span class="w-3.5 h-3.5 rounded-full bg-amber-400 inline-block shrink-0"></span>';
    }}

    function rgbToHex(rgbArr) {{
      if (!Array.isArray(rgbArr) || rgbArr.length < 3) return '#facc15';
      return '#' + rgbArr.slice(0, 3).map(x => x.toString(16).padStart(2, '0')).join('');
    }}

    function selectRaid(idx) {{
      currentRaidIdx = idx;

      // Update Tabs
      for (let i = 0; i <= 7; i++) {{
        const tab = document.getElementById(`tab-${{i}}`);
        if (tab) {{
          if (i === idx) {{
            tab.className = "raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-amber-500 text-slate-950 font-bold border-amber-400 shadow-md";
          }} else {{
            tab.className = "raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151921] border-[#262f3d] text-[#8e9cae] hover:text-white";
          }}
        }}
      }}

      const data = RAID_DATA[idx];
      document.getElementById('map-phase-badge').textContent = data.phase;
      document.getElementById('map-title').textContent = data.quest_name;
      
      const keyBadge = document.getElementById('map-key-badge');
      if (data.keyBadge) {{
        keyBadge.textContent = data.keyBadge;
        keyBadge.className = `px-2.5 py-1 text-xs font-semibold rounded-md border ${{data.keyColor || 'bg-slate-800 text-slate-300 border-slate-700'}}`;
        keyBadge.classList.remove('hidden');
      }} else {{
        keyBadge.textContent = "No Keys Needed";
        keyBadge.className = "px-2.5 py-1 text-xs font-semibold rounded-md bg-slate-800 text-slate-300 border border-slate-700";
      }}

      // Switch Left Map Image
      const hubOverlay = document.getElementById('hub-overlay');
      for (let i = 1; i <= 7; i++) {{
        const img = document.getElementById(`map-img-${{i}}`);
        if (img) {{
          if (idx === i) {{
            img.classList.remove('hidden');
          }} else {{
            img.classList.add('hidden');
          }}
        }}
      }}
      if (idx === 0) {{
        hubOverlay.classList.remove('hidden');
      }} else {{
        hubOverlay.classList.add('hidden');
      }}

      // Update Story POI Landmark text
      if (data.story_pois && data.story_pois.length > 0) {{
        document.getElementById('hud-poi-text').textContent = data.story_pois.map(p => p.label).join(' • ');
      }} else {{
        document.getElementById('hud-poi-text').textContent = "Standard Resource Gathering & Farmhouse Sweep";
      }}

      // BLOCK 1: Active Objectives
      document.getElementById('brief-quest-name').textContent = data.quest_name;
      const btn = document.getElementById('btn-complete-quest');
      if (completedQuests[idx]) {{
        btn.textContent = "Completed ✓";
        btn.className = "px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-colors shadow";
      }} else {{
        btn.textContent = "Mark Complete";
        btn.className = "px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition-colors shadow";
      }}

      const b1Cards = document.getElementById('block1-objective-cards');
      b1Cards.innerHTML = data.active_objectives.map(o => {{
        const contImg = EMBEDDED_ICONS[o.cont_img ? o.cont_img.replace('.webp', '') : ''] || `assets/containers/${{o.cont_img}}`;
        const itemImg = EMBEDDED_ICONS[o.item_img ? o.item_img.replace('.png', '') : ''] || `assets/items/${{o.item_img}}`;
        return `
          <div class="bg-[#1c1a10] border border-amber-500/40 rounded-xl p-3 flex items-start gap-3">
            <div class="relative w-12 h-12 bg-black/40 border border-amber-500/50 rounded-lg shrink-0 flex items-center justify-center p-1 overflow-hidden">
              <img src="${{contImg}}" alt="" class="w-full h-full object-contain">
              <img src="${{itemImg}}" alt="" class="absolute bottom-0 right-0 w-6 h-6 object-contain drop-shadow">
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-2">
                <h4 class="font-bold text-white text-xs truncate">${{o.title}}</h4>
                <span class="text-xs font-bold text-white shrink-0">${{o.drop_rate}}</span>
              </div>
              <p class="text-[11px] text-amber-300 font-semibold mt-0.5">${{o.density}}</p>
              <p class="text-[11px] text-slate-300 mt-0.5 leading-relaxed">${{o.desc}}</p>
              <p class="text-[11px] text-emerald-400 font-bold mt-1">${{o.npc}}</p>
            </div>
          </div>
        `;
      }}).join('');

      // BLOCK 2: Priority Focus
      const pf = data.priority_focus || {{}};
      document.getElementById('b2-title').innerHTML = `<span>⭐</span> ${{pf.title || 'NEXT QUEST FOCUS'}}`;
      const pfContImg = EMBEDDED_ICONS[pf.c_ico ? pf.c_ico.replace('.webp', '') : ''] || `assets/containers/${{pf.c_ico}}`;
      const pfItemImg = EMBEDDED_ICONS[pf.i_ico ? pf.i_ico.replace('.png', '') : ''] || `assets/items/${{pf.i_ico}}`;
      document.getElementById('b2-card').innerHTML = `
        <div class="relative w-12 h-12 bg-black/40 border border-purple-500/50 rounded-lg shrink-0 flex items-center justify-center p-1 overflow-hidden">
          <img src="${{pfContImg}}" alt="" class="w-full h-full object-contain">
          <img src="${{pfItemImg}}" alt="" class="absolute bottom-0 right-0 w-6 h-6 object-contain drop-shadow">
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between gap-2">
            <h4 class="font-bold text-white text-xs truncate">◆ ${{pf.item || 'Focus Target'}}</h4>
            <span class="text-xs font-bold text-white shrink-0">${{pf.rate || ''}}</span>
          </div>
          <p class="text-[11px] text-purple-300 font-semibold mt-0.5">Container: ${{pf.cont || 'Chest'}}</p>
          <p class="text-[11px] text-slate-300 mt-0.5 leading-relaxed">${{pf.desc || ''}}</p>
        </div>
      `;

      // BLOCK 3: Route Steps (Says WHAT without suggesting WHERE)
      const stepsOl = document.getElementById('tactical-steps');
      stepsOl.innerHTML = data.rotation_steps.map((s, i) => `
        <li class="flex items-start gap-2.5">
          <span class="w-5 h-5 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-[10px] shrink-0 mt-0.5">${{i+1}}</span>
          <span class="leading-relaxed">${{s}}</span>
        </li>
      `).join('');

      // BLOCK 4: Map Container Directory (Big Text, No Duplicates, No Colored % Legend)
      document.getElementById('dir-map-name').textContent = `${{data.map_name}} Directory`;
      const dirDiv = document.getElementById('container-directory');
      dirDiv.innerHTML = data.directory.map(itm => {{
        const contImg = EMBEDDED_ICONS[itm.c_ico ? itm.c_ico.replace('.webp', '') : ''] || `assets/containers/${{itm.c_ico}}`;
        const itemImg = EMBEDDED_ICONS[itm.i_ico ? itm.i_ico.replace('.png', '') : ''] || `assets/items/${{itm.i_ico}}`;
        const colorHex = rgbToHex(itm.color);
        return `
          <div class="bg-[#0e121a] border border-[#262f3d] rounded-xl p-3 flex items-center justify-between gap-3 hover:border-slate-600 transition-colors">
            <div class="flex items-center gap-3 min-w-0">
              ${{getShapeBadge(itm.shape, colorHex)}}
              <div class="w-9 h-9 rounded bg-slate-900 border border-slate-700 flex items-center justify-center p-0.5 shrink-0">
                <img src="${{contImg}}" alt="" class="w-full h-full object-contain">
              </div>
              <div class="w-9 h-9 rounded bg-slate-900 border border-slate-700 flex items-center justify-center p-0.5 shrink-0">
                <img src="${{itemImg}}" alt="" class="w-full h-full object-contain">
              </div>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">${{itm.cont}} ➔ ${{itm.item}}</div>
                <div class="text-[11px] text-slate-400 truncate">${{itm.loc}}</div>
              </div>
            </div>
            <span class="text-xs font-bold text-white shrink-0 px-2.5 py-1 rounded bg-slate-800 border border-slate-700">${{itm.rate}}</span>
          </div>
        `;
      }}).join('');

      updateStats();
    }}

    function renderChecklist() {{
      const container = document.getElementById('stash-checklist');
      container.innerHTML = STASH_ITEMS.map(item => {{
        const isChecked = bankedItems[item.id] || false;
        const iconSrc = EMBEDDED_ICONS[item.icon] || `assets/items/${{item.icon}}.png`;
        return `
          <label class="flex items-center gap-2 p-2 rounded-xl border transition-all cursor-pointer ${{
            isChecked ? 'bg-emerald-950/20 border-emerald-600/40 text-emerald-300' : 'bg-[#0e121a] border-[#262f3d] text-slate-300 hover:border-slate-600'
          }}">
            <input type="checkbox" onchange="toggleStashItem('${{item.id}}')" ${{isChecked ? 'checked' : ''}} class="rounded bg-slate-900 border-slate-700 text-emerald-500 focus:ring-0">
            <img src="${{iconSrc}}" class="w-6 h-6 object-contain shrink-0" alt="">
            <div class="truncate">
              <div class="font-bold text-[11px] leading-tight truncate">${{item.name}}</div>
              <div class="text-[10px] text-slate-500 truncate">${{item.quest}}</div>
            </div>
          </label>
        `;
      }}).join('');
    }}

    function toggleStashItem(id) {{
      bankedItems[id] = !bankedItems[id];
      localStorage.setItem('hh_banked_items', JSON.stringify(bankedItems));
      renderChecklist();
      updateStats();
    }}

    function toggleActiveQuestComplete() {{
      completedQuests[currentRaidIdx] = !completedQuests[currentRaidIdx];
      localStorage.setItem('hh_completed_quests', JSON.stringify(completedQuests));
      selectRaid(currentRaidIdx);
    }}

    function updateStats() {{
      const questsDone = Object.values(completedQuests).filter(Boolean).length;
      document.getElementById('stat-quests').textContent = `${{questsDone}} / 8`;
      const itemsDone = Object.values(bankedItems).filter(Boolean).length;
      document.getElementById('stat-items').textContent = `${{itemsDone}} / ${{STASH_ITEMS.length}} Items`;
    }}

    function openZoomModal() {{
      if (currentRaidIdx === 0) return;
      const modalImg = document.getElementById('zoom-modal-img');
      modalImg.src = EMBEDDED_MAPS[currentRaidIdx] || `raid${{currentRaidIdx}}_map.jpg`;
      document.getElementById('zoom-modal-title').textContent = `${{RAID_DATA[currentRaidIdx].phase}} — ${{RAID_DATA[currentRaidIdx].quest_name}}`;
      document.getElementById('zoom-modal').classList.remove('hidden');
    }}

    function closeZoomModal() {{
      document.getElementById('zoom-modal').classList.add('hidden');
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeZoomModal();
    }});

    // Initialize
    selectRaid(1);
    renderChecklist();
    updateStats();
  </script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SUCCESS: Generated {HTML_PATH} ({os.path.getsize(HTML_PATH)/1024/1024:.2f} MB)")
