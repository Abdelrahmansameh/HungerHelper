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
    'jacques_medicinals', 'strongbox', 'oak_barrel', 'basket'
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
        ✔ 5 Buyable Items
      </div>
      <div class="px-3 py-1.5 rounded-md border border-red-500/40 bg-red-950/30 text-red-300 text-xs font-bold">
        ✖ 22 Loot Only Items
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

      <!-- SECTION 1: BUYABLE ITEMS (5 ITEMS) -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#18241c] px-5 py-3.5 border-b-2 border-emerald-500 flex justify-between items-center">
          <div>
            <h2 class="text-base font-cinzel font-bold text-emerald-300 flex items-center gap-2">
              <span>✔</span> 1. BUYABLE FROM MERCHANTS (5 ITEMS)
            </h2>
            <p class="text-xs text-[#a8a091] mt-0.5">Vendors unlocked and stocking items when their respective quests are active</p>
          </div>
          <span class="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/40">5 Items</span>
        </div>

        <div class="p-4 flex flex-col gap-3">

          <!-- Longboy (35% - Purple) -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['longboy']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Longboy Weapon (1x)</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Stock: 35% (Rare)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Piro / Reynauld • Outer Ramparts Hub</p>
              <p class="text-xs text-[#a8a091]">Required For: A Long Boy (Mr Sweet)</p>
            </div>
          </div>

          <!-- Sealed Bloodbag (55% - Blue) -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['sealed_bloodbag']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Sealed Bloodbag (1x)</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Stock: 55% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Piro (Smoke Fire) • Outer Ramparts Hub</p>
              <p class="text-xs text-[#a8a091]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Seamstress Needle (85% - Green) -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['seamstress_needle']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Seamstress Needle (5x)</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">Stock: 85% (Common)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Octave de Villiers • Outer Ramparts Hub</p>
              <p class="text-xs text-[#a8a091]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <!-- Heavy Ammo (100% - Grey) -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['heavy_ammunition']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Heavy Ammunition (10x)</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Reynauld / Piro • Outer Ramparts Hub</p>
              <p class="text-xs text-[#a8a091]">Required For: Bearing Arms (Reynauld)</p>
            </div>
          </div>

          <!-- Thick Branch (100% - Grey) -->
          <div class="bg-[#181814] border-l-4 border-l-[#94a3b8] border border-[#2d2921] rounded-lg p-3 flex gap-3 items-center hover:bg-[#1d1d18] transition">
            <img src="{items_b64['thick_branch']}" class="w-13 h-13 object-contain bg-[#22221c] rounded p-1.5 border border-[#3d382c] flex-shrink-0">
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-sm font-bold font-cinzel text-[#f0ebe0]">Thick Branch (2x)</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-[#94a3b8]/20 text-[#94a3b8] border border-[#94a3b8]/40">Stock: 100% (Guaranteed)</span>
              </div>
              <p class="text-xs text-[#e5c07b] font-medium mt-1">Merchant: Reynauld • Outer Ramparts Hub</p>
              <p class="text-xs text-[#a8a091]">Required For: Child's Play (Louis)</p>
            </div>
          </div>

          <!-- Progression Note -->
          <div class="rounded-lg border border-[#3d382c] bg-[#1a1a15] p-3 text-xs text-[#a8a091] space-y-1 mt-2">
            <div class="font-bold text-[#e5c07b] uppercase font-cinzel">Progression Check Details</div>
            <p>• Items sold in The Cauldron (Saltpetre, Tallow Balm, Fresh Eggs, Bezoars, Hartshorn) are for quests received <i>before</i> the Cauldron is accessible.</p>
            <p>• Mr Sweet asks for Tavern Wine & Thin Mead to open his tavern, so they cannot be purchased beforehand.</p>
          </div>

        </div>
      </div>

      <!-- SECTION 2: CANNOT BUY / LOOT ONLY (22 ITEMS) -->
      <div class="bg-[#12120f] border border-[#2d2921] rounded-lg overflow-hidden flex flex-col shadow-lg">
        <div class="bg-[#241818] px-5 py-3.5 border-b-2 border-red-500 flex justify-between items-center">
          <div>
            <h2 class="text-base font-cinzel font-bold text-red-300 flex items-center gap-2">
              <span>✖</span> 2. CANNOT BUY FROM MERCHANTS (22 ITEMS)
            </h2>
            <p class="text-xs text-[#a8a091] mt-0.5">Container type only • Strictly ordered Yellow (rarest) to Grey (guaranteed)</p>
          </div>
          <span class="text-xs font-mono font-bold text-red-400 bg-red-950/60 px-2.5 py-1 rounded border border-red-500/40">22 Items</span>
        </div>

        <div class="p-4 flex flex-col gap-2">

          <!-- YELLOW (Rarest < 15%) -->
          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['tallow_balm']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Tallow Balm (10x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">Drop: 9.1% (Rarest)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['arsenic']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['jacques_medicinals']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Arsenic (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">Drop: 10.6% (Rarest)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Jacques Medicinals</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#facc15] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium_pipe']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium Pipe (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#facc15]/20 text-[#facc15] border border-[#facc15]/40">Drop: 13.7% (Rarest)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Bullion Box / Jewellery Box</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <!-- PURPLE (Rare 15% - 35%) -->
          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['china_bowl']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['wall_cabinet']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">China Bowl (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 16.1% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Wall Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['saltpetre']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['tooling_bin']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Saltpetre (20x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 18.9% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Tooling Bin</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['glass_vial']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Glass Vial (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 20.4% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['silver_dish']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['strongbox']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Silver Dish (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 23.8% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Strongbox / Wall Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Under the Skin (Piro)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['damp_rag']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['tooling_bin']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Damp Rag (5x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 23.8% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Stone Grave / Tooling Bin</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Bare Necessities (Eloise)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['bezoar']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Bezoar (3x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">Drop: 35.0% (Rare)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <!-- BLUE (Uncommon 40% - 60%) -->
          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['hartshorn']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Hartshorn (2x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 45.0% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Of Blight & Bezoars (Piro)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['flour']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['flour_sack']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Flour (20x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 47.6% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Flour Sack</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Making Dough (Eloise)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['opium']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['physician_bag']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium (1x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 47.6% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Jacques Medicinals</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: A Touch of Bribery (Mr Sweet)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['charcoal']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['pile_of_ash']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Charcoal (15x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 52.6% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Pile of Ash / Old Stove</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Last Embers (Eloise)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['tavern_wine']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['oak_barrel']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Tavern Wine (3x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 55.0% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Oak Barrel / Cellar Shelf</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>

          <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['thin_mead']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['oak_barrel']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Thin Mead (3x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">Drop: 55.0% (Uncommon)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Oak Barrel / Cellar Shelf</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Sweet Lubrication (Mr Sweet)</p>
            </div>
          </div>

          <!-- GREEN (Common 70% - 85%) -->
          <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
            <div class="flex gap-1 flex-shrink-0">
              <img src="{items_b64['fresh_egg']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
              <img src="{conts_b64['basket']}" class="w-7 h-7 object-contain bg-[#1c1c18] rounded p-0.5 self-center opacity-80 border border-[#2d2921]">
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex justify-between items-center gap-2">
                <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Fresh Egg (5x)</span>
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">Drop: 70.0% (Common)</span>
              </div>
              <p class="text-xs text-[#f0ebe0]">Container: Basket / Pantry Crate</p>
              <p class="text-[11px] text-[#e5c07b]">Required For: Gardon's Gambit (Louis)</p>
            </div>
          </div>

          <!-- GREY (100% Guaranteed Creature Trophies) -->
          <div class="pt-1.5 border-t border-[#2d2921]">
            <p class="text-[11px] uppercase font-bold text-[#94a3b8] tracking-wider mb-1.5 font-cinzel">Creature Trophies (100% Harvest on Kill)</p>
            
            <div class="grid grid-cols-2 gap-1.5 text-xs">
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['dreg_head']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Dreg Head (10x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Common Dreg</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['waif_head']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Waif Head (10x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Lurking Waif</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['shambler_hand']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Shambler Hand (5x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Heavy Shambler</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['bloat_spine']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Bloat Spine (5x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Volatile Bloat</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['brute_foot']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Brute Foot (1x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Armored Brute</div>
                </div>
              </div>
              <div class="bg-[#181814] border border-[#2d2921] rounded p-1.5 flex items-center gap-2">
                <img src="{items_b64['drooler_jaw']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5 border border-[#3d382c]">
                <div class="truncate">
                  <div class="font-bold text-[#f0ebe0] text-[11px]">Drooler Jaw (1x)</div>
                  <div class="text-[10px] text-[#94a3b8]">Enemy: Acidic Drooler</div>
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
