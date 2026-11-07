import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from universal_v8_engine import get_universal_skins

res = get_universal_skins("montre moi les skin de la rapier")
print("Query: 'montre moi les skin de la rapier'")
print("Found:", res["found"])
print("Title:", res["title"])
print("Text:\n", res["text"])
print("Cards:", res.get("cards"))
