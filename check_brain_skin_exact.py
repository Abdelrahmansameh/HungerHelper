with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "is_skin_query =" in l:
        for j in range(i-2, i+18):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
