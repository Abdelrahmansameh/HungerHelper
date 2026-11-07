import shutil
from universal_v8_engine import get_universal_skins

res = get_universal_skins("peasant's burden")
p = res['cards'][0]
dst = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\skin_spear_peasants_burden.jpg"
shutil.copyfile(p, dst)
print("Rendered and copied Peasant's Burden!")
