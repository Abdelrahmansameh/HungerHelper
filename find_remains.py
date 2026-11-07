with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "FICHE TECHNIQUE DE MISSION" in line:
        for j in range(max(0, i-25), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j].rstrip().encode('ascii', 'replace').decode('ascii')}")
