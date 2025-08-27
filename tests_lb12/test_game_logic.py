import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from game_logic import roll_dice, move_token, switch_turn, check_winner


def test_roll_dice_returns_valid_values():
    for _ in range(100):
        value = roll_dice()
        assert isinstance(value, int), f"Dice roll should be int, got {type(value)}"
        assert 1 <= value <= 6, f"Dice roll out of range: {value}"

def test_move_token_adds_steps_correctly():
    start = 0
    assert move_token(start, 4) == 4
    assert move_token(5, 2) == 7
    def test_switch_turn_rotates_players():
    players = ["P1", "P2", "P3"]
    assert switch_turn(0, players) == 1
    assert switch_turn(1, players) == 2
    assert switch_turn(2, players) == 0
