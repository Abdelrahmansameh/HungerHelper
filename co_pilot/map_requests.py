"""Resolve explicit map requests before informational/card keyword handlers.

A failed lookup is a text answer, never a request to send a previous artifact.
"""
import re
import sqlite3
from co_pilot import map_generator as maps

MAP_ALIASES = {
    'Sarlat Farm': ('sarlat farm', 'ferme de sarlat', 'sarlat', 'sf'),
    'Jacques Bridge': ('jacques bridge', 'pont jacques', 'jacques', 'jb'),
    'Sombre Forest': ('sombre forest', 'forêt sombre', 'foret sombre', 'sombre'),
}
CREATURES = {
    'farmer dreg': ('farmer dreg', 'dreg farmer', 'dreg fermier', 'fermier dreg'),
    'pale lady': ('pale lady', 'dame pâle', 'dame pale'),
    'drooler': ('drooler', 'droolers', 'baveux', 'drawler'),
    'brute': ('brute', 'brutes'),
    'bloat': ('bloat', 'bloats', 'bloater', 'bloaters', 'boursouflé', 'boursoufle'),
    'shambler': ('shambler', 'shamblers', 'titubant'),
    'dreg': ('dreg', 'dregs', 'rebut'),
}
DUNGEONS = {'the pit': ('the pit', 'pit', 'puits'),
            'the undercroft': ('the undercroft', 'undercroft', 'sous-sol', 'crypte'),
            'jacques folly': ('jacques folly', 'folly')}
DUNGEON_MAPS = {'the pit': 'Sombre Forest', 'the undercroft': 'Sarlat Farm', 'jacques folly': 'Jacques Bridge'}
TRANSLATIONS = {'farine': 'flour', 'charbon': 'charcoal', 'salpêtre': 'saltpetre', 'salpetre': 'saltpetre', 'miel': 'honey', 'os': 'bone', 'pain': 'bread'}


def contains(text, phrase):
    return re.search(r'(?<!\w)' + re.escape(phrase) + r'(?!\w)', text) is not None


def remove(text, phrases):
    for phrase in sorted(phrases, key=len, reverse=True):
        text = re.sub(r'(?<!\w)' + re.escape(phrase) + r'(?!\w)', ' ', text)
    return ' '.join(text.split()).strip(' ?!.,')


def reply(message):
    return {'spoken_text': message, 'display_text': message}


