with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:100]):
    if "is_french" in l:
        print(f"Line {i+1}: {l.strip()}")
