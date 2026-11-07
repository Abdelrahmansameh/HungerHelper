with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    html = f.read()

# Hide redundant keyBadge if not needed
html = html.replace("keyBadge.textContent = data.keyBadge;", "if (data.keyBadge && data.keyBadge !== 'No Keys Needed' && data.keyBadge !== 'Bring No Keys' && !data.keyBadge.includes('Zero Keys Needed')) { keyBadge.textContent = data.keyBadge; keyBadge.classList.remove('hidden'); } else { keyBadge.classList.add('hidden'); }")

with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated eloise_raid_planner.html to hide redundant key badge.")
