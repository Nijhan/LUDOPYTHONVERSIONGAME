import pytest

# temporary stub
database = {}

def save_player(name, score):
    database[name] = score
    return True

def load_player(name):
    return database.get(name)


def test_save_and_load_player():
    save_player("Alice", 100)
    assert load_player("Alice") == 100
    assert load_player("Bob") is None
