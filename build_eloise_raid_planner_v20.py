import os, io, base64, json
from PIL import Image
import generate_perfect_briefings_v25 as gen

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
HTML_PATH = os.path.join(ART_DIR, "eloise_raid_planner.html")
DESKTOP_PATH = r"C:\Users\PC\Desktop\Hunger_Raid_Maps\eloise_raid_planner.html"
PROJECT_PATH = r"C:\Users\PC\Documents\HungerHelper\Raid_Maps\eloise_raid_planner.html"

def build():
    print("1. Encoding 7 V25 Raid Maps to High-Res Base64 (2160x1260)...")
    raid_maps_b64 = {}
    for i in range(1, 8):
        p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
        im = Image.open(p).resize((2160, 1260), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=82, optimize=True)
        b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
        raid_maps_b64[i] = f"data:image/jpeg;base64,{b64_str}"
        raid_maps_b64[str(i)] = raid_maps_b64[i]
        print(f"  Raid {i}: {len(buf.getvalue())/1024:.1f} KB")

    print("2. Encoding Icons...")
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
        'stone_grave', 'physician_bag', 'basket', 'jacques_medicinals'
    ]
    cont_icons_b64 = {}
    for name in cont_icons:
        p = os.path.join(DOC_DIR, "assets", "containers", f"{name}.webp")
        if os.path.exists(p):
            with open(p, "rb") as f:
                cont_icons_b64[name] = f"data:image/webp;base64,{base64.b64encode(f.read()).decode('ascii')}"

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
                "title": "Quest 1: Meet Encampment Leaders (Louis, Piro, Reynauld)",
                "cont_img": "ledger_desk.webp",
                "item_img": "silver_key.png"
            }
        ],
        "priority_focus": {
            "title": "Check Louis Vendor Stock (Silver / Gold Key)",
            "item": "Silver / Gold Key",
            "c_ico": "bullion_box.webp",
            "i_ico": "silver_key.png",
            "color": [192, 132, 252]
        },
        "rotation_steps": [
            {"step": "Speak with Louis (Stashmaster) on the ramparts.", "color": [250, 204, 21]},
            {"step": "Speak with Piro near the smoke fire for starter medical supplies.", "color": [250, 204, 21]},
            {"step": "Go up the hill to Reynauld on his platform to unlock expeditions.", "color": [250, 204, 21]},
            {"step": "Check Louis vendor shop immediately for Silver Key or Gold Key.", "color": [192, 132, 252]},
            {"step": "Extract to Château and turn in completed quests to Eloise.", "color": [148, 163, 184]}
        ],
        "directory": [
            {"color": [192, 132, 252], "cont": "Louis Vendor", "c_ico": "bullion_box.webp", "item": "Silver Key", "i_ico": "silver_key.png", "rate": "17.7%", "spots": "Outer Ramparts Stall (12s 60c)"},
            {"color": [56, 189, 248], "cont": "Louis Vendor", "c_ico": "bullion_box.webp", "item": "Gold Key", "i_ico": "gold_key.png", "rate": "8.8%", "spots": "Outer Ramparts Stall (25s 60c)"},
            {"color": [250, 204, 21], "cont": "Piro Vendor", "c_ico": "physician_bag.webp", "item": "Field Meds", "i_ico": "tallow_balm.png", "rate": "100%", "spots": "Leper Physician Smoke Fire"}
        ],
        "roadmap": [
            {"quest": "Quest 2: Making Dough", "items": [("20x Flour", "flour.png")]},
            {"quest": "Quest 4: Last Embers", "items": [("15x Charcoal", "charcoal.png")]}
        ]
    }

    FULL_RAIDS_DATA = [HUB_CONFIG] + gen.RAIDS_CONFIG

    print("3. Building HTML Template with Interactive Pan/Zoom Map & No Duplicate Navigation...")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HUNGER Companion - Eloise Interactive Quest Tracker</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Spectral:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #0b0b09;
      color: #f0ebe0;
      font-family: 'Spectral', serif;
      user-select: none;
    }}
    .font-cinzel {{
      font-family: 'Cinzel', serif;
    }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.3); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(229,192,123,0.3); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(229,192,123,0.5); }}

    /* Interactive Map Viewport */
    #map-viewport {{
      position: relative;
      overflow: hidden;
      cursor: default;
      touch-action: none;
      background-color: #0c0c0a;
      aspect-ratio: 16 / 10;
    }}
    #map-viewport.is-panning {{
      cursor: grabbing !important;
    }}
    #map-viewport.can-pan {{
      cursor: grab;
    }}
    #map-content {{
      width: 100%;
      height: 100%;
      transform-origin: 0 0;
      transition: transform 0.05s ease-out;
      will-change: transform;
    }}
    #map-content.smooth-transition {{
      transition: transform 0.25s cubic-bezier(0.2, 0, 0, 1) !important;
    }}

    /* Floating Map Tool buttons */
    .map-btn {{
      background-color: rgba(21, 21, 18, 0.9);
      border: 1px solid #302c24;
      color: #f0ebe0;
      transition: all 0.15s ease;
      backdrop-filter: blur(4px);
    }}
    .map-btn:hover {{
      background-color: #e5c07b;
      color: #0b0b09;
      border-color: #e5c07b;
    }}
    .map-btn:active {{
      transform: scale(0.95);
    }}
  </style>
