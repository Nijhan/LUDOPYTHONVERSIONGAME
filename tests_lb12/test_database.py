import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

try:
    import database
except Exception:
    database = None


def test_database_module_exports_expected_functions():
    assert database is not None, "database.py not found in project root"
    assert hasattr(database, "connect_db"), "connect_db missing in database.py"
    assert hasattr(database, "save_player_stats"), "save_player_stats missing in database.py"
    assert hasattr(database, "load_player_stats"), "load_player_stats missing in database.py"
