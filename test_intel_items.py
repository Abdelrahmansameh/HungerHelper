from co_pilot.companion_intel import get_companion_item_intel

for item in ["marengo", "drak", "lasher", "pricker", "bloat", "shambler", "heavy-ammunition"]:
    intel = get_companion_item_intel(item)
    print(f"Intel for '{item}':", intel)
