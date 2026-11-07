import os, base64

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\31f232ba-f37d-4331-8fda-d6f94602b088"
DESKTOP_DIR = r"C:\Users\PC\Desktop\Hunger_Raid_Maps"

ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")

def b64_img(folder, filename):
    p = os.path.join(folder, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            ext = filename.split('.')[-1]
            mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"
    return ""

# Encode all needed icons
items_b64 = {}
target_items = [
    'heavy_ammunition', 'longboy', 'seamstress_needle', 'sealed_bloodbag', 'thick_branch',
    'tavern_wine', 'thin_mead', 'saltpetre', 'tallow_balm', 'bezoar', 'hartshorn', 'fresh_egg',
    'flour', 'charcoal', 'damp_rag', 'china_bowl', 'opium', 'opium_pipe', 'arsenic', 'glass_vial', 'silver_dish',
    'dreg_head', 'waif_head', 'shambler_hand', 'bloat_spine', 'brute_foot', 'drooler_jaw'
]
for item in target_items:
    items_b64[item] = b64_img(ITEM_DIR, f"{item}.png")

conts_b64 = {}
target_conts = [
    'flour_sack', 'pile_of_ash', 'tooling_bin', 'wall_cabinet', 'physician_bag',
    'jacques_medicinals', 'strongbox', 'bullion_box'
]
for cont in target_conts:
    conts_b64[cont] = b64_img(CONT_DIR, f"{cont}.webp")

# Read guide image as b64
guide_img_b64 = ""
guide_img_path = os.path.join(DOC_DIR, "merchant_quest_items_guide.png")
if os.path.exists(guide_img_path):
    with open(guide_img_path, "rb") as f:
        guide_img_b64 = f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HUNGER Logistics - Merchant Procurement & Quest Item Directory</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0b0b09;
      color: #f0ebe0;
    }}
    .font-cinzel {{
      font-family: 'Cinzel', Georgia, serif;
    }}
    .custom-scroll::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scroll::-webkit-scrollbar-track {{
      background: #12120f;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #2d2921;
      border-radius: 3px;
    }}
    .custom-scroll::-webkit-scrollbar-thumb:hover {{
      background: #4b4434;
    }}
  </style>