</head>
<body class="bg-[#0b0b09] text-[#f0ebe0] antialiased p-3 md:p-5 min-h-screen">

  <div class="max-w-[1700px] mx-auto space-y-4">

    <!-- TOP HEADER: Authentic Hunger Companion Navigation (NO DUPLICATE TABS) -->
    <header class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-2xl relative">
      <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
        
        <!-- Left Title & Hub Button -->
        <div class="flex items-center gap-3 shrink-0">
          <button onclick="selectRaid(0)" id="btn-hub" class="px-3.5 py-2 rounded-xl border text-xs font-cinzel font-bold tracking-wider transition-all bg-[#1c1c18] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b] hover:border-[#e5c07b]/50 flex items-center gap-2">
            <span>🏰</span>
            <span>HUB SETUP</span>
          </button>
          <div class="h-8 w-px bg-[#302c24] hidden sm:block"></div>
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 text-[10px] font-bold uppercase rounded bg-[#e5c07b]/15 text-[#e5c07b] border border-[#e5c07b]/30">Playtest 5.0</span>
              <span class="text-xs text-[#a8a091] font-cinzel">Eloise Speedrun Route</span>
            </div>
            <h1 class="text-lg md:text-xl font-bold tracking-tight text-[#e5c07b] font-cinzel">
              HUNGER Companion Planner
            </h1>
          </div>
        </div>

        <!-- 7-RAID CAMPAIGN PROGRESSION (PRIMARY INTERACTIVE SELECTOR - NO DUPLICATE SCROLLBAR!) -->
        <div class="flex-1 min-w-0">
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 text-center" id="header-timeline-steps">
            <!-- 7 Interactive Step Cards Rendered by JS -->
          </div>
        </div>

      </div>
    </header>

    <!-- MAIN TWO-COLUMN LAYOUT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">

      <!-- LEFT: INTERACTIVE TACTICAL MAP WITH PAN & ZOOM (7 COLS) -->
      <div class="lg:col-span-7 space-y-2">
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-3.5 shadow-lg overflow-hidden relative">
          
          <!-- Map Title Bar -->
          <div class="flex items-center justify-between mb-2.5 px-1">
            <div class="flex items-center gap-2 min-w-0">
              <span class="w-2.5 h-2.5 rounded-full bg-[#e5c07b] shrink-0"></span>
              <h2 class="text-sm font-bold tracking-wider uppercase text-[#e5c07b] font-cinzel truncate" id="map-title">
                SARLAT FARM
              </h2>
              <span id="map-quest-pill" class="text-xs text-[#a8a091] border-l border-[#302c24] pl-2 hidden sm:inline truncate">
                Quest 2: Making Dough
              </span>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <span class="text-[11px] text-[#a8a091] bg-[#0b0b09] border border-[#302c24] px-2 py-0.5 rounded">2400 × 1400 HD</span>
              <a id="open-full-btn" href="raid1_map.jpg" target="_blank" class="text-xs text-[#e5c07b] hover:underline font-semibold flex items-center gap-1">
                <span>Raw Map</span>
                <span class="text-[10px]">↗</span>
              </a>
            </div>
          </div>

          <!-- The Zoomable Viewport -->
          <div id="map-viewport" class="rounded-xl border border-[#302c24] flex items-center justify-center">
            
            <!-- Map Content Container (Panned & Scaled) -->
            <div id="map-content" class="w-full h-full flex items-center justify-center">
              <img id="main-map-img" src="" alt="Tactical Map" class="w-full h-full object-contain pointer-events-none select-none">
              
              <!-- Hub Area Placeholder -->
              <div id="hub-placeholder" class="hidden text-center p-8 space-y-3">
                <div class="text-5xl">🏰</div>
                <h3 class="text-xl font-bold text-[#e5c07b] font-cinzel">Château Outer Ramparts</h3>
                <p class="text-xs text-[#a8a091] max-w-md mx-auto">
                  Safe Encampment Hub. Speak with Louis (Stash), Piro (Meds), and Reynauld (Expeditions) to unlock deployment.
                </p>
              </div>
            </div>

            <!-- Floating Hunger Companion Zoom Controls Overlay -->
            <div class="absolute top-3 right-3 flex flex-col gap-1.5 z-20">
              <button onclick="mapPanZoom.zoomIn()" title="Zoom In (+)" class="map-btn w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shadow-lg">
                +
              </button>
              <button onclick="mapPanZoom.zoomOut()" title="Zoom Out (-)" class="map-btn w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm shadow-lg">
                −
              </button>
              <div id="zoom-level-badge" class="px-1.5 py-0.5 rounded bg-black/80 border border-[#302c24] text-[10px] text-center font-mono text-[#e5c07b] shadow">
                100%
              </div>
              <button onclick="mapPanZoom.reset()" title="Reset View (100%)" class="map-btn w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shadow-lg">
                ⟲
              </button>
              <button onclick="toggleMapFullscreen()" title="Toggle Fullscreen" class="map-btn w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shadow-lg">
                ⛶
              </button>
            </div>

            <!-- Bottom Left Navigation Hint -->
            <div class="absolute bottom-2.5 left-3 text-[11px] text-[#a8a091] bg-black/75 backdrop-blur-sm border border-[#302c24] px-2.5 py-1 rounded-md pointer-events-none flex items-center gap-2">
              <span class="text-[#e5c07b]">✦</span>
              <span>Scroll wheel to zoom • Drag to pan</span>
            </div>

          </div>
        </div>
      </div>

      <!-- RIGHT: COMPREHENSIVE RAID BRIEFING (5 COLS, COHERENT SPACING) -->
      <div class="lg:col-span-5 space-y-3">

        <!-- CATEGORY 1: OBJECTIVES -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg space-y-2.5">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-[#e5c07b]"></span>
              Objectives
            </h3>
            <span id="key-badge" class="px-2 py-0.5 rounded text-[10px] font-bold uppercase border"></span>
          </div>
          <div id="active-objectives-container" class="space-y-2.5">
            <!-- Objectives rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 2: FOCUS (Omitted when no focus is needed) -->
        <div id="focus-container" class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg space-y-2.5">
          <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span>
            Focus
          </h3>
          <div id="b2-card" class="bg-[#1c1c18] border border-purple-500/40 rounded-xl p-3 flex items-center gap-3">
            <!-- Focus rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 3: PRIORITIES -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg space-y-2.5">
          <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel">Priorities</h3>
          <ol id="tactical-steps" class="space-y-2.5 text-xs text-[#f0ebe0]">
            <!-- Steps rendered by JS -->
          </ol>
        </div>

        <!-- CATEGORY 4: DROPS (Container Badges, Rates, Map Directions) -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg space-y-2.5">
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
            <!-- Directory rendered by JS -->
          </div>
        </div>

        <!-- CATEGORY 5: QUESTS (Interactive Stash Checklist) -->
        <div class="bg-[#151512] border border-[#302c24] rounded-2xl p-4 shadow-lg space-y-2.5">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold uppercase tracking-wider text-[#e5c07b] font-cinzel">Quests</h3>
            <span class="text-[11px] text-[#e5c07b]">Click to Mark Saved</span>
          </div>
          <div id="stash-checklist" class="grid grid-cols-2 gap-2 text-xs">
            <!-- Checklist rendered by JS -->
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

    // ==========================================
    // INTERACTIVE PAN & ZOOM CONTROLLER
    // ==========================================
    class MapPanZoomController {{
      constructor(viewportEl, contentEl) {{
        this.viewport = viewportEl;
        this.content = contentEl;
        this.scale = 1.0;
        this.minScale = 1.0;
        this.maxScale = 4.5;
        this.translateX = 0;
        this.translateY = 0;
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.init();
      }}

      init() {{
        // Wheel zoom centered on mouse cursor
        this.viewport.addEventListener('wheel', (e) => {{
          e.preventDefault();
          const rect = this.viewport.getBoundingClientRect();
          const mouseX = e.clientX - rect.left;
          const mouseY = e.clientY - rect.top;

          const delta = -e.deltaY;
          const factor = delta > 0 ? 1.2 : 0.833;
          const newScale = Math.min(this.maxScale, Math.max(this.minScale, this.scale * factor));

          if (newScale !== this.scale) {{
            const ratio = newScale / this.scale;
            this.translateX = mouseX - (mouseX - this.translateX) * ratio;
            this.translateY = mouseY - (mouseY - this.translateY) * ratio;
            this.scale = newScale;
            this.clampBounds();
            this.applyTransform();
            this.updateUI();
          }}
        }}, {{ passive: false }});

        // Pointer drag to pan
        this.viewport.addEventListener('pointerdown', (e) => {{
          if (e.button !== 0) return;
          this.isDragging = true;
          this.startX = e.clientX - this.translateX;
          this.startY = e.clientY - this.translateY;
          this.viewport.setPointerCapture(e.pointerId);
          this.viewport.classList.add('is-panning');
        }});

        this.viewport.addEventListener('pointermove', (e) => {{
          if (!this.isDragging) return;
          this.translateX = e.clientX - this.startX;
          this.translateY = e.clientY - this.startY;
          this.clampBounds();
          this.applyTransform();
        }});

        const stopDrag = (e) => {{
          if (this.isDragging) {{
            this.isDragging = false;
            try {{ this.viewport.releasePointerCapture(e.pointerId); }} catch(err){{}}
            this.viewport.classList.remove('is-panning');
          }}
        }};

        this.viewport.addEventListener('pointerup', stopDrag);
        this.viewport.addEventListener('pointercancel', stopDrag);

        // Double click to zoom in or reset
        this.viewport.addEventListener('dblclick', (e) => {{
          if (this.scale > 1.5) {{
            this.reset();
          }} else {{
            const rect = this.viewport.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            this.zoomTo(2.4, mouseX, mouseY);
          }}
        }});
      }}

      zoomIn() {{
        const rect = this.viewport.getBoundingClientRect();
        this.zoomTo(Math.min(this.maxScale, this.scale * 1.3), rect.width / 2, rect.height / 2);
      }}

      zoomOut() {{
        const rect = this.viewport.getBoundingClientRect();
        this.zoomTo(Math.max(this.minScale, this.scale / 1.3), rect.width / 2, rect.height / 2);
      }}

      zoomTo(newScale, cx, cy) {{
        if (newScale === this.scale) return;
        const ratio = newScale / this.scale;
        this.translateX = cx - (cx - this.translateX) * ratio;
        this.translateY = cy - (cy - this.translateY) * ratio;
        this.scale = newScale;
        this.clampBounds();
        this.applyTransform(true);
        this.updateUI();
      }}

      reset() {{
        this.scale = 1.0;
        this.translateX = 0;
        this.translateY = 0;
        this.applyTransform(true);
        this.updateUI();
      }}

      clampBounds() {{
        const rect = this.viewport.getBoundingClientRect();
        if (this.scale <= 1.0) {{
          this.scale = 1.0;
          this.translateX = 0;
          this.translateY = 0;
          return;
        }}
        const minX = rect.width * (1 - this.scale);
        const minY = rect.height * (1 - this.scale);
        this.translateX = Math.min(0, Math.max(minX, this.translateX));
        this.translateY = Math.min(0, Math.max(minY, this.translateY));
      }}

      applyTransform(smooth = false) {{
        if (smooth) {{
          this.content.classList.add('smooth-transition');
          setTimeout(() => this.content.classList.remove('smooth-transition'), 260);
        }}
        this.content.style.transform = `translate(${{this.translateX}}px, ${{this.translateY}}px) scale(${{this.scale}})`;
      }}

      updateUI() {{
        const badge = document.getElementById('zoom-level-badge');
        if (badge) {{
          badge.textContent = `${{Math.round(this.scale * 100)}}%`;
        }}
        if (this.scale > 1.0) {{
          this.viewport.classList.add('can-pan');
        }} else {{
          this.viewport.classList.remove('can-pan');
        }}
      }}
    }}

    let mapPanZoom = null;

    function toggleMapFullscreen() {{
      const elem = document.getElementById('map-viewport');
      if (!document.fullscreenElement) {{
        elem.requestFullscreen().catch(err => console.warn(err));
      }} else {{
        document.exitFullscreen().catch(err => console.warn(err));
      }}
    }}

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

    function getShapeBadgeWithContainer(colorHex, contIco) {{
      const icoKey = contIco ? contIco.replace('.webp', '').replace('.png', '') : '';
      const icoSrc = EMBEDDED_ICONS[icoKey] || (contIco ? `assets/containers/${{contIco}}` : '');
      const icoImg = icoSrc ? `<img src="${{icoSrc}}" alt="" class="w-5 h-5 object-contain">` : '';

      return `
        <div class="w-7 h-7 rounded-full border-2 flex items-center justify-center shrink-0 bg-[#161613] shadow-sm p-0.5" style="border-color: ${{colorHex || '#facc15'}}">
          ${{icoImg}}
        </div>
      `;
    }}

    // ==========================================
    // RAID SELECTION (PRIMARY PROGRESSION HEADER)
    // ==========================================
    function selectRaid(idx) {{
      currentRaidIdx = idx;

      // Update Hub Button State
      const btnHub = document.getElementById('btn-hub');
      if (btnHub) {{
        if (idx === 0) {{
          btnHub.className = "px-3.5 py-2 rounded-xl border text-xs font-cinzel font-bold tracking-wider transition-all bg-[#e5c07b] text-slate-950 border-[#e5c07b] shadow-md flex items-center gap-2";
        }} else {{
          btnHub.className = "px-3.5 py-2 rounded-xl border text-xs font-cinzel font-bold tracking-wider transition-all bg-[#1c1c18] border-[#302c24] text-[#a8a091] hover:text-[#e5c07b] hover:border-[#e5c07b]/50 flex items-center gap-2";
        }}
      }}

      // Update 7-Raid Primary Progression Cards in Header
      const timelineDiv = document.getElementById('header-timeline-steps');
      const timelineSteps = [
        {{ num: 1, label: "Raid 1: Making Dough" }},
        {{ num: 2, label: "Raid 2: Camp & Charcoal" }},
        {{ num: 3, label: "Raid 3: Fort & Supplies" }},
        {{ num: 4, label: "Raid 4: Candle & Bribery" }},
        {{ num: 5, label: "Raid 5: Sinai Part 1" }},
        {{ num: 6, label: "Raid 6: Sinai Part 2" }},
        {{ num: 7, label: "Raid 7: Sinai Finale" }}
      ];
      
      timelineDiv.innerHTML = timelineSteps.map(s => {{
        const isDone = s.num < idx;
        const isCurrent = s.num === idx;
        return `
          <div onclick="selectRaid(${{s.num}})" class="cursor-pointer py-2 px-2.5 rounded-xl border transition-all text-center ${{isCurrent ? 'bg-[#403410] border-[#e5c07b] text-[#e5c07b] font-bold shadow-lg scale-[1.02]' : isDone ? 'bg-[#101c12] border-emerald-500/50 text-emerald-400 font-semibold' : 'bg-[#141410] border-[#302c24] text-[#a8a091] hover:border-[#e5c07b]/40'}}">
            <div class="font-cinzel text-xs truncate">${{s.label}}</div>
          </div>
        `;
      }}).join('');

      const data = RAID_DATA[idx];
      if (!data) return;

      // Update Map Viewport & Title
      const mapImg = document.getElementById('main-map-img');
      const hubPh = document.getElementById('hub-placeholder');
      const mapTitle = document.getElementById('map-title');
      const mapQuestPill = document.getElementById('map-quest-pill');
      const openFullBtn = document.getElementById('open-full-btn');

      if (idx === 0) {{
        mapImg.classList.add('hidden');
        hubPh.classList.remove('hidden');
        mapTitle.textContent = "CHÂTEAU OUTER RAMPARTS";
        mapQuestPill.textContent = "Safe Hub Area";
        openFullBtn.classList.add('hidden');
      }} else {{
        hubPh.classList.add('hidden');
        mapImg.classList.remove('hidden');
        mapImg.src = RAID_MAPS[idx] || RAID_MAPS[String(idx)] || '';
        mapTitle.textContent = `${{data.map_name.toUpperCase()}}`;
        mapQuestPill.textContent = data.quest_name;
        openFullBtn.classList.remove('hidden');
        openFullBtn.href = `raid${{idx}}_map.jpg`;
      }}

      // Reset Pan & Zoom on Raid Switch
      if (mapPanZoom) {{
        mapPanZoom.reset();
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

      // CATEGORY 1: Objectives (No Small Text, Clean & Punchy)
      const actContainer = document.getElementById('active-objectives-container');
      actContainer.innerHTML = data.active_objectives.map(o => {{
        const contImg = EMBEDDED_ICONS[o.cont_img ? o.cont_img.replace('.webp', '') : ''] || `assets/containers/${{o.cont_img}}`;
        const itemImg = EMBEDDED_ICONS[o.item_img ? o.item_img.replace('.png', '') : ''] || `assets/items/${{o.item_img}}`;
        return `
          <div class="bg-[#1c1c18] border border-[#302c24] rounded-xl p-3 flex items-center gap-3.5 hover:border-[#e5c07b]/60 transition-colors">
            <div class="relative w-12 h-12 bg-black/40 border border-[#302c24] rounded-lg shrink-0 flex items-center justify-center p-1 overflow-hidden">
              <img src="${{contImg}}" alt="" class="w-full h-full object-contain">
              <img src="${{itemImg}}" alt="" class="absolute bottom-0 right-0 w-5 h-5 object-contain drop-shadow">
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="font-bold text-[#f0ebe0] text-sm font-cinzel truncate">${{o.title}}</h4>
            </div>
          </div>
        `;
      }}).join('');

      // CATEGORY 2: Focus (No Small Text)
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
            <h4 class="font-bold text-[#f0ebe0] text-sm font-cinzel truncate">${{pf.title || ''}}</h4>
          </div>
        `;
      }} else {{
        focusDiv.classList.add('hidden');
      }}

      // CATEGORY 3: Priorities (No Drop Location, Standard Extraction Phrasing)
      const stepsOl = document.getElementById('tactical-steps');
      stepsOl.innerHTML = data.rotation_steps.map((s, i) => {{
        const prioCls = getPrioClass(s.color);
        return `
          <li class="flex items-start gap-2.5">
            <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] shrink-0 mt-0.5 ${{prioCls}}">${{i}}</span>
            <span class="leading-relaxed font-medium text-[#f0ebe0] text-xs">${{s.step}}</span>
          </li>
        `;
      }}).join('');

      // CATEGORY 4: Drops (Container Badges, Rates, POI Directions)
      const dirDiv = document.getElementById('container-directory');
      dirDiv.innerHTML = data.directory.map(itm => {{
        const colorHex = rgbToHex(itm.color);
        return `
          <div class="bg-[#1c1c18] border border-[#302c24] rounded-xl px-3 py-2 flex items-center justify-between gap-3 hover:border-[#e5c07b]/50 transition-colors">
            <div class="flex items-center gap-3 min-w-0">
              ${{getShapeBadgeWithContainer(colorHex, itm.c_ico)}}
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
                <div class="font-bold text-xs truncate ${{isSaved ? 'text-emerald-300' : 'text-[#f0ebe0]'}}">${{t.name}}</div>
                <div class="text-[10px] text-[#a8a091] truncate">${{t.quest}}</div>
              </div>
            </div>
            <div class="w-4 h-4 rounded border flex items-center justify-center shrink-0 ${{isSaved ? 'bg-emerald-500 border-emerald-400 text-black font-bold text-[10px]' : 'border-[#302c24]'}}">
              ${{isSaved ? '✓' : ''}}
            </div>
          </div>
        `;
      }}).join('');
    }}

    // Safe Auto-Init
    document.addEventListener("DOMContentLoaded", () => {{
      const viewportEl = document.getElementById('map-viewport');
      const contentEl = document.getElementById('map-content');
      if (viewportEl && contentEl) {{
        mapPanZoom = new MapPanZoomController(viewportEl, contentEl);
      }}
      selectRaid(1);
    }});
  </script>
</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(DESKTOP_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(PROJECT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated {HTML_PATH} successfully ({len(html_content)} bytes)")
    print(f"Copied to Desktop: {DESKTOP_PATH}")
    print(f"Copied to Project: {PROJECT_PATH}")

if __name__ == "__main__":
    build()
