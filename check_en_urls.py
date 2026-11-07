import json

data = json.load(open("en_urls.json", encoding="utf-8"))
for item in data:
    url = item if isinstance(item, str) else str(item)
    for term in ["marengo", "drak", "lash", "pricker", "bloat", "shambler"]:
        if term in url.lower():
            print(f"Matched {term}: {url}")
