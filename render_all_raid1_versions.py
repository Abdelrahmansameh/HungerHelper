import os, sys, shutil

out_dir = r"C:\Users\PC\Desktop\Hunger_Raid_Maps\Raid_1_Versions"
os.makedirs(out_dir, exist_ok=True)
art_dir = r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee"

# 1. Current Latest (v25)
import generate_perfect_briefings_v25 as g25
g25.render_briefing(g25.RAIDS_CONFIG[0])
shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v25_latest_perfected.jpg"))
print("Rendered v25 latest perfected.")

# 2. V24 (Full Width Header + Big Badges)
try:
    import generate_perfect_briefings_v24 as g24
    g24.render_briefing(g24.RAIDS_CONFIG[0])
    shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v24_full_header.jpg"))
    print("Rendered v24 full header.")
except Exception as e:
    print("v24 error:", e)

# 3. V22 (Top-Right Header + Item Thumbnails)
try:
    import generate_perfect_briefings_v22 as g22
    g22.render_briefing(g22.RAIDS_CONFIG[0])
    shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v22_item_thumbnails.jpg"))
    print("Rendered v22 item thumbnails.")
except Exception as e:
    print("v22 error:", e)

# 4. V20 (Hunger Companion Dark Theme + In-Map HUD)
try:
    import generate_perfect_briefings_v20 as g20
    g20.render_briefing(g20.RAIDS_CONFIG[0])
    shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v20_inmap_hud.jpg"))
    print("Rendered v20 inmap hud.")
except Exception as e:
    print("v20 error:", e)

# 5. V13 (Letter Markers & Speedrun HUD)
try:
    import generate_perfect_briefings_v13 as g13
    g13.render_briefing(g13.RAIDS_CONFIG[0])
    shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v13_letter_markers.jpg"))
    print("Rendered v13 letter markers.")
except Exception as e:
    print("v13 error:", e)

# 6. V6 (Early Tactical Blueprint Pins)
try:
    import generate_perfect_briefings_v6 as g6
    g6.render_briefing(g6.RAIDS_CONFIG[0])
    shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), os.path.join(out_dir, "raid1_v6_early_blueprint.jpg"))
    print("Rendered v6 early blueprint.")
except Exception as e:
    print("v6 error:", e)

# Restore latest v25 to art_dir and project folder so raid1_map.jpg remains the latest!
g25.render_briefing(g25.RAIDS_CONFIG[0])
shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), r"C:\Users\PC\Documents\HungerHelper\Raid_Maps\raid1_map.jpg")
shutil.copy(os.path.join(art_dir, "raid1_map.jpg"), r"C:\Users\PC\Desktop\Hunger_Raid_Maps\raid1_map.jpg")
print("Restored v25 to main locations.")