</head>
<body class="min-h-screen bg-[#0b0b09] text-[#f0ebe0] flex flex-col">

  <!-- TOP HEADER BAR -->
  <header class="border-b border-[#e5c07b]/40 bg-[#12120f] px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-2xl backdrop-blur-md">
    <div class="flex items-center gap-4">
      <div class="w-10 h-10 rounded border border-[#e5c07b]/50 bg-[#1c1c18] flex items-center justify-center font-cinzel text-xl text-[#e5c07b] font-bold shadow-inner">
        ⚔
      </div>
      <div>
        <h1 class="text-xl md:text-2xl font-bold font-cinzel text-[#e5c07b] tracking-wide flex items-center gap-3">
          HUNGER COMPANION // LOGISTICS
          <span class="text-xs font-sans px-2.5 py-0.5 rounded border border-[#302c24] bg-[#1c1c18] text-[#a8a091] font-medium tracking-normal">
            48 Main Quests
          </span>
        </h1>
        <p class="text-xs text-[#a8a091] tracking-wider uppercase font-medium mt-0.5">
          Speedrun Recon & Vendor Inventory Directory • Excludes Unique Collectibles
        </p>
      </div>
    </div>

    <!-- Badges & Action -->
    <div class="flex items-center gap-3">
      <div class="px-3 py-1.5 rounded-md border border-emerald-500/40 bg-emerald-950/30 text-emerald-400 text-xs font-bold flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        12 Buyable at Merchants
      </div>
      <div class="px-3 py-1.5 rounded-md border border-red-500/40 bg-red-950/30 text-red-400 text-xs font-bold flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-red-400"></span>
        15 Raid Loot Only
      </div>
      <a href="eloise_raid_planner.html" class="px-3.5 py-1.5 rounded-md border border-[#504837] bg-[#1c1c18] hover:bg-[#252520] hover:border-[#e5c07b] text-[#e5c07b] text-xs font-semibold transition flex items-center gap-1.5">
        🗺 Open Eloise Planner
      </a>
    </div>
  </header>

  <!-- FILTER CONTROLS -->
  <div class="bg-[#151512] border-b border-[#2d2921] px-6 py-3 flex flex-wrap items-center justify-between gap-4">
    <div class="flex flex-wrap items-center gap-2" id="filter-buttons">
      <button onclick="setFilter('all')" id="btn-all" class="px-3 py-1 rounded text-xs font-semibold bg-[#e5c07b] text-black transition">
        All 27 Items
      </button>
      <button onclick="setFilter('buyable')" id="btn-buyable" class="px-3 py-1 rounded text-xs font-semibold border border-emerald-500/40 bg-emerald-950/20 text-emerald-400 hover:bg-emerald-900/30 transition">
        ✔ Buyable Only (12)
      </button>
      <button onclick="setFilter('loot')" id="btn-loot" class="px-3 py-1 rounded text-xs font-semibold border border-red-500/40 bg-red-950/20 text-red-400 hover:bg-red-900/30 transition">
        ✖ Loot Only (15)
      </button>
      <button onclick="setFilter('outer')" id="btn-outer" class="px-3 py-1 rounded text-xs font-semibold border border-yellow-500/40 bg-yellow-950/20 text-yellow-400 hover:bg-yellow-900/30 transition">
        Outer Ramparts Hub (7)
      </button>
      <button onclick="setFilter('cauldron')" id="btn-cauldron" class="px-3 py-1 rounded text-xs font-semibold border border-sky-500/40 bg-sky-950/20 text-sky-400 hover:bg-sky-900/30 transition">
        Cauldron Hub (5)
      </button>
    </div>

    <!-- Search input -->
    <div class="relative w-72">
      <input type="text" id="search-input" oninput="filterCards()" placeholder="Filter items, vendors, or quests..." 
             class="w-full bg-[#1c1c18] border border-[#302c24] focus:border-[#e5c07b] rounded px-3 py-1.5 text-xs text-[#f0ebe0] placeholder-[#7d7669] outline-none transition">
      <span class="absolute right-2.5 top-2 text-[#7d7669] text-xs">🔍</span>
    </div>
  </div>

  <!-- MAIN VIEW CONTAINER -->
  <main class="flex-1 p-6 max-w-[1920px] mx-auto w-full flex flex-col gap-8">

    <!-- HIGH RES GRAPHICAL BRIEFING EMBED -->
    <div class="rounded-xl border border-[#302c24] bg-[#12120f] overflow-hidden shadow-2xl">
      <div class="bg-[#181814] px-5 py-3 border-b border-[#2d2921] flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-xs uppercase tracking-widest font-bold text-[#e5c07b] font-cinzel">High-Resolution Tactical Infographic</span>
          <span class="text-[11px] text-[#7d7669]">• Ultra-Wide 2560x1440 Master Layout</span>
        </div>
        <div class="flex items-center gap-3">
          <a href="merchant_quest_items_guide.png" download class="text-xs text-[#e5c07b] hover:underline flex items-center gap-1">
            📥 Download Full Image (PNG)
          </a>
        </div>
      </div>
      <div class="p-2 bg-[#0b0b09] overflow-x-auto custom-scroll">
        <img src="{guide_img_b64}" alt="Merchant Logistics Guide" class="w-full h-auto rounded border border-[#2d2921] shadow-2xl max-w-none min-w-[1200px]">
      </div>
    </div>

    <!-- CARDS DIRECTORY & SPEEDRUN LIST -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- COL 1: BUYABLE ITEMS -->
      <div class="flex flex-col gap-4">
        <div class="border-b-2 border-emerald-500 pb-2 flex items-center justify-between">
          <h2 class="text-base font-cinzel font-bold text-emerald-400 flex items-center gap-2">
            <span>✔</span> 1. BUYABLE AT MERCHANTS
          </h2>
          <span class="text-xs text-[#a8a091] font-mono">12 Items</span>
        </div>

        <div class="flex flex-col gap-3" id="col-buyable">
          <!-- Outer Ramparts Subheading -->
          <div class="text-[11px] uppercase tracking-wider font-bold text-yellow-400/90 pt-1 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-yellow-400"></span>
            Outer Ramparts Encampment (Starting Hub)
          </div>

          <!-- Heavy Ammo -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['heavy_ammunition']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">10x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Heavy Ammunition</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Bearing Arms (Reynauld)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Reynauld / Piro <span class="text-[#7d7669]">(~2c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Reynauld gives this quest and sells the required ammo right at his stall.</p>
            </div>
          </div>

          <!-- Longboy -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['longboy']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">1x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Longboy Weapon</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: A Long Boy (Mr Sweet)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Piro / Reynauld <span class="text-[#7d7669]">(~1s 31c)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Buying directly bypasses tedious weapon crate searches in dangerous zones.</p>
            </div>
          </div>

          <!-- Seamstress Needle -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['seamstress_needle']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">5x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Seamstress Needle</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Under the Skin (Piro)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Octave de Villiers <span class="text-[#7d7669]">(~15c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Octave's tailoring stall in the Outer Ramparts stocks these regularly.</p>
            </div>
          </div>

          <!-- Sealed Bloodbag -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['sealed_bloodbag']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">1x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Sealed Bloodbag</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Under the Skin (Piro)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Piro / Dr. Moreau <span class="text-[#7d7669]">(~5s 31c)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Piro sells blood supplies right beside his smoke fire.</p>
            </div>
          </div>

          <!-- Thick Branch -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['thick_branch']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">2x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Thick Branch</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Child's Play (Louis)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Reynauld <span class="text-[#7d7669]">(~18c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Raw timber sold by Reynauld; instant hand-in for Louis.</p>
            </div>
          </div>

          <!-- Tavern Wine & Thin Mead -->
          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['tavern_wine']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">3x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Tavern Wine</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Sweet Lubrication (Mr Sweet)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Mr Sweet <span class="text-[#7d7669]">(~18c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Sold directly in Mr Sweet's own tavern supply rotation.</p>
            </div>
          </div>

          <div class="item-card buyable outer bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['thin_mead']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">3x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Thin Mead</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Sweet Lubrication (Mr Sweet)</p>
              <p class="text-xs text-yellow-400 font-medium mt-1">Vendor: Mr Sweet <span class="text-[#7d7669]">(~11c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Cheap fermented beverage sold directly at the hub bar.</p>
            </div>
          </div>

          <!-- Cauldron Subheading -->
          <div class="text-[11px] uppercase tracking-wider font-bold text-sky-400/90 pt-3 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
            The Cauldron (Deep Hub Progression)
          </div>

          <!-- Saltpetre -->
          <div class="item-card buyable cauldron bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-sky-500/40 flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['saltpetre']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">20x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Saltpetre</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Bare Necessities (Eloise)</p>
              <p class="text-xs text-sky-400 font-medium mt-1">Vendor: Doctor Lucien Moreau <span class="text-[#7d7669]">(~3c each)</span></p>
              <p class="text-[11px] text-yellow-300 mt-1 line-clamp-2 font-medium">⚡ HIGH PRIORITY: 20x takes hours to loot. Dr. Moreau clears this instantly.</p>
            </div>
          </div>

          <!-- Tallow Balm -->
          <div class="item-card buyable cauldron bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-sky-500/40 flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['tallow_balm']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">10x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Tallow Balm</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Bare Necessities (Eloise)</p>
              <p class="text-xs text-sky-400 font-medium mt-1">Vendor: Doctor Lucien Moreau <span class="text-[#7d7669]">(~6c each)</span></p>
              <p class="text-[11px] text-yellow-300 mt-1 line-clamp-2 font-medium">⚡ HIGH PRIORITY: Stock up at Moreau to finish Eloise's main objectives.</p>
            </div>
          </div>

          <!-- Bezoar -->
          <div class="item-card buyable cauldron bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['bezoar']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">3x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Bezoar</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Of Blight and Bezoars (Piro)</p>
              <p class="text-xs text-sky-400 font-medium mt-1">Vendor: Doctor Lucien Moreau <span class="text-[#7d7669]">(~15c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Rare alchemical drop in raids; buy from Dr. Moreau's clinic.</p>
            </div>
          </div>

          <!-- Hartshorn -->
          <div class="item-card buyable cauldron bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['hartshorn']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">2x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Hartshorn</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Of Blight and Bezoars (Piro)</p>
              <p class="text-xs text-sky-400 font-medium mt-1">Vendor: Doctor Lucien Moreau <span class="text-[#7d7669]">(~1s 10c)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Medical reagent exclusively stocked at Moreau's apothecary.</p>
            </div>
          </div>

          <!-- Fresh Egg -->
          <div class="item-card buyable cauldron bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-emerald-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['fresh_egg']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-emerald-950 border border-emerald-500 text-emerald-300 text-[10px] font-bold rounded">5x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Fresh Egg</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/40 text-emerald-400">BUYABLE</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Gardon's Gambit (Louis)</p>
              <p class="text-xs text-sky-400 font-medium mt-1">Vendor: Grillard <span class="text-[#7d7669]">(~16c each)</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Sold by Cauldron cook Grillard; saves searching farmhouse pantries.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 2: LOOT ONLY CONTAINERS -->
      <div class="flex flex-col gap-4">
        <div class="border-b-2 border-red-500 pb-2 flex items-center justify-between">
          <h2 class="text-base font-cinzel font-bold text-red-400 flex items-center gap-2">
            <span>✖</span> 2. LOOT ONLY: CONTAINERS
          </h2>
          <span class="text-xs text-[#a8a091] font-mono">9 Items</span>
        </div>

        <div class="flex flex-col gap-3" id="col-containers">
          <div class="text-[11px] uppercase tracking-wider font-bold text-[#e5c07b] pt-1 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-[#e5c07b]"></span>
            Target Container Nodes & High-Yield Spawns
          </div>

          <!-- Flour -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['flour']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">20x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Flour Sack">
                <img src="{conts_b64['flour_sack']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Flour</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Making Dough (Eloise)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Flour Sacks <span class="text-[#7d7669]">• Château & Sarlat</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">47.6% drop rate in granaries. Collect over 2-3 speedrun rotations.</p>
            </div>
          </div>

          <!-- Charcoal -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['charcoal']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">15x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Pile of Ash">
                <img src="{conts_b64['pile_of_ash']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Charcoal</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Last Embers (Eloise)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Piles of Ash <span class="text-[#7d7669]">• Manor Hearths</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">52.6% drop rate. Search hearth grates and burnt stoves in manor ruins.</p>
            </div>
          </div>

          <!-- Damp Rag -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['damp_rag']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">5x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Tooling Bin">
                <img src="{conts_b64['tooling_bin']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Damp Rag</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Bare Necessities (Eloise)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Tooling Bins / Desks <span class="text-[#7d7669]">• Workshops</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">High spawn rate in mechanical bins. The only Bare Necessities item needing raids!</p>
            </div>
          </div>

          <!-- China Bowl -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['china_bowl']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Wall Cabinet">
                <img src="{conts_b64['wall_cabinet']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">China Bowl</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: A Touch of Bribery (Mr Sweet)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Wall Cabinets <span class="text-[#7d7669]">• Château Interior</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Search residential dining cabinets on the 2nd floor of intact villas.</p>
            </div>
          </div>

          <!-- Opium & Opium Pipe -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['opium']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Physician Bag">
                <img src="{conts_b64['physician_bag']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Opium</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: A Touch of Bribery (Mr Sweet)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Physician Bags <span class="text-[#7d7669]">• Field Hospitals</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Apothecary bags and field hospital ruins near infirmary tents.</p>
            </div>
          </div>

          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['opium_pipe']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Wall Cabinet">
                <img src="{conts_b64['wall_cabinet']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Opium Pipe</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: A Touch of Bribery (Mr Sweet)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Wall Cabinets / Desks <span class="text-[#7d7669]">• Manors</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Often paired near China Bowl spots in wealthy bedroom furnishings.</p>
            </div>
          </div>

          <!-- Arsenic, Glass Vial, Silver Dish -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['arsenic']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Jacques Medicinals">
                <img src="{conts_b64['jacques_medicinals']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Arsenic</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Of Blight and Bezoars (Piro)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Jacques Medicinals <span class="text-[#7d7669]">• Infirmaries</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Toxic reagent jar found on laboratory benches and drug kits.</p>
            </div>
          </div>

          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['glass_vial']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Physician Bag">
                <img src="{conts_b64['physician_bag']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Glass Vial</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Under the Skin (Piro)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Physician Bags <span class="text-[#7d7669]">• Clinics</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Common medical glass container found inside doctor satchels.</p>
            </div>
          </div>

          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-red-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="flex gap-1.5 flex-shrink-0 items-center">
              <div class="w-13 h-13 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex items-center justify-center p-1.5 relative">
                <img src="{items_b64['silver_dish']}" class="w-full h-full object-contain">
                <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-red-950 border border-red-500 text-red-300 text-[10px] font-bold rounded">1x</span>
              </div>
              <div class="w-10 h-10 rounded-md bg-[#181814] border border-[#302c24] flex items-center justify-center p-1" title="Target Container: Strongbox">
                <img src="{conts_b64['strongbox']}" class="w-full h-full object-contain opacity-80">
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Silver Dish</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-950/60 border border-red-500/40 text-red-400">LOOT ONLY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Under the Skin (Piro)</p>
              <p class="text-xs text-[#f0ebe0] font-medium mt-1">Target: Strongboxes / Desks <span class="text-[#7d7669]">• Officers</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">High-tier bullion furniture. Requires a Silver Key to open locked cases.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 3: CREATURE TROPHIES & PROCUREMENT INTEL -->
      <div class="flex flex-col gap-4">
        <div class="border-b-2 border-purple-500 pb-2 flex items-center justify-between">
          <h2 class="text-base font-cinzel font-bold text-purple-400 flex items-center gap-2">
            <span>☣</span> 3. CREATURE TROPHY HARVESTS
          </h2>
          <span class="text-xs text-[#a8a091] font-mono">6 Items</span>
        </div>

        <div class="flex flex-col gap-3" id="col-trophies">
          <div class="text-[11px] uppercase tracking-wider font-bold text-purple-400 pt-1 flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
            Tissue & Blood Bestiary Objectives (Piro)
          </div>

          <!-- Dreg Head -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['dreg_head']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">10x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Dreg Head</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Common Dregs <span class="text-[#7d7669]">• All Maps</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Standard roaming infected. Headshot kills guarantee head harvest.</p>
            </div>
          </div>

          <!-- Waif Head -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['waif_head']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">10x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Waif Head</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Lurking Waifs <span class="text-[#7d7669]">• Ruins & Roofs</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Agile ambushers. Listen for clicking sounds; harvest heads upon kill.</p>
            </div>
          </div>

          <!-- Shambler Hand -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['shambler_hand']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">5x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Shambler Hand</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Heavy Shamblers <span class="text-[#7d7669]">• Main Roads</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Bulky high-health infected. Aim for exposed arm joints to sever hand.</p>
            </div>
          </div>

          <!-- Bloat Spine -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['bloat_spine']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">5x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Bloat Spine</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Volatile Bloats <span class="text-[#7d7669]">• Marshes</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Snipe from extreme distance; self-detonation destroys the spine!</p>
            </div>
          </div>

          <!-- Brute Foot & Drooler Jaw -->
          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['brute_foot']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">1x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Brute Foot</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Armored Brutes <span class="text-[#7d7669]">• Fortress Gates</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Massive apex elite. Stagger with explosives and finish leg joints.</p>
            </div>
          </div>

          <div class="item-card loot bg-[#151512] hover:bg-[#1a1a16] border border-[#2d2921] hover:border-purple-500/60 rounded-lg p-3 transition flex gap-3 shadow-md">
            <div class="w-14 h-14 rounded-md bg-[#1f1f1a] border border-[#3d382c] flex-shrink-0 flex items-center justify-center p-1.5 relative">
              <img src="{items_b64['drooler_jaw']}" class="w-full h-full object-contain">
              <span class="absolute -bottom-1.5 -right-1 px-1.5 py-0.2 bg-purple-950 border border-purple-500 text-purple-300 text-[10px] font-bold rounded">1x</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-sm font-bold font-cinzel text-[#f0ebe0] truncate">Drooler Jaw</h3>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-purple-950/60 border border-purple-500/40 text-purple-400">TROPHY</span>
              </div>
              <p class="text-xs text-[#e5c07b] truncate mt-0.5">Quest: Tissue and Blood (Piro)</p>
              <p class="text-xs text-purple-300 font-medium mt-1">Source: Acidic Droolers <span class="text-[#7d7669]">• Waterways</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 line-clamp-2">Bait out of water channels before killing so the jaw can be harvested.</p>
            </div>
          </div>

          <!-- TACTICAL SPEEDRUN BRIEFING PANEL -->
          <div class="rounded-lg border border-[#504837] bg-[#1a1a15] p-4 flex flex-col gap-2 shadow-inner mt-2">
            <div class="text-xs uppercase tracking-wider font-bold text-[#e5c07b] font-cinzel flex items-center gap-2">
              ⚡ Speedrun Procurement Strategy
            </div>
            <ul class="text-xs space-y-2 text-[#a8a091] mt-1">
              <li class="flex items-start gap-2">
                <span class="text-yellow-400 font-bold">1.</span>
                <span><b class="text-[#f0ebe0]">Check Louis Every Reset:</b> Buy Silver Key (12s 60c) and Gold Key (25s 60c) immediately to loot locked Château strongrooms.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-yellow-400 font-bold">2.</span>
                <span><b class="text-[#f0ebe0]">Pre-Buy Saltpetre & Balm:</b> Never farm 20x Saltpetre manually. Visit Doctor Lucien Moreau in Cauldron to instantly complete Eloise's *Bare Necessities*.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-yellow-400 font-bold">3.</span>
                <span><b class="text-[#f0ebe0]">Skip Longboy Searching:</b> Buy from Piro or Reynauld for ~1s 31c to clear Mr Sweet's weapon delivery task.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- JAVASCRIPT FILTER SCRIPT -->
  <script>
    let currentFilter = 'all';

    function setFilter(filter) {{
      currentFilter = filter;
      document.querySelectorAll('#filter-buttons button').forEach(b => {{
        b.className = 'px-3 py-1 rounded text-xs font-semibold border border-[#302c24] bg-[#1c1c18] text-[#a8a091] hover:bg-[#252520] transition';
      }});
      const activeBtn = document.getElementById('btn-' + filter);
      if (activeBtn) {{
        activeBtn.className = 'px-3 py-1 rounded text-xs font-semibold bg-[#e5c07b] text-black transition';
      }}
      filterCards();
    }}

    function filterCards() {{
      const query = document.getElementById('search-input').value.toLowerCase();
      const cards = document.querySelectorAll('.item-card');

      cards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        const matchesQuery = text.includes(query);

        let matchesFilter = true;
        if (currentFilter === 'buyable') {{
          matchesFilter = card.classList.contains('buyable');
        }} else if (currentFilter === 'loot') {{
          matchesFilter = card.classList.contains('loot');
        }} else if (currentFilter === 'outer') {{
          matchesFilter = card.classList.contains('outer');
        }} else if (currentFilter === 'cauldron') {{
          matchesFilter = card.classList.contains('cauldron');
        }}

        if (matchesQuery && matchesFilter) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""

# Write HTML file to both destinations
out_html_paths = [
    os.path.join(ART_DIR, "merchant_procurement_guide.html"),
    os.path.join(DESKTOP_DIR, "merchant_procurement_guide.html"),
    os.path.join(DOC_DIR, "Raid_Maps", "merchant_procurement_guide.html")
]

for p in out_html_paths:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved HTML: {p}")
    except Exception as e:
        print(f"Error saving HTML {p}: {e}")
