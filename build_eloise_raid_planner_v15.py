import os, io, base64, json, re
from PIL import Image
import generate_perfect_briefings_v21 as gen

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
HTML_PATH = os.path.join(ART_DIR, "eloise_raid_planner.html")

print("1. Encoding 7 V21 Raid Maps to Base64 (Crisp 1920x1120)...")
raid_maps_b64 = {}
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    im = Image.open(p).resize((1920, 1120), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82, optimize=True)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    raid_maps_b64[i] = f"data:image/jpeg;base64,{b64_str}"
    raid_maps_b64[str(i)] = raid_maps_b64[i]
    print(f"  Raid {i}: {len(buf.getvalue())/1024:.1f} KB")

print("2. Encoding Icons to Base64...")
item_icons = [
    'flour', 'charcoal', 'damp_rag', 'saltpetre', 'tallow_balm',
    'china_bowl', 'opium_pipe', 'opium', 'votive_candle', 'silver_key', 'gold_key',
    'book_rozier', 'book_census', 'book_catechisme', 'book_montesquieu', 'book_buffon', 'book_rondelet', 'book_mortuary'
]
item_icons_b64 = {}
for name in item_icons:
    p = os.path.join(DOC_DIR, "assets", "items", f"{name}.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            item_icons_b64[name] = f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"

cont_icons = [
    'flour_sack', 'bullion_box', 'wall_cabinet', 'pile_of_ash', 'tooling_bin', 'strongbox', 'oak_barrel', 'ledger_desk',
    'stone_grave', 'physician_bag'
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
    "map_name": "Château Outer Ramparts",
    "quest_name": "Quest 1: A Warm Welcome",
    "has_focus": True,
    "keyBadge": "No Keys Needed",
    "keyColor": "bg-[#1c1c18] text-[#a8a091] border-[#302c24]",
    "story_pois": [],
    "active_objectives": [
        {
            "title": "Quest 1: Meet the Encampment Leaders",
            "npc": "Turn in to: Eloise at Château",
            "cont_name": "Louis, Piro, Reynauld (NPCs)",
            "cont_img": "ledger_desk.webp",
            "item_img": "silver_key.png",
            "drop_rate": "100%",
            "density": "3 Hub Leaders on Ramparts",
            "desc": "Speak with Louis (Stashmaster), Piro (Merchant), and Reynauld (Expeditions) to unlock raid expeditions."
        }
    ],
    "priority_focus": {
        "title": "Focus: Check Louis Vendor Stock",
        "item": "Silver / Gold Key",
        "cont": "Louis Shop",
        "c_ico": "bullion_box.webp",
        "i_ico": "silver_key.png",
        "rate": "17.7% / 8.8%",
        "color": [192, 132, 252],
        "detail": "17.7% / 8.8% Stock Rate  •  Buy Silver Key (12s 60c) or Gold Key (25s 60c) on Ramparts"
    },
    "rotation_steps": [
        {"step": "Speak with Louis (Stashmaster) on the ramparts.", "color": [250, 204, 21]},
        {"step": "Speak with Piro near the smoke fire for starter medical supplies.", "color": [250, 204, 21]},
        {"step": "Go up the hill to Reynauld on his platform to unlock expeditions.", "color": [250, 204, 21]},
        {"step": "Check Louis vendor shop immediately: Buy Silver Key or Gold Key if stocked!", "color": [192, 132, 252]},
        {"step": "Extract to Château and turn in completed quests to Eloise.", "color": [148, 163, 184]}
    ],
    "directory": [
        {"color": [192, 132, 252], "cont": "Louis Vendor", "item": "Silver Key", "i_ico": "silver_key.png", "rate": "17.7%", "spots": "Outer Ramparts Stall (12s 60c)"},
        {"color": [56, 189, 248], "cont": "Louis Vendor", "item": "Gold Key", "i_ico": "gold_key.png", "rate": "8.8%", "spots": "Outer Ramparts Stall (25s 60c)"},
        {"color": [250, 204, 21], "cont": "Piro Vendor", "item": "Field Meds", "i_ico": "tallow_balm.png", "rate": "100%", "spots": "Leper Physician Smoke Fire"}
    ],
    "roadmap": [
        {"quest": "Quest 2: Making Dough", "items": [("20x Flour", "flour.png")]},
        {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]}
    ]
}

