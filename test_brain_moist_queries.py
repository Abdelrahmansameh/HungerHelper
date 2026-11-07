import sys
sys.stdout.reconfigure(encoding="utf-8")
from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

print("--- Testing 'montre moi moist pouch' ---")
res1 = brain.process_message("user123", "Abdallah", "montre moi moist pouch")
print("Spoken:", res1.get("spoken_text"))
print("Display:\n", res1.get("display_text"))
print("Image:", res1.get("image_attachment"))

print("\n--- Testing 'moist pouch sert a craft quel skin' ---")
res2 = brain.process_message("user123", "Abdallah", "moist pouch sert a craft quel skin")
print("Spoken:", res2.get("spoken_text"))
print("Display:\n", res2.get("display_text"))
print("Image:", res2.get("image_attachment"))
