# -*- coding: utf-8 -*-
with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

c_data_code = '''
CREATURES_DATA = {
    "drooler": {
        "name_en": "Drooler", "name_fr": "Baveux (Drooler)", "health": 450, "damage": 36,
        "category": "Menace Acide à Distance",
        "tactics_fr": "Garder ses distances pour éviter le crachat d'acide corrosif et frapper rapidement d'estoc."
    },
    "brute": {
        "name_en": "Brute", "name_fr": "Brute Élite", "health": 900, "damage": 68,
        "category": "Menace Élite Lente",
        "tactics_fr": "Vulnérable aux frappes d'estoc critiques dans le dos (x2). Ne jamais parer de face."
    },
    "pitchskin": {
        "name_en": "Pitchskin", "name_fr": "Peau-de-Poix (Miniboss)", "health": 1400, "damage": 75,
        "category": "Miniboss de Raid",
        "tactics_fr": "Sensible aux attaques d'estoc et tirs à distance."
    },
    "pale-lady": {
        "name_en": "Pale Lady", "name_fr": "Dame Pâle (Miniboss)", "health": 1200, "damage": 65,
        "category": "Miniboss Téléporteur",
        "tactics_fr": "Interrompre ses incantations avec des frappes lourdes."
    }
}
'''

text = c_data_code + "\n" + text
with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("CREATURES_DATA added successfully.")