FULL_RAIDS_DATA = [HUB_CONFIG] + gen.RAIDS_CONFIG

print("3. Building HTML Template with Authentic Hunger Companion Styling...")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>HUNGER Companion - Eloise Fast-Track Raid Planner</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Spectral:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #0b0b09;
      color: #f0ebe0;
      font-family: 'Spectral', serif;
    }}
    .font-cinzel {{
      font-family: 'Cinzel', serif;
    }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.2); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(229,192,123,0.3); border-radius: 3px; }}
  </style>
</head>
<body class="bg-[#0b0b09] text-[#f0ebe0] antialiased p-4 md:p-6 min-h-screen">

  <div class="max-w-7xl mx-auto space-y-6">

    <!-- Top Hero Banner (Hunger Companion Dark Obsidian Theme) -->
    <header class="bg-[#151512] border border-[#302c24] rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider rounded-md bg-[#e5c07b]/15 text-[#e5c07b] border border-[#e5c07b]/30">Wipe Speedrun</span>
            <span class="text-xs text-[#a8a091]">Total Required Raids: <strong>7 Dedicated Deployments</strong></span>
          </div>
          <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-[#e5c07b] font-cinzel flex items-center gap-3">
            <span>Eloise Fast-Track Raid Planner</span>
          </h1>
          <p class="text-sm text-[#a8a091] mt-1">
            Tactical terrain maps with high-focus objectives, container priorities, merchant shortcuts, and key requirements.
          </p>
        </div>

        <!-- Progress Mini Tracker -->
        <div class="flex items-center gap-4 bg-[#0b0b09] border border-[#302c24] rounded-xl p-3 px-4 shrink-0">
          <div class="text-right">
            <div class="text-xs text-[#a8a091]">Quests Complete</div>
            <div class="text-lg font-bold text-[#e5c07b]" id="tracker-count">0 / 9</div>
          </div>
          <div class="w-12 h-12 rounded-full border-2 border-[#302c24] flex items-center justify-center font-bold text-sm text-[#e5c07b] bg-[#151512]" id="tracker-pct">
            0%
          </div>
        </div>
      </div>

      <!-- Navigation Tabs (Raid 0 to 7) -->
      <nav class="flex items-center gap-2 overflow-x-auto pt-6 border-t border-[#302c24] mt-6 pb-1">
        <button onclick="selectRaid(0)" id="tab-0" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Hub Setup
        </button>
        <button onclick="selectRaid(1)" id="tab-1" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#e5c07b] text-slate-950 font-bold border-[#e5c07b] shadow-md">
          Raid 1: Sarlat (Flour)
        </button>
        <button onclick="selectRaid(2)" id="tab-2" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 2: Bridge (Camp & Charcoal)
        </button>
        <button onclick="selectRaid(3)" id="tab-3" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 3: Sarlat (Fort & Supplies)
        </button>
        <button onclick="selectRaid(4)" id="tab-4" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 4: Sarlat (Candle & Bribery)
        </button>
        <button onclick="selectRaid(5)" id="tab-5" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 5: Sarlat (Sinai 1-3)
        </button>
        <button onclick="selectRaid(6)" id="tab-6" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 6: Bridge (Sinai 4-5)
        </button>
        <button onclick="selectRaid(7)" id="tab-7" class="raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]">
          Raid 7: Forest (Finale 6-7)
        </button>
      </nav>
    </header>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

      <!-- LEFT: High-Resolution Tactical Map (7 Cols) -->
      <div class="lg:col-span-7 space-y-4">
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg overflow-hidden">
          <div class="flex items-center justify-between mb-3 px-1">
            <h2 class="text-sm font-bold tracking-wider uppercase text-[#e5c07b] font-cinzel flex items-center gap-2" id="map-title">
              SARLAT FARM - QUEST 2: MAKING DOUGH
            </h2>
            <div class="flex items-center gap-2">
              <span class="text-xs text-[#a8a091] bg-[#0b0b09] border border-[#302c24] px-2 py-0.5 rounded">2400 x 1400 HD</span>
              <a id="open-full-btn" href="raid1_map.jpg" target="_blank" class="text-xs text-[#e5c07b] hover:underline font-semibold">Open Raw Map</a>
            </div>
          </div>
          <div class="relative rounded-xl overflow-hidden border border-[#302c24] bg-black aspect-[12/7] flex items-center justify-center">
            <img id="main-map-img" src="" alt="Tactical Map" class="w-full h-full object-contain">
            <div id="hub-placeholder" class="hidden text-center p-8 space-y-3">
              <div class="text-4xl">🏰</div>
              <h3 class="text-lg font-bold text-[#e5c07b] font-cinzel">Château Outer Ramparts</h3>
              <p class="text-xs text-[#a8a091] max-w-md mx-auto">
                No deployment map needed for Hub Setup. Speak with Louis, Piro, and Reynauld on the ramparts to unlock expedition raids.
              </p>
            </div>
          </div>
        </div>

        <!-- Questline Progression Timeline Bar (Matches Quest Titles Above) -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg">
          <div class="text-xs font-bold uppercase tracking-wider text-[#a8a091] mb-3 flex items-center justify-between">
            <span class="font-cinzel text-[#e5c07b]">Questline Progression: Eloise Storyline</span>
            <span class="text-[#e5c07b] font-bold" id="current-phase-pill">Raid 1 of 7</span>
          </div>
          <div class="grid grid-cols-7 gap-2 text-center text-[11px]" id="timeline-steps">
            <!-- Timeline nodes rendered by JS -->
          </div>
        </div>
      </div>

      <!-- RIGHT: Interactive Raid Briefing (5 Cols) -->
      <div class="lg:col-span-5 space-y-4">

        <!-- CATEGORY 1: OBJECTIVES -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#e5c07b]"></span>
              Objectives
            </h3>
            <span id="key-badge" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase border"></span>
          </div>

          <div id="active-objectives-container" class="space-y-3">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 2: FOCUS (Omitted when no focus is needed) -->
        <div id="focus-container" class="bg-[#151512] border border-[#302c24] rounded-2xl p-5 shadow-lg space-y-3">
          <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span>
            Focus
          </h3>
          <div id="b2-card" class="bg-[#1c1c18] border border-purple-500/40 rounded-xl p-3.5 flex items-center gap-3.5">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 3: PRIORITIES (Each task number in circle of matching priority color) -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-5 shadow-lg space-y-3">
          <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel">Priorities</h3>
          <ol id="tactical-steps" class="space-y-3 text-sm text-[#f0ebe0]">
            <!-- Rendered by JS -->
          </ol>
        </div>

        <!-- CATEGORY 4: DROPS (Directions with Map POIs, Item Thumbnail Badges) -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel">Drops</h3>
            <span class="text-[11px] text-[#a8a091]">Sorted by Priority</span>
          </div>

          <!-- Color Order Legend -->
          <div class="bg-[#0b0b09] border border-[#302c24] rounded-lg p-2 px-3 flex flex-wrap items-center justify-between text-[11px] gap-2">
            <span class="flex items-center gap-1.5 text-amber-400 font-semibold">
              <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>Priority 1
            </span>
            <span class="flex items-center gap-1.5 text-purple-400 font-semibold">
              <span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span>Priority 2
            </span>
            <span class="flex items-center gap-1.5 text-sky-400 font-semibold">
              <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span>Priority 3
            </span>
            <span class="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>Priority 4
            </span>
          </div>

          <!-- Dynamic Container List -->
          <div id="container-directory" class="space-y-2 text-xs">
            <!-- Rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 5: QUESTS -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-5 shadow-lg space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel">Quests</h3>
            <span class="text-[11px] text-[#e5c07b]">Click to Mark Saved</span>
          </div>
          <div id="stash-checklist" class="grid grid-cols-2 gap-2 text-xs">
            <!-- Interactive Stash Checkboxes -->
          </div>
        </div>

      </div>

    </div>

  </div>

  <script>
    const RAID_MAPS = {json.dumps(raid_maps_b64)};
    const EMBEDDED_ICONS = {{
      ...{json.dumps(item_icons_b64)},
      ...{json.dumps(cont_icons_b64)}
    }};
    const RAID_DATA = {json.dumps(FULL_RAIDS_DATA)};

    let currentRaidIdx = 1;
    let savedStash = {{}};
    try {{
      savedStash = JSON.parse(localStorage.getItem('hh_stash_saved') || '{{}}');
    }} catch (e) {{
      console.warn('localStorage not accessible:', e);
    }}

    const ALL_STASH_TARGETS = [
      {{ id: "flour", name: "20x Flour", quest: "Q2: Making Dough", icon: "flour" }},
      {{ id: "charcoal", name: "15x Charcoal", quest: "Q4: Last Embers", icon: "charcoal" }},
      {{ id: "saltpetre", name: "20x Saltpetre", quest: "Q6: Medical", icon: "saltpetre" }},
      {{ id: "damp_rag", name: "5x Damp Rag", quest: "Q6: Medical", icon: "damp_rag" }},
      {{ id: "tallow_balm", name: "10x Tallow Balm", quest: "Q6: Medical", icon: "tallow_balm" }},
      {{ id: "votive_candle", name: "1x Red Votive Candle", quest: "Q8: Sanctuary", icon: "votive_candle" }},
      {{ id: "opium_pipe", name: "1x Opium Pipe", quest: "Q9: Bribery", icon: "opium_pipe" }},
      {{ id: "china_bowl", name: "1x China Bowl", quest: "Q9: Bribery", icon: "china_bowl" }},
      {{ id: "sinai_books", name: "7x Mount Sinai Books", quest: "Q10: Mount Sinai", icon: "book_rozier" }}
    ];

    function rgbToHex(rgbArr) {{
      if (!Array.isArray(rgbArr) || rgbArr.length < 3) return '#facc15';
      return '#' + rgbArr.slice(0, 3).map(x => x.toString(16).padStart(2, '0')).join('');
    }}

    function getPrioClass(rgbArr) {{
      const hex = rgbToHex(rgbArr);
      if (hex === '#facc15') return 'bg-amber-400 text-slate-950 font-bold';
      if (hex === '#c084fc') return 'bg-purple-400 text-slate-950 font-bold';
      if (hex === '#38bdf8') return 'bg-sky-400 text-slate-950 font-bold';
      if (hex === '#4ade80') return 'bg-emerald-400 text-slate-950 font-bold';
      return 'bg-slate-600 text-white font-bold';
    }}

    function getShapeBadgeWithItem(colorHex, itemIco) {{
      const icoKey = itemIco ? itemIco.replace('.png', '') : '';
      const icoSrc = EMBEDDED_ICONS[icoKey] || (itemIco ? `assets/items/${{itemIco}}` : '');
      const icoImg = icoSrc ? `<img src="${{icoSrc}}" alt="" class="w-4 h-4 object-contain">` : '';

      return `
        <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0 bg-[#161613] shadow-sm p-0.5" style="border-color: ${{colorHex || '#facc15'}}">
          ${{icoImg}}
        </div>
      `;
    }}

    function selectRaid(idx) {{
      currentRaidIdx = idx;

      // Update Tabs
      for (let i = 0; i <= 7; i++) {{
        const tab = document.getElementById(`tab-${{i}}`);
        if (tab) {{
          if (i === idx) {{
            tab.className = "raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#e5c07b] text-slate-950 font-bold border-[#e5c07b] shadow-md";
          }} else {{
            tab.className = "raid-tab px-3.5 py-2 rounded-lg border whitespace-nowrap transition-all bg-[#151512] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b]";
          }}
        }}
      }}

      const data = RAID_DATA[idx];
      if (!data) return;

      // Update Map Viewport
      const mapImg = document.getElementById('main-map-img');
      const hubPh = document.getElementById('hub-placeholder');
      const mapTitle = document.getElementById('map-title');
      const openFullBtn = document.getElementById('open-full-btn');

      if (idx === 0) {{
        mapImg.classList.add('hidden');
        hubPh.classList.remove('hidden');
        mapTitle.textContent = "CHÂTEAU OUTER RAMPARTS - SAFE HUB";
        openFullBtn.classList.add('hidden');
      }} else {{
        hubPh.classList.add('hidden');
        mapImg.classList.remove('hidden');
        mapImg.src = RAID_MAPS[idx] || RAID_MAPS[String(idx)] || '';
        mapTitle.textContent = `${{data.map_name.toUpperCase()}} - ${{data.quest_name.toUpperCase()}}`;
        openFullBtn.classList.remove('hidden');
        openFullBtn.href = `raid${{idx}}_map.jpg`;
      }}

      // Key Badge
      const keyBadge = document.getElementById('key-badge');
      if (idx === 0) {{
        keyBadge.textContent = "Hub Safe Area";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-[#1c1c18] text-[#a8a091] border-[#302c24]";
      }} else if (idx === 1) {{
        keyBadge.textContent = "Starter Run";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-[#1c1c18] text-[#a8a091] border-[#302c24]";
      }} else if (idx === 2) {{
        keyBadge.textContent = "Camp & Charcoal";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-[#e5c07b]/15 text-[#e5c07b] border-[#e5c07b]/30";
      }} else if (idx === 3) {{
        keyBadge.textContent = "Fort Recon";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-blue-500/15 text-blue-400 border-blue-500/30";
      }} else if (idx === 4) {{
        keyBadge.textContent = "Candle & Bribery";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-purple-500/15 text-purple-400 border-purple-500/30";
      }} else {{
        keyBadge.textContent = "Sinai Expedition";
        keyBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold uppercase border bg-[#e5c07b]/15 text-[#e5c07b] border-[#e5c07b]/30";
      }}

      // Phase Pill
      document.getElementById('current-phase-pill').textContent = idx === 0 ? 'Hub Setup' : `Raid ${{idx}} of 7`;

      // Timeline Nodes (Matches Quest Titles Above)
      const timelineDiv = document.getElementById('timeline-steps');
      const timelineLabels = [
        "Q2: Making Dough", "Q3-4: Camp & Charcoal", "Q5-6: Fort & Supplies", "Q8-9: Candle & Bribery", "Q10: Sinai Part 1", "Q10: Sinai Part 2", "Q10: Sinai Finale"
      ];
      timelineDiv.innerHTML = timelineLabels.map((lbl, i) => {{
        const raidNum = i + 1;
        const isDone = raidNum < idx;
        const isCurrent = raidNum === idx;
        return `
          <div class="p-2 rounded-xl border ${{isCurrent ? 'bg-[#e5c07b]/15 border-[#e5c07b] text-[#e5c07b] font-bold' : isDone ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-400 font-semibold' : 'bg-[#0b0b09] border-[#302c24] text-[#a8a091]'}}">
            <div class="text-[10px] uppercase font-bold">${{isDone ? '[DONE]' : `Raid ${{raidNum}}`}}</div>
            <div class="truncate mt-0.5 font-cinzel text-[10px]">${{lbl}}</div>
          </div>
        `;
      }}).join('');

      // CATEGORY 1: Objectives (All Books in Objectives, No Coords)
      const actContainer = document.getElementById('active-objectives-container');
      actContainer.innerHTML = data.active_objectives.map(o => {{
        const contImg = EMBEDDED_ICONS[o.cont_img ? o.cont_img.replace('.webp', '') : ''] || `assets/containers/${{o.cont_img}}`;
        const itemImg = EMBEDDED_ICONS[o.item_img ? o.item_img.replace('.png', '') : ''] || `assets/items/${{o.item_img}}`;
        return `
          <div class="bg-[#1c1c18] border border-[#302c24] rounded-xl p-3.5 flex items-start gap-3.5 hover:border-[#e5c07b]/60 transition-colors">
            <div class="relative w-14 h-14 bg-black/40 border border-[#302c24] rounded-lg shrink-0 flex items-center justify-center p-1 overflow-hidden">
              <img src="${{contImg}}" alt="" class="w-full h-full object-contain">
              <img src="${{itemImg}}" alt="" class="absolute bottom-0 right-0 w-6 h-6 object-contain drop-shadow">
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-2">
                <h4 class="font-bold text-[#f0ebe0] text-xs truncate font-cinzel">${{o.title}}</h4>
                <span class="text-xs font-bold text-[#e5c07b] shrink-0">${{o.drop_rate}}</span>
              </div>
              <p class="text-[11px] text-[#a8a091] mt-0.5 truncate">${{o.cont_name}} - <span class="text-[#f0ebe0]">${{o.density}}</span></p>
              <p class="text-[11px] text-[#a8a091] mt-1 leading-relaxed">${{o.desc}}</p>
              <div class="text-[10px] text-emerald-400 font-bold mt-1.5 flex items-center gap-1">
                <span>📍</span> ${{o.npc}}
              </div>
            </div>
          </div>
        `;
      }}).join('');

      // CATEGORY 2: Focus (Omitted in Raids 4, 5, 6, 7)
      const focusDiv = document.getElementById('focus-container');
      if (data.has_focus && data.priority_focus) {{
        focusDiv.classList.remove('hidden');
        const pf = data.priority_focus;
        const b2Card = document.getElementById('b2-card');
        const pfColorHex = rgbToHex(pf.color || [192, 132, 252]);
        b2Card.style.borderColor = pfColorHex;

        const pfContImg = EMBEDDED_ICONS[pf.c_ico ? pf.c_ico.replace('.webp', '') : ''] || `assets/containers/${{pf.c_ico}}`;
        const pfItemImg = EMBEDDED_ICONS[pf.i_ico ? pf.i_ico.replace('.png', '') : ''] || `assets/items/${{pf.i_ico}}`;
        b2Card.innerHTML = `
          <div class="relative w-12 h-12 bg-black/40 border rounded-lg shrink-0 flex items-center justify-center p-1 overflow-hidden" style="border-color: ${{pfColorHex}}">
            <img src="${{pfContImg}}" alt="" class="w-full h-full object-contain">
            <img src="${{pfItemImg}}" alt="" class="absolute bottom-0 right-0 w-6 h-6 object-contain drop-shadow">
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="font-bold text-[#f0ebe0] text-xs font-cinzel truncate">${{pf.title || ''}}</h4>
            <p class="text-[11px] font-semibold mt-1" style="color: ${{pfColorHex}}">${{pf.detail || ''}}</p>
          </div>
        `;
      }} else {{
        focusDiv.classList.add('hidden');
      }}

      // CATEGORY 3: Priorities (Coherent Extraction Phrasing & Matching Color Badges)
      const stepsOl = document.getElementById('tactical-steps');
      stepsOl.innerHTML = data.rotation_steps.map((s, i) => {{
        const prioCls = getPrioClass(s.color);
        return `
          <li class="flex items-start gap-3">
            <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] shrink-0 mt-0.5 ${{prioCls}}">${{i}}</span>
            <span class="leading-relaxed font-medium text-[#f0ebe0]">${{s.step}}</span>
          </li>
        `;
      }}).join('');

      // CATEGORY 4: Drops (POI Directions, Two-Line Clean Format)
      const dirDiv = document.getElementById('container-directory');
      dirDiv.innerHTML = data.directory.map(itm => {{
        const colorHex = rgbToHex(itm.color);
        return `
          <div class="bg-[#1c1c18] border border-[#302c24] rounded-xl px-3 py-2.5 flex items-center justify-between gap-3 hover:border-[#e5c07b]/50 transition-colors">
            <div class="flex items-center gap-3 min-w-0">
              ${{getShapeBadgeWithItem(colorHex, itm.i_ico)}}
              <div class="min-w-0">
                <div class="font-bold text-[#f0ebe0] text-xs truncate font-cinzel">
                  ${{itm.cont}} <span class="text-[#a8a091]">-></span> ${{itm.item}}
                </div>
                <div class="text-[11px] text-[#a8a091] mt-0.5">
                  <span class="text-[#e5c07b] font-semibold">${{itm.rate}}</span> • ${{itm.spots}}
                </div>
              </div>
            </div>
          </div>
        `;
      }}).join('');

      // CATEGORY 5: Quests Checklist
      renderStashChecklist();
    }}

    function toggleStash(id) {{
      savedStash[id] = !savedStash[id];
      try {{
        localStorage.setItem('hh_stash_saved', JSON.stringify(savedStash));
      }} catch(e) {{}}
      renderStashChecklist();
      updateTracker();
    }}

    function renderStashChecklist() {{
      const div = document.getElementById('stash-checklist');
      div.innerHTML = ALL_STASH_TARGETS.map(t => {{
        const isSaved = !!savedStash[t.id];
        const iconSrc = EMBEDDED_ICONS[t.icon] || `assets/items/${{t.icon}}.png`;
        return `
          <div onclick="toggleStash('${{t.id}}')" class="cursor-pointer border rounded-xl p-2.5 flex items-center justify-between gap-2 transition-all ${{isSaved ? 'bg-emerald-950/40 border-emerald-500/50 text-[#f0ebe0]' : 'bg-[#1c1c18] border-[#302c24] text-[#a8a091] hover:border-[#e5c07b]/40'}}">
            <div class="flex items-center gap-2 min-w-0">
              <img src="${{iconSrc}}" alt="" class="w-6 h-6 object-contain shrink-0">
              <div class="min-w-0">
                <div class="font-bold text-[11px] truncate ${{isSaved ? 'text-emerald-300' : 'text-[#f0ebe0]'}}">${{t.name}}</div>
                <div class="text-[9px] text-[#a8a091] truncate">${{t.quest}}</div>
              </div>
            </div>
            <div class="w-4 h-4 rounded border flex items-center justify-center shrink-0 ${{isSaved ? 'bg-emerald-500 border-emerald-400 text-black font-bold text-[10px]' : 'border-[#302c24]'}}">
              ${{isSaved ? '✓' : ''}}
            </div>
          </div>
        `;
      }}).join('');
    }}

    function updateTracker() {{
      const count = Object.values(savedStash).filter(Boolean).length;
      const total = ALL_STASH_TARGETS.length;
      const pct = Math.round((count / total) * 100);
      document.getElementById('tracker-count').textContent = `${{count}} / ${{total}}`;
      document.getElementById('tracker-pct').textContent = `${{pct}}%`;
    }}

    // Safe Auto-Init
    try {{
      selectRaid(1);
      updateTracker();
    }} catch(e) {{
      console.error('Initialization error:', e);
    }}
  </script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {HTML_PATH} successfully ({len(html_content)} bytes)")
