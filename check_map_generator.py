import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/map_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_location_poi_map")
print(text[idx:idx+1500])
