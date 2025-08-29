import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the alembic directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'alembic'))

from app.db import get_db, create_player, get_player, create_game, get_game, update_game_status, update_current_player
from app.models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:wSSeDgPVPo0aa3Oo@localhost:5432/ludo"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    """Create a new database session for a test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_player(db):
    player_id = create_player(db, name="Alice", color="Red")
    player = get_player(db, player_id)
    assert player is not None
    assert player['name'] == "Alice"
    assert player['color'] == "Red"

def test_create_game(db):
    game_id = create_game(db, player_count=4)
    game = get_game(db, game_id)
    assert game is not None
    assert game['player_count'] == 4

def test_update_game_status(db):
    game_id = create_game(db, player_count=4)
    update_game_status(db, game_id, "in_progress")
    game = get_game(db, game_id)
    assert game['status'] == "in_progress"

def test_update_current_player(db):
    game_id = create_game(db, player_count=4)
    update_current_player(db, game_id, 1)
    game = get_game(db, game_id)
    assert game['current_player'] == 1
