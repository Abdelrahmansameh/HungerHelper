with open('co_pilot/game_knowledge.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}\n\n# ---------------------------------------------------------------------------\n# 11. COMBAT TTK & HIT CALCULATOR'
replacement = '    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path, "image_attachments": [p1, p2]}\n\n# ---------------------------------------------------------------------------\n# 11. COMBAT TTK & HIT CALCULATOR'

text = text.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))
text = text.replace(target, replacement)

with open('co_pilot/game_knowledge.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Line 694 in game_knowledge.py successfully restored with [p1, p2]!")
