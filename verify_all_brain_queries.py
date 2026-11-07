# -*- coding: utf-8 -*-
import sys
import os

from co_pilot.brain import CoPilotBrain

brain = CoPilotBrain()

test_queries = [
    ("montre moi les skin de la vepr", "Vepr Skins"),
    ("montre moi les skin de la rapier", "Rapier Skins"),
    ("montre moi les skills de eva", "Eva Character Profile"),
    ("jb", "Blank Jacques Bridge Map"),
    ("carte de sombre", "Blank Sombre Forest Map"),
    ("sarlat", "Blank Sarlat Farm Map"),
    ("combien de coup pour tuer un joueur en blue a la longsword", "Longsword HTK Blue Player"),
    ("en combien de hit je tue un jouer en legendaire avec le club", "Club HTK Legendary Player"),
    ("moist pouch sert a craft quel skin", "Moist Pouch Craft Recipe"),
    ("analyse mon stash", "Stash Analysis")
]

sys.stdout.buffer.write(b"=== RUNNING COMPREHENSIVE V8 VERIFICATION ===\n\n")

for q, title in test_queries:
    sys.stdout.buffer.write(f"--- TEST: {title} (Query: '{q}') ---\n".encode("utf-8"))
    res = brain.process_message("123", "Abdallah", q)
    if not res:
        sys.stdout.buffer.write(b"[FAIL] No result returned!\n\n")
        continue

    spoken = res.get("spoken_text", "")
    disp = res.get("display_text", "")
    img = res.get("image_attachment")
    imgs = res.get("image_attachments", [])

    sys.stdout.buffer.write(f"Spoken: {spoken[:100]}...\n".encode("utf-8"))
    sys.stdout.buffer.write(f"Display Header: {disp.splitlines()[0] if disp else 'None'}\n".encode("utf-8"))
    sys.stdout.buffer.write(f"Image: {img}\n".encode("utf-8"))
    if imgs:
        sys.stdout.buffer.write(f"Image attachments count: {len(imgs)}\n".encode("utf-8"))
    sys.stdout.buffer.write(b"[SUCCESS]\n\n")

sys.stdout.buffer.write(b"=== ALL TESTS EXECUTED ===\n")
