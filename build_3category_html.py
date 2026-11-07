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
      background: #12120e;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #2a2820;
      border-radius: 3px;
    }}
    .custom-scroll::-webkit-scrollbar-thumb:hover {{
      background: #c5a059;
    }}
  </style>
</head>
<body class="p-6 md:p-10 max-w-7xl mx-auto custom-scroll">

  <!-- Header -->
  <header class="border-b border-[#2d2921] pb-6 mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
    <div>
      <div class="flex items-center gap-3">
        <span class="text-xs font-bold tracking-widest uppercase px-2.5 py-1 rounded bg-[#c5a059]/10 text-[#c5a059] border border-[#c5a059]/30">HUNGER // Official Field Manual</span>
        <span class="text-xs tracking-wider text-[#a8a29e]">STANDARD MAIN QUESTS (48 TOTAL)</span>
      </div>
      <h1 class="text-3xl md:text-4xl font-black font-cinzel text-[#f0ebe0] mt-2 tracking-wide">MAIN QUEST PROCUREMENT & LOGISTICS</h1>
      <p class="text-sm text-[#a8a29e] mt-1 max-w-3xl">
        Strict progression audit of all 27 functional quest items across standard main quests. Divided into three clear progression phases: Cauldron Access Items, Outer Ramparts Buyables, and Post-Access / Side Quest Loot.
      </p>
    </div>
    <div class="flex items-center gap-3 bg-[#151512] px-4 py-3 rounded border border-[#2d2921] text-xs">
      <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[#fbbf24]"></span> Yellow (&lt;15%)</div>
      <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[#c084fc]"></span> Purple (15-35%)</div>
      <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[#38bdf8]"></span> Blue (40-60%)</div>
      <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[#4ade80]"></span> Green (70-85%)</div>
      <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-[#9ca3af]"></span> Grey (100%)</div>
    </div>
  </header>

  <!-- Big Graphic Display -->
  <div class="mb-10 rounded border border-[#2d2921] bg-[#12120e] p-2 overflow-hidden shadow-2xl">
    <div class="text-[11px] font-bold tracking-widest text-[#a8a29e] uppercase px-3 py-1 flex justify-between items-center bg-[#181814] border-b border-[#2d2921] mb-2 rounded-t">
      <span>HIGH-RESOLUTION VISUAL GUIDE (2560x1440)</span>
      <span class="text-[#c5a059]">3-COLUMN PROGRESSION ARCHITECTURE</span>
    </div>
    <img src="{guide_img_b64}" alt="Hunger Quest Item Logistics Guide" class="w-full h-auto rounded border border-[#22221c]">
  </div>

  <!-- 3-Column Directory -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

    <!-- COLUMN 1: ITEMS TO REACH CAULDRON -->
    <div class="bg-[#12120e] border border-[#2d2921] rounded p-5 flex flex-col gap-4">
      <div class="border-b border-[#2d2921] pb-3">
        <div class="flex justify-between items-center">
          <span class="text-xs font-bold font-cinzel tracking-wider text-[#f87171]">PHASE 1 // GATEWAY REQUIREMENTS</span>
          <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-[#f87171]/20 text-[#f87171] border border-[#f87171]/40">8 Items</span>
        </div>
        <h2 class="text-xl font-bold font-cinzel text-[#f0ebe0] mt-1">ITEMS TO REACH CAULDRON</h2>
        <p class="text-xs text-[#a8a29e] mt-1">Eloise's Questline & Mr Sweet's Bribery. Required <b>BEFORE</b> Crossing The Threshold unlocks The Cauldron hub. Cannot be purchased when needed.</p>
      </div>

      <div class="flex flex-col gap-2.5">

        <!-- YELLOW (<15%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#fbbf24] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['tallow_balm']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Tallow Balm (10x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#fbbf24]/20 text-[#fbbf24] border border-[#fbbf24]/40">9.1% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Bare Necessities (Eloise)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#fbbf24] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['opium_pipe']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium Pipe (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#fbbf24]/20 text-[#fbbf24] border border-[#fbbf24]/40">13.7% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Bullion Box / Jewellery Box</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: A Touch of Bribery (Mr Sweet)</p>
          </div>
        </div>

        <!-- PURPLE (15-35%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['china_bowl']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">China Bowl (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">16.1% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Wall Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: A Touch of Bribery (Mr Sweet)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['saltpetre']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Saltpetre (20x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">18.9% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Tooling Bin</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Bare Necessities (Eloise)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['damp_rag']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Damp Rag (5x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">23.8% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Stone Grave / Tooling Bin</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Bare Necessities (Eloise)</p>
          </div>
        </div>

        <!-- BLUE (40-60%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['flour']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Flour (20x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">47.6% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Flour Sack</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Making Dough (Eloise)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['opium']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Opium (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">47.6% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Jacques Medicinals</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: A Touch of Bribery (Mr Sweet)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['charcoal']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Charcoal (15x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">52.6% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Pile of Ash / Old Stove</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Last Embers (Eloise)</p>
          </div>
        </div>

      </div>
    </div>

    <!-- COLUMN 2: BUYABLE FROM MERCHANTS -->
    <div class="bg-[#12120e] border border-[#2d2921] rounded p-5 flex flex-col gap-4">
      <div class="border-b border-[#2d2921] pb-3">
        <div class="flex justify-between items-center">
          <span class="text-xs font-bold font-cinzel tracking-wider text-[#4ade80]">OUTER RAMPARTS HUB ONLY</span>
          <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">5 Items</span>
        </div>
        <h2 class="text-xl font-bold font-cinzel text-[#f0ebe0] mt-1">BUYABLE FROM MERCHANTS</h2>
        <p class="text-xs text-[#a8a29e] mt-1">Available immediately in base hub. Can be purchased directly when quests are active. Ranked by stock spawn chance.</p>
      </div>

      <div class="flex flex-col gap-2.5">

        <!-- PURPLE (35%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['longboy']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Longboy Weapon (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">35.0% Stock</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Merchant: Piro / Reynauld</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: A Long Boy (Piro)</p>
          </div>
        </div>

        <!-- BLUE (55%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['sealed_bloodbag']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Sealed Bloodbag (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">55.0% Stock</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Merchant: Piro</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Under the Skin (Octave de Villiers)</p>
          </div>
        </div>

        <!-- GREEN (85%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['seamstress_needle']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Seamstress Needle (5x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">85.0% Stock</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Merchant: Octave de Villiers</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Under the Skin (Octave de Villiers)</p>
          </div>
        </div>

        <!-- GREY (100%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#9ca3af] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['heavy_ammunition']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Heavy Ammunition (10x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#9ca3af]/20 text-[#9ca3af] border border-[#9ca3af]/40">100% Stock</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Merchant: Reynauld / Piro</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Bearing Arms (Reynauld)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#9ca3af] border border-[#2d2921] rounded p-2.5 flex gap-3 items-center">
          <img src="{items_b64['thick_branch']}" class="w-11 h-11 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Thick Branch (2x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#9ca3af]/20 text-[#9ca3af] border border-[#9ca3af]/40">100% Stock</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Merchant: Reynauld</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Child's Play (Reynauld)</p>
          </div>
        </div>

      </div>
    </div>

    <!-- COLUMN 3: OTHER SIDE QUESTS - LOOT ONLY -->
    <div class="bg-[#12120e] border border-[#2d2921] rounded p-5 flex flex-col gap-4">
      <div class="border-b border-[#2d2921] pb-3">
        <div class="flex justify-between items-center">
          <span class="text-xs font-bold font-cinzel tracking-wider text-[#a8a29e]">POST-ACCESS / RAID LOOT ONLY</span>
          <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-[#9ca3af]/20 text-[#9ca3af] border border-[#9ca3af]/40">14 Items</span>
        </div>
        <h2 class="text-xl font-bold font-cinzel text-[#f0ebe0] mt-1">OTHER SIDE QUESTS // LOOT</h2>
        <p class="text-xs text-[#a8a29e] mt-1">Quests from side vendors. Either never sold, or sold inside Cauldron after the quest is already issued.</p>
      </div>

      <div class="flex flex-col gap-2.5">

        <!-- YELLOW (<15%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#fbbf24] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['arsenic']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Arsenic (2x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#fbbf24]/20 text-[#fbbf24] border border-[#fbbf24]/40">10.6% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Medicine Cabinet / Strongbox</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: The Rats of Ypres (Doctor Moreau)</p>
          </div>
        </div>

        <!-- PURPLE (15-35%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['glass_vial']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Glass Vial (5x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">20.4% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Tooling Bin / Medicine Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Spring Water / Tissue (Doctor Moreau)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['silver_dish']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Silver Dish (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">23.8% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Jewellery Box / Wall Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: An Appetite for Silver (Reynauld)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#c084fc] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['bezoar']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Bezoar (1x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#c084fc]/20 text-[#c084fc] border border-[#c084fc]/40">35.0% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Of Blight & Bezoars (Piro)</p>
          </div>
        </div>

        <!-- BLUE (40-60%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['hartshorn']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Hartshorn (2x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">45.0% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Physician's Cabinet</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Of Blight & Bezoars (Piro)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['tavern_wine']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Tavern Wine (3x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">55.0% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Oak Barrel / Cellar Shelf</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Sweet Lubrication (Mr Sweet)</p>
          </div>
        </div>

        <div class="bg-[#181814] border-l-4 border-l-[#38bdf8] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['thin_mead']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Thin Mead (3x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#38bdf8]/20 text-[#38bdf8] border border-[#38bdf8]/40">55.0% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Oak Barrel / Cellar Shelf</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: Sweet Lubrication (Mr Sweet)</p>
          </div>
        </div>

        <!-- GREEN (70-85%) -->
        <div class="bg-[#181814] border-l-4 border-l-[#4ade80] border border-[#2d2921] rounded p-2 flex gap-2.5 items-center">
          <img src="{items_b64['fresh_egg']}" class="w-10 h-10 object-contain bg-[#22221c] rounded p-1 border border-[#3d382c]">
          <div class="min-w-0 flex-1">
            <div class="flex justify-between items-center gap-2">
              <span class="text-xs font-bold font-cinzel text-[#f0ebe0]">Fresh Egg (12x)</span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-[#4ade80]/20 text-[#4ade80] border border-[#4ade80]/40">70.0% Drop</span>
            </div>
            <p class="text-xs text-[#f0ebe0]">Container: Basket / Kitchen Pantry</p>
            <p class="text-[11px] text-[#e5c07b]">Quest: How Do You Like Your Eggs? (Doctor Moreau)</p>
          </div>
        </div>

        <!-- GREY (100% Creature Trophies) -->
        <div class="mt-2 pt-2 border-t border-[#2d2921]">
          <div class="text-[10px] font-bold tracking-widest text-[#9ca3af] uppercase mb-1.5">CREATURE TROPHIES (100% DROPS FROM TARGET ENEMY)</div>
          <div class="grid grid-cols-2 gap-2">
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['dreg_head']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Dreg Head (3x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Dreg</span>
              </div>
            </div>
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['waif_head']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Waif Head (3x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Waif</span>
              </div>
            </div>
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['shambler_hand']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Shambler Hand (3x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Shambler</span>
              </div>
            </div>
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['bloat_spine']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Bloat Spine (1x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Bloat</span>
              </div>
            </div>
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['brute_foot']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Brute Foot (1x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Brute</span>
              </div>
            </div>
            <div class="bg-[#181814] border-l-2 border-l-[#9ca3af] border border-[#2d2921] rounded p-1.5 flex gap-2 items-center">
              <img src="{items_b64['drooler_jaw']}" class="w-8 h-8 object-contain bg-[#22221c] rounded p-0.5">
              <div class="min-w-0">
                <span class="text-[11px] font-bold font-cinzel block truncate">Drooler Jaw (1x)</span>
                <span class="text-[10px] text-[#a8a29e] block">Enemy: Drooler</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>

</body>
</html>
"""

desktop_html = os.path.join(DESKTOP_DIR, "merchant_procurement_guide.html")
art_html = os.path.join(ART_DIR, "merchant_procurement_guide.html")

with open(desktop_html, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(art_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated HTML saved to:\n  - {desktop_html}\n  - {art_html}")
