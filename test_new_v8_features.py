import universal_v8_engine as v8

p_bloat = v8.render_universal_creature_card("bloater")
print("Bloater card:", p_bloat)

p_shambler = v8.render_universal_creature_card("shambler")
print("Shambler card:", p_shambler)

p_marengo = v8.render_pure_english_firearm_card("marengo")
print("Marengo card:", p_marengo)

p_drak = v8.render_pure_english_firearm_card("drak")
print("Drak card:", p_drak)

p_lasher = v8.render_pure_english_firearm_card("lasher")
print("Lasher card:", p_lasher)

p_2h = v8.render_two_handed_melee_overview_card()
print("2H Melee card:", p_2h)

p_quest = v8.render_dynamic_quest_contract_card("down-from-mount-sinai")
print("Quest card:", p_quest)
