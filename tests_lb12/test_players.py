import pytest
import psycopg2
from database import RealDB


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