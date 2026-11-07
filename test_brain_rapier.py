import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from co_pilot.brain import HungerBrain

brain = HungerBrain()
res = brain.process_query("montre moi les skin de la rapier")
print("Brain response for 'montre moi les skin de la rapier':")
print("Spoken:", res.get("spoken_text"))
print("Display:", res.get("display_text"))
print("Attachment:", res.get("image_attachment"))
print("Attachments:", res.get("image_attachments"))
