# import pytest
# import builtins
# #builtins is the module that contains all the “built-in” functions, constants, and exceptions that you can use without importing anything.


# # Flexible import so it works in both structures

# try:
#     # Case 1: utils inside ludo_game/
#     from ludo_game.utils import input_utils
# except ModuleNotFoundError:
    
#     # Case 2: utils at project root
#     from utils import input_utils

# from ludo_game import players



# # Fake DB class for testing

# class FakeDB:
#     """
#     A very simple fake 'database' for testing.
#     It stores players in a dictionary instead of a real database.
#     """
#     def __init__(self):
#         self.data = {}
#         self.next_id = 1

#     def get_or_create_player(self, username):
#         """
#         If player exists, return it.
#         If not, create a new one with a unique id.
#         """
#         if username not in self.data:
#             self.data[username] = {
#                 "id": self.next_id,
#                 "username": username,
#                 "wins": 0,
#                 "losses": 0,
#             }
#             self.next_id += 1
#         return self.data[username]



# # Helper to simulate user inputs

# def run_with_inputs(inputs, func, *args):
#     """
#     Replaces input() temporarily with our fake version.
#     Each call to input() will return the next item from 'inputs'.
#     """
#     iterator = iter(inputs)

#     def fake_input(_prompt=""):
#         return next(iterator)

#     # Save real input
#     real_input = builtins.input
#     builtins.input = fake_input

#     try:
#         return func(*args)
#     finally:
#         builtins.input = real_input



# # Tests

# def test_validate_username_valid_and_invalid():
#     """
#     Test different usernames to make sure validation works.
#     """
#     # valid username
#     assert input_utils.validate_username("eva123")[0] is True

#     # too short (only 2 letters, needs 3+)
#     assert input_utils.validate_username("ab")[0] is False

#     # too long (more than 20 characters)
#     assert input_utils.validate_username("thisiswaytoolongusername")[0] is False

#     # invalid characters (only letters, numbers, _, - are allowed)
#     assert input_utils.validate_username("eva!")[0] is False

#     # reserved name (like "admin")
#     assert input_utils.validate_username("admin")[0] is False


# def test_register_players_and_choose_colors():
#     """
#     Test registering 2 players and assigning colors.
#     """
#     db = FakeDB()

#     # Simulated user inputs:
#     # - "2" players
#     # - names: "eva", "maina"
#     # - colors: "red", "green"
#     inputs = ["2", "eva", "maina", "red", "green"]

#     # First part: register players (asks for number of players + names)
#     players_list = run_with_inputs(inputs, players.register_players, db)

#     # Second part: choose colors (asks for colors)
#     run_with_inputs(inputs[3:], players.choose_colors, players_list)

#     # Now check the results with assert
#     assert len(players_list) == 2               # we should have 2 players
#     assert players_list[0].username == "eva"    # first player's name is eva
#     assert players_list[0].color == "RED"       # and she chose red
#     assert players_list[1].username == "maina"  # second player's name is maina
#     assert players_list[1].color == "GREEN"     # and he chose green

import pytest
import psycopg2
from ludo_game.db import RealDB


# Setup: Connect to a test database

@pytest.fixture(scope="module")
def real_db():
    """
    Fixture to connect to a Postgres test database.
    Make sure you have created:
    database: ludo_test
    user: your_postgres_user
    password: your_postgres_password
    host: localhost
    """
    db = RealDB(
        dbname="postgres",
        user="postgres.uoouexfczqhdqjrvtsjn",
        password="zSDUjdsAZT4xmwEh",
        host="aws-1-eu-north-1.pooler.supabase.com",
    )
    yield db

    # Teardown: clear test data
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres.uoouexfczqhdqjrvtsjn",
        password="zSDUjdsAZT4xmwEh",
        host="aws-1-eu-north-1.pooler.supabase.com",
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM players;")  # cleanup players table
    conn.commit()
    cur.close()
    conn.close()


# Tests

def test_create_and_get_player(real_db):
    """Test inserting a new player and retrieving them."""
    player = real_db.get_or_create_player("eva")
    assert player["username"] == "eva"
    assert "id" in player

    # Second call should not create a duplicate
    player2 = real_db.get_or_create_player("eva")
    assert player2["id"] == player["id"]


def test_update_player_stats(real_db):
    """Test updating wins/losses for a player."""
    player = real_db.get_or_create_player("maina")

    # Update wins + losses
    real_db.update_player_stats(player["id"], wins=5, losses=2)

    updated = real_db.get_or_create_player("maina")
    assert updated["wins"] == 5
    assert updated["losses"] == 2
