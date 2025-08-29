import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ludo_game.players import register_players, Player
from ludo_game.postgres_db import PostgresDB

class TestPlayerRegistrationResume(unittest.TestCase):
    def setUp(self):
        self.db = PostgresDB()

    @patch('builtins.input')
    def test_register_new_player(self, mock_input):
        # Simulate inputs for new player registration
        mock_input.side_effect = ['2', 'newplayer1', 'newplayer2', 'red', 'green']
        players = register_players(self.db)
        self.assertEqual(len(players), 2)
        self.assertTrue(all(isinstance(p, Player) for p in players))
        self.assertTrue(all(p.username in ['newplayer1', 'newplayer2'] for p in players))

    @patch('builtins.input')
    def test_register_existing_player_no_active_game(self, mock_input):
        # Simulate existing player with no active game
        existing_username = 'existingplayer'
        # Ensure player exists in DB
        self.db.get_or_create_player(existing_username)
        mock_input.side_effect = ['2', existing_username, 'newplayer2', 'red', 'green']
        players = register_players(self.db)
        self.assertEqual(len(players), 2)
        self.assertTrue(any(p.username == existing_username for p in players))

    @patch('builtins.input')
    def test_register_existing_player_with_active_game_resume(self, mock_input):
        existing_username = 'activeplayer'
        player_row = self.db.get_or_create_player(existing_username)
        # Simulate active game tokens for player
        def dummy_get_player_active_game_tokens(player_id):
            return {
                'game_id': 1,
                'game_player_id': 1,
                'color': 'RED',
                'tokens': [
                    {'id': 1, 'position': '5', 'is_home': False, 'is_finished': False},
                    {'id': 2, 'position': '10', 'is_home': False, 'is_finished': False}
                ]
            }
        self.db.get_player_active_game_tokens = dummy_get_player_active_game_tokens
        mock_input.side_effect = ['1', existing_username, 'y', 'red']
        players = register_players(self.db)
        self.assertEqual(len(players), 1)
        self.assertEqual(players[0].username, existing_username)
        self.assertTrue(hasattr(players[0], 'active_game_data'))
        self.assertEqual(players[0].active_game_data['game_id'], 1)

    @patch('builtins.input')
    def test_register_existing_player_with_active_game_new(self, mock_input):
        existing_username = 'activeplayernew'
        player_row = self.db.get_or_create_player(existing_username)
        def dummy_get_player_active_game_tokens(player_id):
            return {
                'game_id': 2,
                'game_player_id': 2,
                'color': 'GREEN',
                'tokens': [
                    {'id': 3, 'position': '3', 'is_home': False, 'is_finished': False},
                    {'id': 4, 'position': '7', 'is_home': False, 'is_finished': False}
                ]
            }
        self.db.get_player_active_game_tokens = dummy_get_player_active_game_tokens
        mock_input.side_effect = ['1', existing_username, 'n', 'green']
        players = register_players(self.db)
        self.assertEqual(len(players), 1)
        self.assertEqual(players[0].username, existing_username)
        self.assertFalse(hasattr(players[0], 'active_game_data'))

if __name__ == '__main__':
    unittest.main()
