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

target_items = [
    'heavy_ammunition', 'longboy', 'seamstress_needle', 'sealed_bloodbag', 'thick_branch',
    'tavern_wine', 'thin_mead', 'saltpetre', 'tallow_balm', 'bezoar', 'hartshorn', 'fresh_egg',
    'flour', 'charcoal', 'damp_rag', 'china_bowl', 'opium', 'opium_pipe', 'arsenic', 'glass_vial', 'silver_dish',
    'dreg_head', 'waif_head', 'shambler_hand', 'bloat_spine', 'brute_foot', 'drooler_jaw'
]
items_b64 = {item: b64_img(ITEM_DIR, f"{item}.png") for item in target_items}

target_conts = [
    'flour_sack', 'pile_of_ash', 'tooling_bin', 'wall_cabinet', 'physician_bag',
    'jacques_medicinals', 'strongbox'
]
conts_b64 = {cont: b64_img(CONT_DIR, f"{cont}.webp") for cont in target_conts}

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
  <title>HUNGER Companion // Main Quest Item & Merchant Directory</title>
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

  <!-- TOP HEADER BAR (CLEAN) -->
  <header class="border-b border-[#e5c07b]/40 bg-[#12120f] px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-2xl">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded border border-[#e5c07b]/50 bg-[#1c1c18] flex items-center justify-center font-cinzel text-lg text-[#e5c07b] font-bold">
        ⚔
      </div>
      <h1 class="text-xl md:text-2xl font-bold font-cinzel text-[#e5c07b] tracking-wide">
        HUNGER COMPANION // MAIN QUEST ITEM & MERCHANT DIRECTORY
      </h1>
    </div>

    <!-- Badges -->
    <div class="flex items-center gap-3">
      <div class="px-3 py-1.5 rounded-md border border-emerald-500/40 bg-emerald-950/30 text-emerald-300 text-xs font-bold">
        ✔ 12 Buyable Items
      </div>
      <div class="px-3 py-1.5 rounded-md border border-red-500/40 bg-red-950/30 text-red-300 text-xs font-bold">
        ✖ 15 Loot Only Items
      </div>
      <a href="eloise_raid_planner.html" class="px-3 py-1.5 rounded-md border border-[#504837] bg-[#1c1c18] hover:border-[#e5c07b] text-[#e5c07b] text-xs font-semibold transition">
        🗺 Eloise Planner
      </a>
    </div>
  </header>

  <!-- MAIN VIEW CONTAINER -->
  <main class="flex-1 p-6 max-w-[2560px] mx-auto w-full flex flex-col gap-6">

    <!-- MASTER IMAGE DISPLAY -->
    <div class="rounded-xl border border-[#302c24] bg-[#12120f] overflow-hidden shadow-2xl">
      <div class="p-2 bg-[#0b0b09] overflow-x-auto custom-scroll">
        <img src="{guide_img_b64}" alt="Merchant Logistics Guide" class="w-full h-auto rounded border border-[#2d2921] shadow-2xl min-w-[1200px]">
      </div>
    </div>

    <!-- 5-COLUMN DIRECTORY: YELLOW, PURPLE, BLUE, GREEN, GREY -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">

      <!-- COL 1: YELLOW -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#1c1c15] px-4 py-3 border-b-2 border-[#facc15]">
          <h2 class="text-sm font-cinzel font-bold text-[#facc15]">1. PRIORITY YELLOW</h2>
          <p class="text-[11px] text-[#a8a091] mt-0.5 font-medium">PRIMARY OBJECTIVES & CORE GEAR</p>
        </div>
        <div class="p-3 flex flex-col gap-2.5">
          <!-- Flour -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['flour']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['flour_sack']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Flour</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">20x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Flour Sacks (Sarlat Farm)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Making Dough (Eloise)</p>
            </div>
          </div>

          <!-- Heavy Ammo -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['heavy_ammunition']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Heavy Ammunition</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">10x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#facc15] truncate mt-1">Vendor: Reynauld / Piro</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Bearing Arms (Reynauld)</p>
            </div>
          </div>

          <!-- Longboy -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['longboy']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Longboy Weapon</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#facc15] truncate mt-1">Vendor: Piro / Reynauld</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: A Long Boy (Mr Sweet)</p>
            </div>
          </div>

          <!-- Thick Branch -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['thick_branch']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Thick Branch</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">2x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#facc15] truncate mt-1">Vendor: Reynauld (Outer Ramparts)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Child's Play (Louis)</p>
            </div>
          </div>

          <!-- Fresh Egg -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['fresh_egg']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Fresh Egg</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">5x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#facc15] truncate mt-1">Vendor: Grillard (Cauldron)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Gardon's Gambit (Louis)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 2: PURPLE -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#1c1c15] px-4 py-3 border-b-2 border-[#c084fc]">
          <h2 class="text-sm font-cinzel font-bold text-[#c084fc]">2. PRIORITY PURPLE</h2>
          <p class="text-[11px] text-[#a8a091] mt-0.5 font-medium">HEARTHS & ALCHEMICAL REAGENTS</p>
        </div>
        <div class="p-3 flex flex-col gap-2.5">
          <!-- Charcoal -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['charcoal']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['pile_of_ash']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Charcoal</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">15x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Piles of Ash (Manor Hearths)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Last Embers (Eloise)</p>
            </div>
          </div>

          <!-- Silver Dish -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['silver_dish']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['strongbox']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Silver Dish</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Strongboxes (Officers' Desks)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Bezoar -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['bezoar']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Bezoar</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">3x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#c084fc] truncate mt-1">Vendor: Doctor Moreau (Cauldron)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <!-- Hartshorn -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['hartshorn']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Hartshorn</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">2x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#c084fc] truncate mt-1">Vendor: Doctor Moreau (Cauldron)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <!-- Seamstress Needle -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['seamstress_needle']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Seamstress Needle</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">5x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#c084fc] truncate mt-1">Vendor: Octave de Villiers</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Under the Skin (Piro)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 3: BLUE -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#1c1c15] px-4 py-3 border-b-2 border-[#38bdf8]">
          <h2 class="text-sm font-cinzel font-bold text-[#38bdf8]">3. PRIORITY BLUE</h2>
          <p class="text-[11px] text-[#a8a091] mt-0.5 font-medium">APOTHECARY & CLINIC REAGENTS</p>
        </div>
        <div class="p-3 flex flex-col gap-2.5">
          <!-- Saltpetre -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['saltpetre']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Saltpetre</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">20x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#38bdf8] truncate mt-1">Vendor: Doctor Moreau (Cauldron)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Tallow Balm -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['tallow_balm']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Tallow Balm</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">10x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#38bdf8] truncate mt-1">Vendor: Doctor Moreau (Cauldron)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Sealed Bloodbag -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['sealed_bloodbag']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Sealed Bloodbag</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#38bdf8] truncate mt-1">Vendor: Piro / Dr. Moreau</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Damp Rag -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['damp_rag']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['tooling_bin']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Damp Rag</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">5x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Tooling Bins / Desks</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Glass Vial -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['glass_vial']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Glass Vial</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Physician Bags (Clinics)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Arsenic -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['arsenic']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['jacques_medicinals']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Arsenic</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Jacques Medicinals</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 4: GREEN -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#1c1c15] px-4 py-3 border-b-2 border-[#4ade80]">
          <h2 class="text-sm font-cinzel font-bold text-[#4ade80]">4. PRIORITY GREEN</h2>
          <p class="text-[11px] text-[#a8a091] mt-0.5 font-medium">CONTRABAND & TAVERN GOODS</p>
        </div>
        <div class="p-3 flex flex-col gap-2.5">
          <!-- China Bowl -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['china_bowl']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">China Bowl</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Wall Cabinets (Château)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Opium Pipe -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium_pipe']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Opium Pipe</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Wall Cabinets / Desks</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Opium -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-9 h-9 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Opium</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#a8a091] truncate mt-1">Source: Physician Bags (Hospitals)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Tavern Wine -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['tavern_wine']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Tavern Wine</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">3x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#4ade80] truncate mt-1">Vendor: Mr Sweet (Outer Ramparts)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>

          <!-- Thin Mead -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['thin_mead']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Thin Mead</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">3x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-500/40 mt-1">✔ BUYABLE</span>
              <p class="text-[11px] text-[#4ade80] truncate mt-1">Vendor: Mr Sweet (Outer Ramparts)</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>
        </div>
      </div>

      <!-- COL 5: GREY -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#1c1c15] px-4 py-3 border-b-2 border-[#94a3b8]">
          <h2 class="text-sm font-cinzel font-bold text-[#94a3b8]">5. PRIORITY GREY</h2>
          <p class="text-[11px] text-[#a8a091] mt-0.5 font-medium">BESTIARY CREATURE TROPHIES</p>
        </div>
        <div class="p-3 flex flex-col gap-2.5">
          <!-- Dreg Head -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['dreg_head']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Dreg Head</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">10x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Common Dregs</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>

          <!-- Waif Head -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['waif_head']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Waif Head</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">10x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Lurking Waifs</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>

          <!-- Shambler Hand -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['shambler_hand']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Shambler Hand</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">5x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Heavy Shamblers</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>

          <!-- Bloat Spine -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['bloat_spine']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Bloat Spine</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">5x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Volatile Bloats</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>

          <!-- Brute Foot -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['brute_foot']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Brute Foot</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Armored Brutes</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>

          <!-- Drooler Jaw -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded p-2.5 flex gap-2.5 items-center">
            <img src="{items_b64['drooler_jaw']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-1">
                <span class="text-xs font-bold text-[#f0ebe0] truncate">Drooler Jaw</span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">1x</span>
              </div>
              <span class="inline-block text-[10px] font-bold px-1.5 py-0.2 rounded bg-red-950/60 text-red-300 border border-red-500/40 mt-1">✖ CANNOT BUY</span>
              <p class="text-[11px] text-[#94a3b8] truncate mt-1">Harvest: Acidic Droolers</p>
              <p class="text-[11px] text-[#e5c07b] truncate">Quest: Tissue and Blood (Piro)</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </main>
</body>
</html>
"""

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
        print(f"Saved Clean HTML: {p}")
    except Exception as e:
        print(f"Error saving HTML {p}: {e}")
