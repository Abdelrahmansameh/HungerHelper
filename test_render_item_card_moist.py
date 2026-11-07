from co_pilot.card_renderer import render_item_card, find_item_icon

ico = find_item_icon("moist pouch")
print("find_item_icon('moist pouch'):", ico)

p = render_item_card("Moist Pouch")
print("Rendered item card for Moist Pouch:", p)
