import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from co_pilot import map_generator as maps
from co_pilot.map_requests import handle_map_request
from co_pilot.brain import CoPilotBrain


def result(target='Honey', map_name='Sombre Forest'):
    return '/new-map.jpg', {'title': target, 'map_name': map_name, 'drops': ['Verified requested points']}


class RoutingTests(unittest.TestCase):
    def test_requested_item_precedes_generic_map(self):
        with patch.object(maps, 'generate_item_farm_map', return_value=result()) as generate:
            response = CoPilotBrain().process_message('u', 'Tester', 'make me a map of honey on Sombre Forest')
        generate.assert_called_once_with('honey', 'Sombre Forest')
        self.assertEqual(response['image_attachment'], '/new-map.jpg')

    def test_french_item_and_map(self):
        with patch.object(maps, 'generate_item_farm_map', return_value=result()) as generate:
            handle_map_request('montre moi une carte pour trouver du miel sur Sombre Forest')
        generate.assert_called_once_with('honey', 'Sombre Forest')

    def test_creature_map_beats_creature_card(self):
        with patch.object(maps, 'generate_universal_bestiary_map', return_value=result('Bloat')) as generate:
            CoPilotBrain().process_message('u', 'Tester', 'show me a map of bloat on Sombre Forest')
        generate.assert_called_once_with('bloat', 'Sombre Forest')

    def test_unknown_and_ambiguous_never_attach_previous(self):
        prior = {'target': 'flour', 'map_name': 'Sarlat Farm', 'type': 'farm'}
        for query in ['make me a map of unobtainium', 'make me a map', 'map of flour',
                      'map of dungeon', 'map of Sarlat and Sombre', 'map of honey on Atlantis']:
            with self.subTest(query=query):
                response, context = handle_map_request(query, prior)
                self.assertNotIn('image_attachment', response)
                self.assertIsNone(context)

    def test_explicit_followup_only_and_user_isolation(self):
        brain = CoPilotBrain()
        with patch.object(maps, 'generate_item_farm_map', return_value=result()) as generate:
            brain.process_message('alice', 'Alice', 'map of honey on Sombre Forest')
            brain.process_message('alice', 'Alice', 'show that map again')
            self.assertEqual(generate.call_count, 2)
            response = brain.process_message('bob', 'Bob', 'show that map again')
            self.assertNotIn('image_attachment', response)
            brain.process_message('alice', 'Alice', 'forget it')
            response = brain.process_message('alice', 'Alice', 'show that map again')
            self.assertNotIn('image_attachment', response)

    def test_marker_followup_uses_actual_context(self):
        response, _ = handle_map_request('explain the points on that map', {'points_description': 'Honey sacks'})
        self.assertEqual(response['display_text'], 'Honey sacks')

    def test_dungeon_no_folly_fallback(self):
        with patch.object(maps, 'generate_dungeon_tactical_map', return_value=result('Pit', 'Sombre Forest')) as generate:
            CoPilotBrain().process_message('u', 'U', 'map of the pit')
        generate.assert_called_once_with('the pit')
        response, _ = handle_map_request('map of the pit on Sarlat Farm')
        self.assertNotIn('image_attachment', response)

    def test_named_map_is_blank_not_flour(self):
        response, _ = handle_map_request('show me Sarlat Farm map')
        self.assertEqual(response['image_attachment'], maps.SARLAT_MAP)

    def test_objective_uses_full_target_and_map(self):
        with patch.object(maps, 'generate_location_poi_map', return_value=result('Seeing Clearly', 'Jacques Bridge')) as generate:
            handle_map_request('map of Seeing Clearly on Jacques Bridge')
        generate.assert_called_once_with('seeing clearly', 'Jacques Bridge')

    def test_speedrun_response_and_repeat(self):
        payload = {'raid_id': 2, 'raid_name': 'Raid 2', 'map_name': 'Jacques Bridge',
                   'drops': [{'cont': 'Chest'}], 'active_objectives': ['Quest objective']}
        with patch.object(maps, 'generate_speedrun_raid_map', return_value=('/raid.jpg', payload)) as generate:
            response, context = handle_map_request('speedrun raid 2')
            repeated, _ = handle_map_request('show that map again', context)
        self.assertEqual(response['image_attachment'], '/raid.jpg')
        self.assertEqual(repeated['image_attachment'], '/raid.jpg')
        self.assertEqual(generate.call_count, 2)

    def test_pending_learning_cannot_swallow_map(self):
        import time
        brain = CoPilotBrain()
        brain.pending_term = 'old unknown request'
        brain.pending_term_time = time.time()
        response = brain.process_message('u', 'U', 'make me a map of Sarlat')
        self.assertEqual(response['image_attachment'], maps.SARLAT_MAP)
        self.assertIsNone(brain.pending_term)

    def test_unknown_map_cannot_match_known_objective(self):
        for query in ["map of Piro's Lens on Atlantis", "map of Piro's Lens Atlantis"]:
            response, _ = handle_map_request(query)
            self.assertNotIn('image_attachment', response)

    def test_explicit_different_explanation_does_not_use_context(self):
        response, _ = handle_map_request('explain the map of flour on Sarlat', {'points_description': 'Honey sacks'})
        self.assertNotEqual(response['display_text'], 'Honey sacks')

    def test_quest_articles_are_not_lost(self):
        with patch.object(maps, 'render_dynamic_v25_briefing'):
            response, _ = handle_map_request('map of The Last Prisoner on Jacques Bridge')
        self.assertIn('image_attachment', response)

    def test_missing_image_is_text_only(self):
        with patch.object(maps, 'resolve_map_image', side_effect=maps.MapDataUnavailable('Image missing')):
            response, _ = handle_map_request('map of Sarlat')
        self.assertNotIn('image_attachment', response)


