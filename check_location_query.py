import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def answer_location_query")
print(text[idx:idx+1500])
