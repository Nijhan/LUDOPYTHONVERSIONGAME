import pytest

# temporary stub
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0


def register_player(name):
    return Player(name)


def test_register_player():
    p = register_player("Alice")
    assert isinstance(p, Player)
    assert p.name == "Alice"
    assert p.position == 0
