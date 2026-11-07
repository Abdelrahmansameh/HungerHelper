import os
import shutil

base = r"C:\Users\PC\Desktop\Hunger_Helper"

p1 = os.path.join(base, "01_Raid_Planner_and_Maps")
p2 = os.path.join(base, "02_Merchant_Quests_Guide")
p3 = os.path.join(base, "03_Mastery_Build_Planner")

os.makedirs(p1, exist_ok=True)
os.makedirs(p2, exist_ok=True)
os.makedirs(p3, exist_ok=True)

# 1. Raid Planner and Maps
raid_files = [
    "eloise_raid_planner.html",
    "raid1_map.jpg", "raid2_map.jpg", "raid3_map.jpg",
    "raid4_map.jpg", "raid5_map.jpg", "raid6_map.jpg", "raid7_map.jpg",
    "Raid_1_Versions"
]

for f in raid_files:
    src = os.path.join(base, f)
    dst = os.path.join(p1, f)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)
        print(f"Moved {f} -> {p1}")

# 2. Merchant Quests Guide
merchant_files = [
    "merchant_procurement_guide.html",
    "merchant_quest_items_guide.png"
]

for f in merchant_files:
    src = os.path.join(base, f)
    dst = os.path.join(p2, f)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)
        print(f"Moved {f} -> {p2}")

# 3. Mastery Build Planner
mastery_source = r"C:\Users\PC\Documents\HungerHelper"
mastery_files = [
    "mastery_build_summary.png",
    "mastery_build_card.html"
]

for f in mastery_files:
    src = os.path.join(mastery_source, f)
    dst = os.path.join(p3, f)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {f} -> {p3}")

# Also copy mastery_build_summary.png directly to root of Hunger_Helper so it's instantly visible upon opening
root_img_copy = os.path.join(base, "mastery_build_summary.png")
shutil.copyfile(os.path.join(mastery_source, "mastery_build_summary.png"), root_img_copy)
print(f"Copied mastery_build_summary.png to root: {root_img_copy}")

print("\nFinal structure of Hunger_Helper on Desktop:")
for root, dirs, files in os.walk(base):
    rel = os.path.relpath(root, base)
    indent = "  " * (0 if rel == "." else rel.count(os.sep) + 1)
    if rel != ".":
        print(f"{indent}📁 {os.path.basename(root)}/")
    for fl in files:
        f_indent = "  " * (1 if rel == "." else rel.count(os.sep) + 2)
        print(f"{f_indent}📄 {fl}")
