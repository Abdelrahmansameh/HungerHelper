#!/usr/bin/env python3
"""Build the complete static card catalog before starting the bot."""
import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import sqlite3
import tempfile
import os

from co_pilot.card_store import ROOT, building_cards, card_key, store_root


def catalog():
    """Enumerate actual renderer data, with exact English/French name aliases."""
    # Fail early rather than allowing the legacy item renderer to swallow missing dependencies.
    import co_pilot.companion_intel
    import universal_v8_engine as engine
    from co_pilot.lore_engine import LORE_DATABASE
    specs = []
    def add(module, renderer, args=(), kwargs=None, aliases=()):
        specs.append((module, renderer, args, kwargs or {}, aliases))
    def universal(renderer, args=(), kwargs=None, aliases=()):
        add('universal_v8_engine', renderer, args, kwargs, aliases)
    with sqlite3.connect(f'file:{ROOT / "hunger_helper.db"}?mode=ro', uri=True) as db:
        for table, renderer, names, languages in [
            ('companion_items_cache', 'render_item_card', 'name_en, name_fr', True),
            ('weapons', 'render_pure_english_melee_card', 'name_en, name_fr', False),
            ('quests', 'render_dynamic_quest_contract_card', 'name', True),
            ('bags_full', 'render_bag_card', 'name', False),
            ('traps_full', 'render_trap_hazard_card', 'name', False),
            ('status_effects_full', 'render_status_effect_card', 'name', False),
            ('gathering_full', 'render_gathering_card', 'name', False),
            ('containers_full', 'render_container_card', 'name', False),
            ('recipes_full', 'render_recipe_card', 'name', False),
        ]:
            for slug, *aliases in db.execute(f'SELECT slug, {names} FROM {table} ORDER BY slug'):
                for french in ([False, True] if languages else [None]):
                    add('co_pilot.card_renderer' if table == 'companion_items_cache' else 'universal_v8_engine',
                        renderer, (slug,), {'is_french': french} if french is not None else {},
                        tuple(a for a in aliases if a))
    for renderer, entries in [('render_clean_character_card', engine.HEROES_DATA),
                              ('render_universal_creature_card', engine.CREATURES_DATABASE),
                              ('render_pure_english_firearm_card', engine.FIREARMS_DATABASE)]:
        for key, data in entries.items():
            for french in [False, True]:
                universal(renderer, (key,), {'is_french': french}, tuple(
                    data[n] for n in ('name', 'name_en', 'name_fr') if data.get(n)))
    for renderer in ['render_one_handed_melee_overview_card', 'render_two_handed_melee_overview_card']:
        universal(renderer)
    for french in [False, True]:
        universal('render_authentic_dungeon_card', kwargs={'is_french': french})
        add('clean_cards_v5', 'render_clean_dungeon_card', kwargs={'is_french': french})
    for topic in LORE_DATABASE:
        universal('render_lore_card', (topic,))
    drops = json.loads((ROOT / 'data/high_rate_drops.json').read_text())
    for slug, data in drops.items():
        universal('render_recipe_card', (slug,), aliases=(data.get('title', slug),))
    skins = json.loads((ROOT / 'data/full_companion_skins.json').read_text())
    groups = {}
    for skin in skins.values():
        universal('render_pure_english_cosmetic_card', (skin,))
        target = skin.get('target', '')
        group = groups.setdefault(target, [])
        if skin.get('name') and skin['name'].strip() not in {s['name'].strip() for s in group}:
            group.append(skin)
    for target, group in groups.items():
        if len(group) >= 2:
            universal('render_weapon_skins_showcase_sheet', (target, group))
    legacy = json.loads((ROOT / 'data/full_skins_database.json').read_text())
    for skin in legacy.values():
        add('cosmetic_card_builder', 'render_cosmetic_craft_card_dynamic', (skin,))
    for hero in engine.HEROES_DATA:
        for renderer in ['render_all_5_mastery_trees_card', 'render_build_stats_summary_card']:
            add('mastery_cards_v5', renderer, (), {'player_name': hero.title(), 'level': 100})
    return specs


def spec_key(fn, args, kwargs):
    bound = fn.card_signature.bind(*args, **kwargs)
    bound.apply_defaults()
    return card_key(fn.__name__, [bound.arguments[f] for f in fn.card_fields])


def build(specs, destination):
    """Publish one manifest only after every card succeeds; keep old files usable."""
    from PIL import Image
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    images = destination / 'images'
    images.mkdir(exist_ok=True)
    cards, failures, counts = {}, [], Counter()
    alias_targets = {}
    with building_cards():
        for index, (module, name, args, kwargs, aliases) in enumerate(specs):
            if index and index % 100 == 0:
                print(f'Processed {index} catalog entries; {len(failures)} failures', flush=True)
            fn = getattr(importlib.import_module(module), name)
            key = spec_key(fn, args, kwargs)
            if key in cards:
                for alias in aliases:
                    alias_key = spec_key(fn, (alias,) + args[1:], kwargs)
                    alias_targets.setdefault(alias_key, set()).add(cards[key])
                continue
            try:
                source = Path(fn(*args, **kwargs))
                with Image.open(source) as image:
                    image.verify()
                content = source.read_bytes()
                filename = hashlib.sha256(content).hexdigest() + source.suffix.lower()
                target = images / filename
                if not target.exists():
                    with tempfile.NamedTemporaryFile(dir=images, delete=False) as temp:
                        temp.write(content)
                    os.replace(temp.name, target)
                relative = 'images/' + filename
                cards[key] = relative
                for alias in aliases:
                    alias_key = spec_key(fn, (alias,) + args[1:], kwargs)
                    alias_targets.setdefault(alias_key, set()).add(relative)
                counts[name] += 1
            except Exception as exc:
                failures.append({'renderer': name, 'key': key, 'error': str(exc)})
                print(f'FAILED {name} {args[:1]}: {exc}', flush=True)
    ambiguous = [key for key, targets in alias_targets.items() if len(targets) > 1]
    for key, targets in alias_targets.items():
        if len(targets) == 1 and key not in cards:
            cards[key] = next(iter(targets))
    report = {'ambiguous_aliases': ambiguous, 'version': 1, 'counts': dict(counts), 'failures': failures, 'cards': cards}
    (destination / 'build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    if failures:
        raise RuntimeError(f'{len(failures)} cards failed. Previous manifest was not replaced; see build-report.json.')
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination, delete=False) as temp:
        json.dump(report, temp, indent=2)
    os.replace(temp.name, destination / 'manifest.json')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=store_root())
    parser.add_argument('--list', action='store_true', help='List coverage without rendering')
    options = parser.parse_args()
    specs = catalog()
    if options.list:
        print(json.dumps(dict(Counter(s[1] for s in specs)), indent=2))
        return
    report = build(specs, options.output)
    print(json.dumps(report['counts'], indent=2))
    print(f'Published {sum(report["counts"].values())} cards to {options.output}')


if __name__ == '__main__':
    main()
