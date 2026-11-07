# -*- coding: utf-8 -*-
with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

old_c_data = '''CREATURES_DATA = {
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
}'''

new_c_data = '''CREATURES_DATA = {
    "drooler": {
        "name_en": "Drooler", "name_fr": "Baveux (Drooler)", "health": 450, "damage": 36,
        "category": "Menace Acide à Distance", "speed": "Rapide (Sprint)",
        "tactics_fr": "Garder ses distances pour éviter le crachat d'acide corrosif et frapper rapidement d'estoc.",
        "drops_fr": "Mâchoire de Baveux (85%), Bile Corrosive", "drops_en": "Drooler Jaw, Corrosive Bile"
    },
    "brute": {
        "name_en": "Brute", "name_fr": "Brute Élite", "health": 900, "damage": 68,
        "category": "Menace Élite Lente", "speed": "Lente (Charge lourde)",
        "tactics_fr": "Vulnérable aux frappes d'estoc critiques dans le dos (x2). Ne jamais parer de face.",
        "drops_fr": "Pied de Brute (85%), Os Épais", "drops_en": "Brute Foot, Thick Bone"
    },
    "pitchskin": {
        "name_en": "Pitchskin", "name_fr": "Peau-de-Poix (Miniboss)", "health": 1400, "damage": 75,
        "category": "Miniboss de Raid", "speed": "Moyenne",
        "tactics_fr": "Sensible aux attaques d'estoc et tirs à distance.",
        "drops_fr": "Peau de Poix Épaisse, Échantillon d'Hémoglobine", "drops_en": "Pitchskin Hide, Blood Sample"
    },
    "pale-lady": {
        "name_en": "Pale Lady", "name_fr": "Dame Pâle (Miniboss)", "health": 1200, "damage": 65,
        "category": "Miniboss Téléporteur", "speed": "Téléportation",
        "tactics_fr": "Interrompre ses incantations avec des frappes lourdes.",
        "drops_fr": "Voile Pâle, Poussière d'Opium Scellée", "drops_en": "Pale Veil, Sealed Opium Dust"
    }
}'''

assert old_c_data in text, "old_c_data not found"
text = text.replace(old_c_data, new_c_data, 1)

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated CREATURES_DATA with speed & drops.")
