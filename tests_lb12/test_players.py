import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from players import Player, register_player


def test_register_player_creates_player_instance():
    p = register_player("Ada")
    assert isinstance(p, Player)
    assert p.name == "Ada"
    assert p.position == 0 or getattr(p, "token_position", 0) == 0


def test_player_empty_name_raises_value_error():
    with pytest.raises(ValueError):
        register_player("   ")

