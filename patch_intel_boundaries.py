with open("co_pilot/companion_intel.py", "r", encoding="utf-8") as f:
    code = f.read()

target_block = '''def normalize_query_to_slug(query: str) -> str:
    """Resolve user query string to clean companion item slug."""
    clean = query.lower().strip()
    clean = re.sub(r'^(combien\\s+se\\s+vend|combien\\s+coute|combien\\s+vaut|prix\\s+de|prix\\s+du|fiche\\s+de|stats\\s+du|stats\\s+de|le|la|les|un|une|l\')\\s+', '', clean).strip()
    
    if clean in ITEM_ALIASES:
        return ITEM_ALIASES[clean]
        
    for k in sorted(ITEM_ALIASES.keys(), key=len, reverse=True):
        if k in clean:
            return ITEM_ALIASES[k]
            
    # Try slugifying
    return clean.replace(" ", "-").replace("'", "-")'''

new_norm_func = '''def normalize_query_to_slug(query: str) -> str:
    """Resolve user query string to clean companion item slug with strict word boundaries."""
    clean = query.lower().strip()
    clean = re.sub(r'^(combien\\s+se\\s+vend|combien\\s+coute|combien\\s+vaut|prix\\s+de|prix\\s+du|fiche\\s+de|stats\\s+du|stats\\s+de|le|la|les|un|une|l\')\\s+', '', clean).strip()
    
    clean_spaced = clean.replace("-", " ")
    if clean in ITEM_ALIASES:
        return ITEM_ALIASES[clean]
    if clean_spaced in ITEM_ALIASES:
        return ITEM_ALIASES[clean_spaced]
        
    for k in sorted(ITEM_ALIASES.keys(), key=len, reverse=True):
        k_spaced = k.replace("-", " ")
        if re.search(r'\\b' + re.escape(k_spaced) + r'\\b', clean_spaced):
            return ITEM_ALIASES[k]
            
    # Try slugifying
    return clean.replace(" ", "-").replace("'", "-")'''

if target_block in code:
    code = code.replace(target_block, new_norm_func)
    print("Replaced normalize_query_to_slug via string replace!")
else:
    print("Target block not matched exactly, let's find start and end:")
    p_start = code.find("def normalize_query_to_slug(")
    p_end = code.find("def fetch_and_cache_companion_item(")
    if p_start != -1 and p_end != -1:
        code = code[:p_start] + new_norm_func + "\n\n" + code[p_end:]
        print("Replaced via index slice!")

old_get_intel = '''def get_companion_item_intel(query_or_slug: str) -> Optional[Dict[str, Any]]:
    """
    Look up item intelligence:
    1. Check SQLite companion_items_cache.
    2. If not found, fetch live from hunger-companion.com and cache.
    """
    slug = normalize_query_to_slug(query_or_slug)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM companion_items_cache WHERE slug = ? LIMIT 1", (slug,))
    row = cur.fetchone()'''

new_get_intel = '''def get_companion_item_intel(query_or_slug: str) -> Optional[Dict[str, Any]]:
    """
    Look up item intelligence:
    1. Check SQLite companion_items_cache directly by raw slug or normalized slug.
    2. If not found, fetch live from hunger-companion.com and cache.
    """
    raw_slug = query_or_slug.lower().strip()
    slug = normalize_query_to_slug(query_or_slug)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Try exact raw slug, then normalized slug
    cur.execute("SELECT * FROM companion_items_cache WHERE slug = ? OR slug = ? LIMIT 1", (raw_slug, slug))
    row = cur.fetchone()'''

if old_get_intel in code:
    code = code.replace(old_get_intel, new_get_intel)
    print("Replaced get_companion_item_intel!")

with open("co_pilot/companion_intel.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated companion_intel.py!")
