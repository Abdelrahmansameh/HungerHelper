import universal_v8_engine as v8

print("Universal V8 Engine attributes:")
for attr in dir(v8):
    if not attr.startswith("__"):
        print(f" - {attr}")
