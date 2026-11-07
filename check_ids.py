with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

for id_name in ['map-phase-badge', 'map-title', 'map-key-badge', 'brief-giver', 'brief-quest-name', 'brief-desc', 'brief-multi-turnin', 'btn-complete-quest', 'focus-breakdown', 'tactical-steps', 'container-targets', 'mob-targets', 'tactical-img', 'hub-overlay', 'hub-overlay-title', 'hub-overlay-desc']:
    print(f"{id_name}: {'FOUND' if f'id=\"{id_name}\"' in s else 'MISSING!'}")
