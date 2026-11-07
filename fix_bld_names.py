with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """def render_talent_build_card(build_query: str = "", is_french: bool = True) -> str:
    if any(w in build_query.lower() for w in ["resume", "résumé", "stat", "stats", "selection", "selectionne", "pris"]):
        return render_build_stats_summary_by_category()
    return render_build_all_trees_view()

def render_talent_build_cards_both(player_name: str = "Abdallah", level: int = 100):
    p1 = render_build_all_trees_view(player_name=player_name, level=level)
    p2 = render_build_stats_summary_by_category(player_name=player_name, level=level)
    return p1, p2"""

replacement = """def render_talent_build_card(build_query: str = "", is_french: bool = False) -> str:
    if any(w in build_query.lower() for w in ["resume", "résumé", "stat", "stats", "selection"]):
        return render_build_stats_summary_card(player_name="Abdallah")
    return render_all_5_mastery_trees_card(player_name="Abdallah")

def render_talent_build_cards_both(player_name: str = "Abdallah", level: int = 100):
    p1 = render_all_5_mastery_trees_card(player_name=player_name, level=level)
    p2 = render_build_stats_summary_card(player_name=player_name, level=level)
    return p1, p2"""

text_n = text.replace("\r\n", "\n")
target_n = target.replace("\r\n", "\n")
if target_n in text_n:
    text_n = text_n.replace(target_n, replacement)
    with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
        f.write(text_n)
    print("RENDER_BUILD_NAMES_UPDATED")
else:
    print("target_n not found")