class GeneratorTests(unittest.TestCase):
    def test_unknown_map_rejected(self):
        with self.assertRaises(maps.MapDataUnavailable):
            maps.resolve_map_image('Atlantis')

    def test_dungeons_use_database_maps_and_coordinates(self):
        for dungeon, expected_map, x in [('the pit', 'Sombre Forest', 2655.2),
                                         ('the undercroft', 'Sarlat Farm', 3444.1),
                                         ('jacques folly', 'Jacques Bridge', 1680.37)]:
            with self.subTest(dungeon=dungeon), patch.object(maps, 'render_dynamic_v25_briefing') as render:
                _, intel = maps.generate_dungeon_tactical_map(dungeon)
                self.assertEqual(intel['map_name'], expected_map)
                self.assertAlmostEqual(render.call_args.args[0]['points'][0]['x'], x, places=1)

    def test_unknown_dungeon_rejected(self):
        with self.assertRaises(maps.MapDataUnavailable):
            maps.generate_dungeon_tactical_map('unknown dungeon')

    def test_speedrun_requires_valid_number(self):
        for query in ['speedrun map', 'speedrun raid 99', 'speedrun raid 1 and raid 2']:
            with self.subTest(query=query), self.assertRaises(maps.MapDataUnavailable):
                maps.generate_speedrun_raid_map(query)

    def test_empty_creature_data_does_not_use_miniboss(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            import json
            json.dump({'bestiary': {'bloat': {'name_en': 'Bloat'}}, 'map_spawners': {'Sarlat Farm': {'miniboss': [{'x': 1, 'y': 2}]}}}, f)
            f.flush()
            with patch.object(maps, 'SPAWNS_DB_PATH', f.name), self.assertRaises(maps.MapDataUnavailable):
                maps.generate_universal_bestiary_map('bloat', 'Sarlat Farm')

    def test_farmer_not_fabricated_on_other_maps(self):
        with self.assertRaises(maps.MapDataUnavailable):
            maps.generate_universal_bestiary_map('farmer dreg', 'Sombre Forest')

    def test_unknown_creature_not_drooler(self):
        with self.assertRaises(maps.MapDataUnavailable):
            maps.generate_universal_bestiary_map('unicorn', 'Sarlat Farm')

    def test_item_is_exact_and_unknown_not_rendered(self):
        with patch.object(maps, 'render_dynamic_v25_briefing') as render:
            for item in ['unobtainium', 'flo', '']:
                with self.subTest(item=item), self.assertRaises(maps.MapDataUnavailable):
                    maps.generate_item_farm_map(item, 'Sarlat Farm')
        render.assert_not_called()

    def test_known_item_uses_data_and_no_unrelated_story_poi(self):
        with patch.object(maps, 'render_dynamic_v25_briefing') as render:
            path, intel = maps.generate_item_farm_map('flour', 'Sarlat Farm')
        cfg = render.call_args.args[0]
        self.assertTrue(cfg['points'])
        self.assertEqual(cfg['story_pois'], [])
        self.assertIn('flour_Sarlat_Farm', path)
        self.assertEqual(intel['map_name'], 'Sarlat Farm')

    def test_unknown_objective_not_blank_map(self):
        with self.assertRaises(maps.MapDataUnavailable):
            maps.generate_location_poi_map('unknown objective', 'Sarlat Farm')

    def test_objective_map_hint_is_filter(self):
        with tempfile.NamedTemporaryFile(suffix='.db') as f:
            conn = sqlite3.connect(f.name)
            conn.execute('CREATE TABLE map_points (map_name, title, point_type, x, y, description, quest_slug)')
            conn.execute("INSERT INTO map_points VALUES ('Jacques Bridge', 'Camp', 'poi', 1, 2, '', 'camp')")
            conn.commit(); conn.close()
            def connect():
                c = sqlite3.connect(f.name); c.row_factory = sqlite3.Row; return c
            with patch.object(maps, 'get_connection', side_effect=connect), self.assertRaises(maps.MapDataUnavailable):
                maps.generate_location_poi_map('Camp', 'Sarlat Farm')


if __name__ == '__main__':
    unittest.main()
