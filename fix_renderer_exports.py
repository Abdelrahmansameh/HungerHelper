with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read().replace("\r\n", "\n")

extra_funcs = """

# ---------------------------------------------------------------------------
# DUNGEON CARD
# ---------------------------------------------------------------------------
def render_dungeon_card(dungeon_key: str = "jacques-folly", is_french: bool = True) -> str:
    from overhaul_all_cards import render_clean_dungeon_card
    return render_clean_dungeon_card(is_french)


# ---------------------------------------------------------------------------
# TALENT BUILD CARD
# ---------------------------------------------------------------------------
def render_talent_build_card(build_query: str = "", is_french: bool = True) -> str:
    from overhaul_all_cards import render_clean_talent_summary_card
    # Check if user asked for summary or full 5-tree
    if any(w in build_query.lower() for w in ["resume", "résumé", "selection", "selectionne", "pris"]):
        return render_clean_talent_summary_card()
    out_tree = os.path.join(OUT_DIR, "build_official_tree.jpg")
    if os.path.exists(out_tree):
        return out_tree
    from create_talent_tree_card import create_talent_tree_master_card
    return create_talent_tree_master_card()
"""

text += extra_funcs

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Added render_dungeon_card and render_talent_build_card back to card_renderer.py!")
