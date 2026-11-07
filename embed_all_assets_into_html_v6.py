import os, io, base64, re
from PIL import Image

ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
ITEM_DIR = os.path.join(ART_DIR, "assets", "items")
HTML_PATH = os.path.join(ART_DIR, "eloise_raid_planner.html")

print("1. Encoding 7 V6 Raid Map Briefings to Base64 (Crisp 1920x1120)...")
raid_maps_b64 = {}
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    im = Image.open(p).resize((1920, 1120), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82, optimize=True)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    raid_maps_b64[i] = f"data:image/jpeg;base64,{b64_str}"
    print(f"  Raid {i}: {len(buf.getvalue())/1024:.1f} KB")

print("2. Encoding Item Icons to Base64...")
item_icons = [
    'flour', 'charcoal', 'damp_rag', 'saltpetre', 'tallow_balm',
    'china_bowl', 'opium_pipe', 'opium', 'votive_candle'
]
item_icons_b64 = {}
for name in item_icons:
    p = os.path.join(ITEM_DIR, f"{name}.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64_str = base64.b64encode(f.read()).decode("ascii")
            item_icons_b64[name] = f"data:image/png;base64,{b64_str}"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Fix outdated tab labels
html = html.replace("Raid 6 · Bridge (Silver Key)", "Raid 6 · Bridge (Mount Sinai 2)")
html = html.replace("Raid 7 · Forest (Gold Key)", "Raid 7 · Forest (Mount Sinai 3)")

# Replace map container with multi-image pre-rendered DOM structure
map_imgs_html = ""
for i in range(1, 8):
    hidden_cls = "" if i == 1 else "hidden"
    map_imgs_html += f'            <img id="map-img-{i}" class="map-view w-full h-full object-contain {hidden_cls}" src="{raid_maps_b64[i]}" alt="Raid {i} Map" onerror="this.src=\'raid{i}_map.jpg\'">\n'

old_container_pattern = r'<div class="relative w-full aspect-\[16/10\] bg-slate-950 rounded-xl my-4 overflow-hidden border border-\[var\(--border,#262f3d\)\] shadow-inner flex items-center justify-center group cursor-pointer" onclick="openZoomModal\(\)">[\s\S]*?</div>\s*</div>\s*<!-- 4-Box Focused Priority Breakdown Grid -->'

new_container = f'''<div class="relative w-full aspect-[16/10] bg-slate-950 rounded-xl my-4 overflow-hidden border border-[var(--border,#262f3d)] shadow-inner flex items-center justify-center group cursor-pointer" onclick="openZoomModal()">
{map_imgs_html}
            <div id="hub-overlay" class="hidden text-center p-6 space-y-2">
              <div class="text-3xl">🏰</div>
              <h3 id="hub-overlay-title" class="text-lg font-bold text-white">Hub Base</h3>
              <p id="hub-overlay-desc" class="text-xs text-slate-400 max-w-md mx-auto"></p>
            </div>
            <div class="absolute top-3 right-3 bg-slate-900/80 hover:bg-slate-800 text-amber-300 text-xs px-3 py-1.5 rounded-lg border border-amber-500/30 flex items-center gap-1.5 shadow transition-all pointer-events-none">
              <span>🔍</span> Click Infographic for Fullscreen 2400x1400 View
            </div>
          </div>
        </div>

        <!-- 4-Box Focused Priority Breakdown Grid -->'''

if re.search(old_container_pattern, html):
    html = re.sub(old_container_pattern, new_container, html)

# Strip existing EMBEDDED_MAPS blocks
html = re.sub(r'// --- EMBEDDED SELF-CONTAINED ASSETS.*?const RAID_DATA = \[', 'const RAID_DATA = [', html, flags=re.DOTALL)

# Construct fresh JS injection with BOTH EMBEDDED_MAPS AND EMBEDDED_ICONS!
js_injection = "\n    // --- EMBEDDED SELF-CONTAINED ASSETS (ZERO EXTERNAL REQUESTS) ---\n"
js_injection += "    const EMBEDDED_MAPS = {\n"
for k, v in raid_maps_b64.items():
    js_injection += f'      {k}: "{v}",\n'
js_injection += "    };\n\n"

js_injection += "    const EMBEDDED_ICONS = {\n"
for k, v in item_icons_b64.items():
    js_injection += f'      "{k}": "{v}",\n'
js_injection += "    };\n\n"

html = html.replace("const RAID_DATA = [", js_injection + "    const RAID_DATA = [")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"CLEAN INJECTION SUCCESS: New HTML size: {os.path.getsize(HTML_PATH)/1024/1024:.2f} MB")
