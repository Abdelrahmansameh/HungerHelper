with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read().replace("\r\n", "\n")

text = text.replace('quest_qty = "10x requis pour Denis"', 'quest_qty = "10x requis pour Éloïse"')
text = text.replace('quest_giver = "Denis le Meunier"', 'quest_giver = "Éloïse (Château Hub)"')

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Denis replaced with Éloïse in card_renderer.py!")
