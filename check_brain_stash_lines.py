import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "render_stash_report_card" in l or "render_stash_two_images" in l or "stash_report" in l:
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j].rstrip()}")
        print("="*40)
