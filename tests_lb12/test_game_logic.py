import pytest
import random

# temporary stubs
def roll_dice():
    return random.randint(1, 6)

def move_token(position, steps):
    return position + steps

def switch_turn(current):
    return "Player2" if current == "Player1" else "Player1"

def check_winner(position, end=30):
    return position >= end


def test_roll_dice():
    for _ in range(10):
        result = roll_dice()
        assert 1 <= result <= 6


def test_move_token():
    assert move_token(0, 3) == 3
    assert move_token(5, 2) == 7


def test_switch_turn():
    assert switch_turn("Player1") == "Player2"
    assert switch_turn("Player2") == "Player1"


def test_check_winner():
    assert not check_winner(10)
    assert check_winner(30)
    assert check_winner(40)
