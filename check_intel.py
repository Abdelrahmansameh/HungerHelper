with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for j in range(1115, min(len(lines), 1180)):
    print(f"{j+1}: {lines[j].rstrip().encode('ascii', 'replace').decode('ascii')}")
