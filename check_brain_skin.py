with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "skin" in line.lower() or "cosmetic" in line.lower() or "craft" in line.lower():
        print(f"Line {i+1}: {line.strip()[:100]}")
