from co_pilot.game_knowledge import answer_combat_ttk_query

import sys

q1 = "combien de coup pour tuer un joueur en blue a la longsword"
res1 = answer_combat_ttk_query(q1, is_french=False)
sys.stdout.buffer.write(f"Q1 Result:\nSpoken: {res1['spoken_text']}\nDisplay: {res1['display_text']}\nImage: {res1['image_attachment']}\n\n".encode("utf-8"))

q2 = "en combien de hit je tue un jouer en legendaire avec le club"
res2 = answer_combat_ttk_query(q2, is_french=False)
sys.stdout.buffer.write(f"Q2 Result:\nSpoken: {res2['spoken_text']}\nDisplay: {res2['display_text']}\nImage: {res2['image_attachment']}\n\n".encode("utf-8"))

