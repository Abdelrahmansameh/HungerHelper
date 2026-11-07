with open("co_pilot/core.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "ITEM_IMGS" in line or "CONTAINER_IMGS" in line:
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
