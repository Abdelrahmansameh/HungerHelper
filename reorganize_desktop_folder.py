import os
import shutil

desktop = r"C:\Users\PC\Desktop"
old_folder = os.path.join(desktop, "Hunger_Raid_Maps")
new_folder = os.path.join(desktop, "Hunger_Helper")

if os.path.exists(old_folder) and not os.path.exists(new_folder):
    os.rename(old_folder, new_folder)
    print(f"Renamed {old_folder} -> {new_folder}")
elif os.path.exists(old_folder) and os.path.exists(new_folder):
    print(f"Both exist, merging into {new_folder}")
    for item in os.listdir(old_folder):
        s = os.path.join(old_folder, item)
        d = os.path.join(new_folder, item)
        if not os.path.exists(d):
            shutil.move(s, d)
    os.rmdir(old_folder)
else:
    print(f"Target folder {new_folder} already exists or old folder not found.")

print("Current contents of Hunger_Helper on Desktop:")
for item in os.listdir(new_folder):
    print(" -", item)
