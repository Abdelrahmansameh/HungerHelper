import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("test_mastery_cards_v2.py", "r", encoding="utf-8") as f:
    for i in range(35):
        print(f"{i+1}: {f.readline().rstrip()}")
