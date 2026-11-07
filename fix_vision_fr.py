with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "    api_key = get_gemini_api_key()"
replacement = """    is_french = any(w in (user_query or "").lower() for w in ["en français", "en francais", "in french"])
    api_key = get_gemini_api_key()"""

if target in text:
    new_text = text.replace(target, replacement, 1)
    with open("co_pilot/vision_analyzer.py", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("IS_FRENCH_ADDED_TO_VISION")
else:
    print("target not found")
