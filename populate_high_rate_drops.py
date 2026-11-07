import sys, urllib.request, json, time
from bs4 import BeautifulSoup
import concurrent.futures
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    all_items = json.load(f)

# Load existing high_rate_drops if present
existing = {}
try:
    with open("data/high_rate_drops.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except:
    pass

schema_slugs = [k for k, v in all_items.items() if v.get("c") == "schema" or "recipe" in k or "schema" in k]
print(f"Total schemas to check: {len(schema_slugs)}")

def parse_schema_item(slug):
    # Specialized overrides
    if "peasant-s-burden" in slug:
        return slug, {
            "title": "Peasant's Burden - Spear",
            "slug": slug,
            "rarity": "Epic",
            "category": "Cosmetic Schema",
            "sell_copper": 18,
            "sell_display": "18 Copper",
            "mob_drops": ["Dreg Farmer (Always 100% drop on kill · Spawns 1 in 20 raids at Garnier's Farm, Sarlat Farm)"],
            "placed_drops": [],
            "vendor_buys": ["Not sold by merchants (Raid Mob Exclusive Drop)"],
            "unlocks": "Peasant's Burden appearance for Spear in Chateau Appearance menu",
            "summary_intel": [
                "• 💀 **Mob Drop :** Dreg Farmer (100% Always Drop · Garnier's Farm, Sarlat Farm)",
                "• 📍 **Spawn Intel :** Sarlat Farm (Courtyard North of buildings) · 1 in 20 raids",
                "• 🔓 **Unlock Rule :** Discover Schema in Chateau to add Peasant's Burden to Appearance menu.",
                "• 🪙 **Vendor Resale :** Sells to vendors for 18 Copper (Merchants do not sell this item)"
            ]
        }

    if "metallurgist-recipe-spear" in slug:
        return slug, {
            "title": "Metallurgist Recipe - Spear",
            "slug": slug,
            "rarity": "Epic",
            "category": "Crafting Recipe",
            "sell_copper": 9200,
            "sell_display": "9 Silver 20 Copper",
            "mob_drops": [],
            "placed_drops": ["Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)"],
            "vendor_buys": ["Henri at Chateau Hub (92 Silver)"],
            "unlocks": "Crafting Spear Lv 185 at Chateau Metallurgist",
            "summary_intel": [
                "• 📍 **Placed World Loot :** Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)",
                "• 🛒 **Merchant Stock :** Henri at Chateau Hub (92 Silver)",
                "• 🔨 **Crafting Unlock :** Unlocks Spear Lv 185 crafting at Metallurgist",
                "• 🪙 **Vendor Resale :** Sells to vendors for 9 Silver 20 Copper"
            ]
        }

    # If already parsed with good data, keep it unless incomplete
    if slug in existing and existing[slug].get("summary_intel") and not any("1/1.2 M" in x for x in str(existing[slug])):
        return slug, existing[slug]

    url = f"https://hunger-companion.com/items/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return slug, existing.get(slug)

    soup = BeautifulSoup(html, "html.parser")
    item_card_meta = all_items.get(slug, {})
    title = item_card_meta.get("t") or (soup.find("h1").text.strip() if soup.find("h1") else slug.replace("-", " ").title())
    rarity = item_card_meta.get("r", "rare").title()
    category = item_card_meta.get("c", "schema")
    sell_value = item_card_meta.get("v", 0)

    s_silver = sell_value // 100
    s_copper = sell_value % 100
    val_str = f"{s_silver} Silver {s_copper} Copper" if s_silver > 0 else f"{s_copper} Copper"

    mob_drops = []
    placed_drops = []
    vendor_buys = []
    unlocks = None

    text_all = soup.get_text(separator=" | ", strip=True)
    
    # Check unlocks
    for line in text_all.split(" | "):
        if "unlocks" in line.lower() or "learn this recipe" in line.lower() or "appearance menu" in line.lower():
            if len(line) < 120 and "previous" not in line.lower() and "next" not in line.lower():
                unlocks = line.strip()
                break

    # Look for Placed in the world
    for div in soup.find_all(["div", "section"]):
        t = div.get_text(separator=" | ", strip=True)
        if "Placed in the world" in t:
            for seg in t.split(" | "):
                if any(m in seg for m in ["Sarlat Farm", "Jacques Bridge", "Sombre Forest", "fixed spot"]):
                    if seg not in placed_drops:
                        placed_drops.append(seg)
        if "In vendor stock" in t or "From vendors" in t:
            for v_name in ["Henri", "Grillard", "Heinrich Voss", "Octave de Villiers", "Piro", "Reynauld", "Voyant the Rifleman"]:
                if v_name in t and v_name not in str(vendor_buys):
                    vendor_buys.append(v_name)
        if "Always" in t and "Best:" in t:
            mob_drops.append(t[:80])

    summary_intel = []
    if mob_drops:
        summary_intel.append(f"• 💀 **Mob Drop :** {mob_drops[0]}")
    if placed_drops:
        summary_intel.append(f"• 📍 **Placed World Loot :** {placed_drops[0]}")
    if vendor_buys:
        summary_intel.append(f"• 🛒 **Merchant Stock :** Available from {', '.join(vendor_buys)} at Chateau Hub")
    else:
        summary_intel.append("• 🛒 **Vendor Stock :** Not sold by merchants (Exclusive Raid Loot)")

    summary_intel.append(f"• 🪙 **Vendor Resale :** Sells to vendors for {val_str}")
    if unlocks:
        summary_intel.append(f"• 🔓 **Unlock Rule :** {unlocks}")

    return slug, {
        "title": title,
        "slug": slug,
        "rarity": rarity,
        "category": category,
        "sell_copper": sell_value,
        "sell_display": val_str,
        "mob_drops": mob_drops,
        "placed_drops": placed_drops,
        "vendor_buys": vendor_buys,
        "unlocks": unlocks,
        "summary_intel": summary_intel
    }

print("Fetching and validating schemas...")
results = {}
for i, s in enumerate(schema_slugs):
    slug, res = parse_schema_item(s)
    if res:
        results[slug] = res
    if (i + 1) % 25 == 0:
        print(f"Processed {i+1}/{len(schema_slugs)}...")
    time.sleep(0.05)

with open("data/high_rate_drops.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2, ensure_ascii=False)

print(f"Successfully compiled all {len(results)} high rate drops in data/high_rate_drops.json!")
