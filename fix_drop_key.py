# -*- coding: utf-8 -*-
with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('"drops_fr":', '"drop_fr":')
text = text.replace('"drops_en":', '"drop_en":')

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated drop_fr and drop_en.")
