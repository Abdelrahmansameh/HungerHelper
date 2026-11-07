import urllib.request
import json

headers = {"User-Agent": "Mozilla/5.0"}
urls = [
    "https://hunger-companion.com/api/item-card/peasant-s-burden-spear",
    "https://hunger-companion.com/api/item-card/metallurgist-recipe-spear",
    "https://hunger-companion.com/api/item-card/heavy-ammunition"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            print(f"[OK] {u} -> Len: {len(data)}")
            try:
                js = json.loads(data)
                print("  Keys:", list(js.keys()) if isinstance(js, dict) else type(js))
                print("  Sample:", json.dumps(js, indent=2)[:300])
            except:
                print("  Raw:", data[:200])
    except Exception as e:
        print(f"[FAIL] {u} -> {e}")
