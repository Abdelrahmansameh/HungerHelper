import json

data = json.load(open("data/all_tracker_data.json", encoding="utf-8"))
print("Keys in all_tracker_data:", list(data.keys()) if isinstance(data, dict) else len(data))

if isinstance(data, dict):
    for k, v in data.items():
        for term in ["marengo", "drak", "lasher", "pricker", "bloat", "shambler"]:
            if term in k.lower():
                print(f"Matched key '{k}' for term '{term}':", str(v)[:200])
