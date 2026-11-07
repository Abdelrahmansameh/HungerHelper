import os, io, base64, re
from PIL import Image

ART_DIR = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"
ITEM_DIR = os.path.join(ART_DIR, "assets", "items")
HTML_PATH = os.path.join(ART_DIR, "eloise_raid_planner.html")

print("1. Encoding 7 Raid Map Briefings to Base64 (Crisp 1920x1120)...")
raid_maps_b64 = {}
for i in range(1, 8):
    p = os.path.join(ART_DIR, f"raid{i}_map.jpg")
    im = Image.open(p).resize((1920, 1120), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82, optimize=True)
    b64_str = base64.b64encode(buf.getvalue()).decode("ascii")
    raid_maps_b64[i] = f"data:image/jpeg;base64,{b64_str}"
    print(f"  Raid {i}: {len(buf.getvalue())/1024:.1f} KB")

print("2. Encoding 9 Item Icons to Base64...")
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

# Strip any existing EMBEDDED_MAPS blocks
html = re.sub(r'// --- EMBEDDED SELF-CONTAINED ASSETS.*?const RAID_DATA = \[', 'const RAID_DATA = [', html, flags=re.DOTALL)

# Strip old tactical-img src base64
html = re.sub(r'id="tactical-img"\s+src="[^"]*"', 'id="tactical-img" src=""', html)

# Construct fresh JS injection
js_injection = "\n    // --- EMBEDDED SELF-CONTAINED ASSETS (ZERO EXTERNAL REQUESTS) ---\n"
js_injection += "    const EMBEDDED_MAPS = {\n"
for k, v in raid_maps_b64.items():
    js_injection += f'      {k}: "{v}",\n'
js_injection += "    };\n\n"

js_injection += "    const EMBEDDED_ICONS = {\n"
for k, v in item_icons_b64.items():
    js_injection += f'      "{k}": "{v}",\n'
js_injection += "    };\n\n"

html = html.replace('id="tactical-img" src=""', f'id="tactical-img" src="{raid_maps_b64[1]}"')
html = html.replace("const RAID_DATA = [", js_injection + "    const RAID_DATA = [")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"CLEAN WRITE SUCCESS: File size: {os.path.getsize(HTML_PATH)/1024/1024:.2f} MB")
