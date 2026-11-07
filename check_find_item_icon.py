with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def find_item_icon" in line or "find_item_icon" in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(i, min(len(lines), i+45)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
