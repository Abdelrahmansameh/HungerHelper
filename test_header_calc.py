import perfect_briefings_core_v23 as core

CANVAS_W = 2400
HEADER_H = 78
start_x = 184
end_x = CANVAS_W - 24 # 2376
total_w = end_x - start_x # 2192
gap = 14
num_cards = 7
card_w = (total_w - (num_cards - 1) * gap) // num_cards
print(f"start_x: {start_x}, end_x: {end_x}, total_w: {total_w}")
print(f"card_w: {card_w}, gap: {gap}")
for i in range(7):
    cx = start_x + i * (card_w + gap)
    print(f"  Card {i+1}: cx={cx} to {cx+card_w}")
