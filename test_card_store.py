"""Offline, isolated tests: python -m unittest test_card_store -v."""
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from PIL import Image
from co_pilot.card_store import (CardUnavailableError, building_cards, card_key,
                                handle_missing_card, lookup, stored_card)
from generate_cards import build


class CardStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.env = patch.dict(os.environ, {'HUNGER_CARD_STORE': str(self.root / 'store')})
        self.env.start()
        self.calls = []
        @stored_card('name', 'is_french')
        def render_test(name='spear', is_french=False):
            self.calls.append((name, is_french))
            path = self.root / 'same-output.jpg'
            Image.new('RGB', (20, 20), 'blue' if is_french or name == 'shield' else 'red').save(path)
            return str(path)
        self.render = render_test
        self.module = types.ModuleType('_card_test_fixture')
        self.module.render_test = render_test
        self.modules = patch.dict(sys.modules, {'_card_test_fixture': self.module})
        self.modules.start()

    def tearDown(self):
        self.modules.stop()
        self.env.stop()
        self.temp.cleanup()

    def spec(self, name='spear', french=False, aliases=()):
        return ('_card_test_fixture', 'render_test', (name,), {'is_french': french}, aliases)

    def test_batch_then_read_only_retrieval_and_alias(self):
        report = build([self.spec(aliases=('Lance',)), self.spec(french=True)], self.root / 'store')
        self.assertEqual(report['counts']['render_test'], 2)
        english = self.render('SPEAR')
        self.assertEqual(english, self.render('Lance'))
        self.assertNotEqual(english, self.render('spear', True))
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.render(), english)
        self.assertEqual(self.render(name='spear'), english)
        self.assertEqual(Path(english).read_bytes(), Path(self.render('spear')).read_bytes())

    def test_duplicate_names_do_not_merge_different_skin_records(self):
        first = {'name': 'Skin', 'target': 'Hero', 'materials': ['Bone']}
        second = {'name': 'Skin', 'target': 'Hero', 'materials': ['Cloth']}
        self.assertNotEqual(card_key('skin', [first]), card_key('skin', [second]))

    def test_ambiguous_alias_is_not_served(self):
        report = build([self.spec(aliases=('shared',)),
                        self.spec('shield', aliases=('shared',))], self.root / 'store')
        self.assertEqual(len(report['ambiguous_aliases']), 1)
        with self.assertRaises(CardUnavailableError):
            self.render('shared')
        self.assertNotEqual(self.render('spear'), self.render('shield'))

    def test_duplicate_specs_keep_all_aliases(self):
        build([self.spec(aliases=('lance',)), self.spec(aliases=('polearm',))], self.root / 'store')
        self.assertEqual(self.render('lance'), self.render('polearm'))
        self.assertEqual(len(self.calls), 1)

    def test_missing_manifest_never_renders(self):
        with self.assertRaisesRegex(CardUnavailableError, 'python generate_cards.py'):
            self.render()
        self.assertEqual(self.calls, [])

    def test_unknown_card_never_renders(self):
        build([self.spec()], self.root / 'store')
        with self.assertRaises(CardUnavailableError):
            self.render('unknown')
        self.assertEqual(len(self.calls), 1)

    def test_missing_file_never_renders(self):
        build([self.spec()], self.root / 'store')
        Path(self.render()).unlink()
        with self.assertRaises(CardUnavailableError):
            self.render()
        self.assertEqual(len(self.calls), 1)

    def test_bad_manifest(self):
        directory = self.root / 'store'
        directory.mkdir()
        for value in ['not json', '[]', '{"version":99}', '{"version":1,"cards":{}}']:
            (directory / 'manifest.json').write_text(value)
            with self.assertRaises(CardUnavailableError):
                self.render()

    def test_outside_path_rejected(self):
        directory = self.root / 'store'
        directory.mkdir()
        (self.root / 'outside.jpg').write_bytes(b'not a card')
        (directory / 'manifest.json').write_text(json.dumps({'version': 1, 'cards': {
            card_key('render_test', ['spear', False]): '../outside.jpg'}}))
        with self.assertRaises(CardUnavailableError):
            self.render()

    def test_failed_build_keeps_previous_manifest_and_files(self):
        build([self.spec()], self.root / 'store')
        previous = (self.root / 'store/manifest.json').read_bytes()
        previous_image = self.render()
        @stored_card('name')
        def broken(name):
            raise RuntimeError('render failed')
        self.module.broken = broken
        with self.assertRaisesRegex(RuntimeError, 'Previous manifest was not replaced'):
            build([('_card_test_fixture', 'broken', ('x',), {}, ())], self.root / 'store')
        self.assertEqual(previous, (self.root / 'store/manifest.json').read_bytes())
        self.assertTrue(Path(previous_image).exists())
        self.assertEqual(self.render(), previous_image)

    def test_duplicate_specs_render_once(self):
        build([self.spec(), self.spec()], self.root / 'store')
        self.assertEqual(len(self.calls), 1)

    def test_build_scope_does_not_leak_after_error(self):
        with self.assertRaises(ValueError):
            with building_cards():
                self.render()
                raise ValueError()
        with self.assertRaises(CardUnavailableError):
            self.render()
        self.assertEqual(len(self.calls), 1)

    def test_bot_missing_card_response(self):
        @handle_missing_card
        def request():
            return self.render()
        reply = request()
        self.assertIsNone(reply['image_attachment'])
        self.assertIn('pre-generated card', reply['display_text'])
        self.assertIn('generate_cards.py', reply['display_text'])

    def test_unrelated_errors_not_hidden(self):
        @handle_missing_card
        def request():
            raise ValueError('not a missing card')
        with self.assertRaises(ValueError):
            request()

    def test_failed_image_validation_does_not_publish(self):
        @stored_card()
        def broken():
            path = self.root / 'bad.jpg'
            path.write_bytes(b'not an image')
            return str(path)
        self.module.broken = broken
        with self.assertRaises(RuntimeError):
            build([('_card_test_fixture', 'broken', (), {}, ())], self.root / 'store')
        self.assertFalse((self.root / 'store/manifest.json').exists())

