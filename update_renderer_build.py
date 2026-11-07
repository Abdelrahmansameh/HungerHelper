import os

p = "co_pilot/card_renderer.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("\r\n", "\n")

idx = text.find("def render_dungeon_card(")
if idx != -1:
    end_part = """def render_dungeon_card(dungeon_key: str = "jacques-folly", is_french: bool = True) -> str:
    return render_clean_dungeon_card(is_french)


# ---------------------------------------------------------------------------
# TALENT BUILD CARDS (IMAGE 1: 5-TREES VIEW, IMAGE 2: STATS SUMMARY BY CATEGORY)
# ---------------------------------------------------------------------------
def render_talent_build_card(build_query: str = "", is_french: bool = True) -> str:
    if any(w in build_query.lower() for w in ["resume", "résumé", "stat", "stats", "selection", "selectionne", "pris"]):
        return render_build_stats_summary_by_category()
    return render_build_all_trees_view()

def render_talent_build_cards_both(player_name: str = "Abdallah", level: int = 100):
    p1 = render_build_all_trees_view(player_name=player_name, level=level)
    p2 = render_build_stats_summary_by_category(player_name=player_name, level=level)
    return p1, p2
"""
    new_text = text[:idx] + end_part
    with open(p, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("SUCCESS: Updated card_renderer.py with clean build renderers.")
else:
    print("idx not found")
