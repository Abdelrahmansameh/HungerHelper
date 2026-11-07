import json, re

with open("data/high_rate_drops.json", "r", encoding="utf-8") as f:
    drops = json.load(f)

for slug, data in drops.items():
    # Filter mob drops
    clean_mobs = []
    for m in data.get("mob_drops", []):
        m_low = m.lower()
        if "1/1.2 m" in m_low or "m" in m_low or "1/60" in m_low or "1/10" in m_low or "1/11" in m_low or "1/9" in m_low:
            continue
        if any(h in m_low for h in ["always", "100%", "high", "guaranteed", "best: dreg farmer"]) or (re.search(r'1/[1-9]\b', m_low) and not "m" in m_low):
            clean_mobs.append(m)
    data["mob_drops"] = clean_mobs

    # Filter placed drops
    clean_placed = []
    for p in data.get("placed_drops", []):
        if any(h in p for h in ["sarlat farm", "dupo farrier", "jacques bridge", "sombre forest", "1/"]):
            clean_placed.append(p)
    data["placed_drops"] = clean_placed

    # Summary intel rebuild
    summary = []
    if clean_mobs:
        summary.append(f"• 💀 **Mob Drop :** {clean_mobs[0]}")
    if clean_placed:
        summary.append(f"• 📍 **Placed World Loot :** {clean_placed[0]}")
    if data.get("vendor_buys") and not "not sold" in str(data["vendor_buys"]).lower():
        summary.append(f"• 🛒 **Merchant Stock :** Available from {', '.join(data['vendor_buys'])} at Chateau Hub")
    else:
        summary.append("• 🛒 **Vendor Stock :** Not sold by merchants (Raid Loot Exclusive)")
    
    val_disp = data.get("sell_display", "Copper")
    summary.append(f"• 🪙 **Vendor Resale :** Sells to vendors for {val_disp}")
    if data.get("unlocks"):
        summary.append(f"• 🔓 **Unlock Rule :** {data['unlocks']}")
    
    data["summary_intel"] = summary

with open("data/high_rate_drops.json", "w", encoding="utf-8") as f:
    json.dump(drops, f, indent=2, ensure_ascii=False)

print("high_rate_drops.json cleaned of low-rate clutter!")
