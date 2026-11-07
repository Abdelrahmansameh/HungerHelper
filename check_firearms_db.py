from universal_v8_engine import FIREARMS_DATABASE
print("Firearms in FIREARMS_DATABASE:")
for k, v in FIREARMS_DATABASE.items():
    print(f" - {k}: {v.get('name')} | Dmg: {v.get('damage')} | HS: {v.get('headshot')} | Ammo: {v.get('ammo')}")
