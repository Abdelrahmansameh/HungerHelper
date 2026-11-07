with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(145, 170):
    print(f"{i+1}: {lines[i].rstrip()}")
