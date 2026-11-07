from co_pilot.card_renderer import find_item_icon
from PIL import Image
import os

im = find_item_icon("moist pouch")
print("find_item_icon returned size:", im.size, "mode:", im.mode)

im_ui = Image.open("assets/items/T_UI_Item_MoistPouch.png")
print("T_UI_Item_MoistPouch.png size:", im_ui.size)

im_render = Image.open("assets/items/ID_HipBag_Common01.webp")
print("ID_HipBag_Common01.webp size:", im_render.size)