def handle_map_request(text, previous=None):
    """Return (response, successful context), or None for a non-map question."""
    q = text.lower().strip(' ?!.,')
    previous = previous or {}
    exact_map = any(q in aliases for aliases in MAP_ALIASES.values())
    explicit_followup = bool(re.search(r'\b(same|that|this|again|it|même|cette)\b', q))
    if not (re.search(r'\b(map|maps|carte|cartes|plan|route|routes)\b', q) or exact_map or 'speedrun' in q or 'speed run' in q or
            (explicit_followup and re.search(r'\b(show|send|generate|montre|envoie)\b', q))):
        return None

    def fail(message):
        return reply(message), None

    if re.search(r'\b(explain|mean|meaning|explique|représente|represente)\b', q):
        if not previous or not explicit_followup:
            return fail('No map has been generated yet. Which map and objective do you mean?')
        if any(any(contains(q, a) for a in aliases) and name != previous.get('map_name')
               for name, aliases in MAP_ALIASES.items()):
            return fail('Please generate that map first so I can explain its actual markers.')
        return fail(previous.get('points_description', 'No marker details available.'))

    # Resolve dungeon names first so "Jacques Folly" does not imply Jacques Bridge twice.
    dungeon_hits = [name for name, aliases in DUNGEONS.items() if any(contains(q, a) for a in aliases)]
    map_text = remove(q, [a for name in dungeon_hits for a in DUNGEONS[name]])
    map_hits = [name for name, aliases in MAP_ALIASES.items() if any(contains(map_text, a) for a in aliases)]
    if len(map_hits) > 1 or len(dungeon_hits) > 1:
        return fail('Please request one map or dungeon at a time.')
    target_map = map_hits[0] if map_hits else None
    qualifier = re.search(r"\b(?:on|sur|dans)\s+(.+)$", map_text)
    if qualifier and not target_map:
        return fail(f"Unknown map: {qualifier.group(1)}. Please specify Sarlat Farm, Jacques Bridge, or Sombre Forest.")
    remaining = remove(map_text, [a for aliases in MAP_ALIASES.values() for a in aliases])
    remaining = remove(remaining, ['make me', 'show me', 'give me', 'send me', 'montre moi', 'donne moi',
        'could you', 'can you', 'i want', 'i need', 'please', 'a', 'an', 'the', 'of', 'for', 'on', 'in', 'at', 'to',
        'make', 'generate', 'show', 'send', 'display', 'post', 'map', 'maps', 'carte', 'cartes', 'plan', 'route', 'routes',
        'génère', 'genere', 'montre', 'affiche', 'envoie', 'une', 'un', 'de', 'du', 'des', 'le', 'la', 'les',
        'sur', 'dans', 'pour', 'farm', 'farming', 'find', 'trouver', 'location', 'locations', 'spawns', 'spawn',
        'blank', 'base', 'pure', 'objective', 'quest', 'quête', 'objectif', 'tactical'])
    # Context is opt-in and never fills an unrecognized new target.
    followup_terms = ('same', 'that', 'this', 'again', 'it', 'même', 'cette')
    if explicit_followup:
        target_map = target_map or previous.get('map_name')
        remaining = remove(remaining, followup_terms)
        if not remaining and not dungeon_hits:
            remaining = previous.get('target', '')
            if previous.get('type') == 'dungeon':
                dungeon_hits = [remaining]
                remaining = ''

    try:
        kind = 'base'
        target = remaining
        if 'speedrun' in q or 'speed run' in q or (explicit_followup and previous.get('type') == 'speedrun' and remaining == previous.get('target')):
            path, intel = maps.generate_speedrun_raid_map(remaining if explicit_followup else q)
            if target_map and intel['map_name'] != target_map:
                return fail('That raid belongs to a different map. Please confirm the raid number or map.')
            kind, target = 'speedrun', f"speedrun raid {intel['raid_id']}"
        elif dungeon_hits:
            dungeon = dungeon_hits[0]
            if remaining:
                return fail(f'Please clarify the dungeon objective: {remaining}.')
            if target_map and target_map != DUNGEON_MAPS[dungeon]:
                return fail(f'{dungeon.title()} is mapped on {DUNGEON_MAPS[dungeon]}, not {target_map}.')
            path, intel = maps.generate_dungeon_tactical_map(dungeon)
            kind, target = 'dungeon', dungeon
        elif remaining in ('dungeon', 'donjon', 'creatures', 'creature', 'monsters', 'monstre', 'boss', 'miniboss'):
            return fail('Which dungeon or creature, and which map should I use?')
        elif not remaining:
            if not target_map:
                return fail('Which map and item, creature, or objective would you like?')
            path = maps.resolve_map_image(target_map)
            intel = {'map_name': target_map, 'title': target_map, 'drops': [], 'focus': 'Blank base map; no objective markers.'}
        else:
            creature = next((name for name, aliases in CREATURES.items() if remaining in aliases), None)
            if creature:
                if not target_map:
                    return fail(f'Which map should I use for {creature}?')
                path, intel = maps.generate_universal_bestiary_map(creature, target_map)
                kind, target = 'creatures', creature
            else:
                target = TRANSLATIONS.get(remaining, remaining)
                item_name = maps.resolve_item_name(target)
                if item_name:
                    if not target_map:
                        return fail(f'Which map should I use for {item_name}?')
                    path, intel = maps.generate_item_farm_map(target, target_map)
                    kind = 'farm'
                else:
                    path, intel = maps.generate_location_poi_map(target, target_map)
                    kind = 'objective'
                    if target_map and intel['map_name'] != target_map:
                        return fail(f'No mapped objective data for {target} on {target_map}.')
        title = intel.get('title') or intel.get('raid_name') or intel['map_name']
        drops = intel.get('drops', [])
        description = '\n'.join(d for d in drops if isinstance(d, str))
        description = description or '\n'.join(intel.get('active_objectives', [])) or intel.get('focus', '')
        context = {'map_name': intel['map_name'], 'type': kind, 'target': target,
                   'intel': intel, 'points_description': description}
        return {'spoken_text': f"Map for {title} generated.",
                'display_text': f"{title}\n{description}", 'image_attachment': path}, context
    except maps.MapDataUnavailable as error:
        return fail(str(error))
    except (OSError, sqlite3.Error):
        return fail('The map data or image could not be loaded. No map was generated; please try again once the data is available.')
