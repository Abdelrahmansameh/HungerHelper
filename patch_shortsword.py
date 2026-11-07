with open('co_pilot/game_knowledge.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    if any(w in lowered for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
    elif any(w in lowered for w in ["longsword", "long sword", "epee", "épée"]):
        w_slug, w_name = "longsword", "Longsword"'''

replacement = '''    if any(w in lowered for w in ["shortsword", "short-sword", "short sword", "épée courte", "epee courte"]):
        w_slug, w_name = "short-sword", "Short Sword"
    elif any(w in lowered for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
    elif any(w in lowered for w in ["longsword", "long sword", "epee", "épée"]):
        w_slug, w_name = "longsword", "Longsword"'''

text = text.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))
text = text.replace(target, replacement)

with open('co_pilot/game_knowledge.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed weapon order and added shortsword to game_knowledge.py!")
