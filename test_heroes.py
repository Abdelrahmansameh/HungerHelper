from co_pilot.brain import CoPilotBrain
b = CoPilotBrain()
for hero in ["eva", "gabriel", "hugo", "otto", "serine"]:
    res = b.process_message("test_user", "Abdallah", f"fiche personnage {hero}")
    print(hero, "->", res.get("image_attachment"))
