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
  <title>HUNGER Logistics // Main Quest Item & Merchant Directory</title>
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
  <header class="border-b border-[#e5c07b]/40 bg-[#12120f] px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-2xl">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded border border-[#e5c07b]/50 bg-[#1c1c18] flex items-center justify-center font-cinzel text-lg text-[#e5c07b] font-bold">
        ⚔
      </div>
      <h1 class="text-xl md:text-2xl font-bold font-cinzel text-[#e5c07b] tracking-wide">
        HUNGER COMPANION // MAIN QUEST ITEM & MERCHANT RECON
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

    <!-- MASTER HIGH-RES GRAPHIC EMBED -->
    <div class="rounded-xl border border-[#302c24] bg-[#12120f] overflow-hidden shadow-2xl">
      <div class="p-2 bg-[#0b0b09] overflow-x-auto custom-scroll">
        <img src="{guide_img_b64}" alt="Merchant Logistics Guide" class="w-full h-auto rounded border border-[#2d2921] shadow-2xl min-w-[1200px]">
      </div>
    </div>

    <!-- 2 MAIN ORGANIZED SECTIONS -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- SECTION 1: BUYABLE ITEMS -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#18241c] px-5 py-3.5 border-b-2 border-emerald-500 flex justify-between items-center">
          <div>
            <h2 class="text-base font-cinzel font-bold text-emerald-300 flex items-center gap-2">
              <span>✔</span> 1. BUYABLE FROM MERCHANTS (12 ITEMS)
            </h2>
            <p class="text-xs text-[#a8a091] mt-0.5">Check vendor stocks on each hub reset • Stock chances shown per item</p>
          </div>
          <span class="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/40">12 Items</span>
        </div>

        <div class="p-4 flex flex-col gap-3">

          <!-- Heavy Ammo -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['heavy_ammunition']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Heavy Ammunition</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">10x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#facc15] border border-[#facc15]/40 flex-shrink-0">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Reynauld / Piro • Location: Outer Ramparts (~2c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Bearing Arms (Reynauld)</p>
            </div>
          </div>

          <!-- Thick Branch -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['thick_branch']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Thick Branch</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">2x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#facc15] border border-[#facc15]/40 flex-shrink-0">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Reynauld • Location: Outer Ramparts (~18c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Child's Play (Louis)</p>
            </div>
          </div>

          <!-- Tavern Wine -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['tavern_wine']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Tavern Wine</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">3x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#facc15] border border-[#facc15]/40 flex-shrink-0">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Mr Sweet • Location: Outer Ramparts (~18c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>

          <!-- Thin Mead -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['thin_mead']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Thin Mead</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">3x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#facc15] border border-[#facc15]/40 flex-shrink-0">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Mr Sweet • Location: Outer Ramparts (~11c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>

          <!-- Seamstress Needle -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['seamstress_needle']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Seamstress Needle</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">5x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#c084fc] border border-[#c084fc]/40 flex-shrink-0">Stock: 85% (High Chance)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Octave de Villiers • Location: Outer Ramparts (~15c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Fresh Egg -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['fresh_egg']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Fresh Egg</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">5x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#c084fc] border border-[#c084fc]/40 flex-shrink-0">Stock: 80% (High Chance)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Grillard • Location: The Cauldron (~16c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Gardon's Gambit (Louis)</p>
            </div>
          </div>

          <!-- Saltpetre -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['saltpetre']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Saltpetre</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">20x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#c084fc] border border-[#c084fc]/40 flex-shrink-0">Stock: 75% (High Chance)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Doctor Lucien Moreau • Location: The Cauldron (~3c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Tallow Balm -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['tallow_balm']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Tallow Balm</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">10x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#c084fc] border border-[#c084fc]/40 flex-shrink-0">Stock: 70% (High Chance)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Doctor Lucien Moreau • Location: The Cauldron (~6c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Sealed Bloodbag -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['sealed_bloodbag']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Sealed Bloodbag</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">1x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#38bdf8] border border-[#38bdf8]/40 flex-shrink-0">Stock: 55% (Moderate)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Piro / Doctor Moreau • Location: Hub / Cauldron (~5s 31c)</p>
              <p class="text-xs text-[#a8a091]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Hartshorn -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['hartshorn']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Hartshorn</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">2x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#38bdf8] border border-[#38bdf8]/40 flex-shrink-0">Stock: 45% (Moderate)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Doctor Lucien Moreau • Location: The Cauldron (~1s 10c)</p>
              <p class="text-xs text-[#a8a091]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <!-- Longboy -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['longboy']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Longboy Weapon</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">1x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#4ade80] border border-[#4ade80]/40 flex-shrink-0">Stock: 35% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Piro / Reynauld • Location: Outer Ramparts (~1s 31c)</p>
              <p class="text-xs text-[#a8a091]">Required For: A Long Boy (Mr Sweet)</p>
            </div>
          </div>

          <!-- Bezoar -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['bezoar']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <div class="flex items-center gap-2 truncate">
                  <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Bezoar</span>
                  <span class="text-xs font-bold px-1.5 py-0.2 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">3x</span>
                </div>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-[#4ade80] border border-[#4ade80]/40 flex-shrink-0">Stock: 35% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Doctor Lucien Moreau • Location: The Cauldron (~15c each)</p>
              <p class="text-xs text-[#a8a091]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

        </div>
      </div>

      <!-- SECTION 2: CANNOT BUY / LOOT ONLY -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#241818] px-5 py-3.5 border-b-2 border-red-500 flex justify-between items-center">
          <div>
            <h2 class="text-base font-cinzel font-bold text-red-300 flex items-center gap-2">
              <span>✖</span> 2. CANNOT BUY FROM MERCHANTS (15 ITEMS)
            </h2>
            <p class="text-xs text-[#a8a091] mt-0.5">Never sold by merchants • Must target container nodes or harvest from elites</p>
          </div>
          <span class="text-xs font-mono font-bold text-red-400 bg-red-950/60 px-2.5 py-1 rounded border border-red-500/40">15 Items</span>
        </div>

        <div class="p-4 flex flex-col gap-3">

          <!-- Charcoal -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['charcoal']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['pile_of_ash']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Charcoal (15x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#c084fc] border border-[#c084fc]/40">Drop Rate: 52.6% (Pile of Ash)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Piles of Ash / Old Stoves (Manor Hearths)</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Last Embers (Eloise)</p>
            </div>
          </div>

          <!-- Flour -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['flour']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['flour_sack']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Flour (20x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#facc15] border border-[#facc15]/40">Drop Rate: 47.6% (Flour Sack)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Flour Sacks (Granaries / Sarlat Farm)</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Making Dough (Eloise)</p>
            </div>
          </div>

          <!-- Opium -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#c084fc] border border-[#c084fc]/40">Drop Rate: 47.6% (Medicinals)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Jacques Medicinals (Field Hospitals)</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Damp Rag -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['damp_rag']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['tooling_bin']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Damp Rag (5x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#38bdf8] border border-[#38bdf8]/40">Drop Rate: 23.8% (Grave / Bin)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Stone Graves / Tooling Bins / Desks</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <!-- Silver Dish -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['silver_dish']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['strongbox']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Silver Dish (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#38bdf8] border border-[#38bdf8]/40">Drop Rate: 23.8% (Cabinet / Box)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Wall Cabinets / Locked Strongboxes</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Glass Vial -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['glass_vial']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Glass Vial (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#38bdf8] border border-[#38bdf8]/40">Drop Rate: 20.4% (Physician Kit)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Physician's Cabinets / Clinics</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- China Bowl -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['china_bowl']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">China Bowl (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#4ade80] border border-[#4ade80]/40">Drop Rate: 16.1% (Wall Cabinet)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Wall Cabinets (Château Upper Villas)</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Opium Pipe -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium_pipe']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium Pipe (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#4ade80] border border-[#4ade80]/40">Drop Rate: 13.7% (Bullion Box)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Bullion Boxes / Jewellery Boxes (Manor Desks)</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- Arsenic -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-2.5 flex gap-2.5 items-center hover:bg-[#1d1d18] transition">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['arsenic']}" class="w-12 h-12 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['jacques_medicinals']}" class="w-8 h-8 object-contain bg-[#1c1c18] rounded p-1 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Arsenic (1x)</span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-red-950/80 text-[#4ade80] border border-[#4ade80]/40">Drop Rate: 10.6% (Medicinals)</span>
              </div>
              <p class="text-xs text-[#f0ebe0] mt-0.5">Target: Jacques Medicinals / Laboratory Jars</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <!-- CREATURE TROPHIES -->
          <div class="pt-2 border-t border-[#2d2921] mt-1">
            <p class="text-xs uppercase font-bold text-[#94a3b8] tracking-wider mb-2 font-cinzel">Creature Trophies (100% Harvest on Kill)</p>
            
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['dreg_head']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Dreg Head (10x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Common Dregs (All Maps)</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['waif_head']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Waif Head (10x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Lurking Waifs (Ruins)</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['shambler_hand']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Shambler Hand (5x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Heavy Shamblers (Roads)</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['bloat_spine']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Bloat Spine (5x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Volatile Bloats (Range Kill)</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['brute_foot']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Brute Foot (1x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Armored Brutes (Fortress)</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-2 flex items-center gap-2">
                <img src="{items_b64['drooler_jaw']}" class="w-9 h-9 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0]">Drooler Jaw (1x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Acidic Droolers (Canals)</div>
                </div>
              </div>
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
        print(f"Saved HTML: {p}")
    except Exception as e:
        print(f"Error saving HTML {p}: {e}")