class RecipeCatalogTests(unittest.TestCase):
    def test_uncached_recipe_uses_own_data_without_invented_prices_or_spawns(self):
        import universal_v8_engine as engine
        texts = []
        def record_text(self, xy, text, *args, **kwargs):
            texts.append(str(text))
        with building_cards(), patch.object(engine, 'save_and_sync', return_value='unused'):
            with patch('PIL.ImageDraw.ImageDraw.text', record_text):
                engine.render_recipe_card('conservator')
        rendered_text = ' '.join(texts)
        self.assertIn('CONSERVATOR', rendered_text)
        self.assertIn('Not recorded', rendered_text)
        self.assertNotIn('92 Silver', rendered_text)
        self.assertNotIn('Dupo Farrier', rendered_text)


class BuiltCatalogTests(unittest.TestCase):
    """Run these checks after generate_cards.py; skip on a clean source checkout."""
    @unittest.skipUnless((Path(__file__).parent / 'generated_cards/manifest.json').exists(),
                         'Build the full catalog first with python generate_cards.py')
    def test_lore_bot_queries_resolve_canonical_slugs_without_rendering(self):
        from co_pilot.lore_engine import answer_lore_query
        root = Path(__file__).parent / 'generated_cards'
        with patch.dict(os.environ, {'HUNGER_CARD_STORE': str(root)}):
            with patch.object(Image.Image, 'save', side_effect=AssertionError('Runtime rendered an image')):
                for query in ["c'est quoi the hunger", "who is mr sweet", "histoire du chateau"]:
                    with self.subTest(query=query):
                        reply = answer_lore_query(query, False)
                        self.assertTrue(Path(reply['image_attachment']).is_file())

    @unittest.skipUnless((Path(__file__).parent / 'generated_cards/manifest.json').exists(),
                         'Build the full catalog first with python generate_cards.py')
    def test_every_catalog_entry_is_retrievable_without_rendering(self):
        import importlib
        from generate_cards import catalog
        root = Path(__file__).parent / 'generated_cards'
        with patch.dict(os.environ, {'HUNGER_CARD_STORE': str(root)}):
            with patch.object(Image.Image, 'save', side_effect=AssertionError('Runtime rendered an image')):
                for module, name, args, kwargs, _ in catalog():
                    with self.subTest(renderer=name, args=str(args)[:80]):
                        path = getattr(importlib.import_module(module), name)(*args, **kwargs)
                        self.assertTrue(Path(path).is_file())
                        self.assertTrue(Path(path).is_relative_to(root.resolve()))


if __name__ == '__main__':
    unittest.main()
