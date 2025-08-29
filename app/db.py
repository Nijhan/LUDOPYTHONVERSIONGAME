import sys
from pathlib import Path
# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from alembic.app.db import get_db
from alembic.app.models.player import Player as DBPlayer
from sqlalchemy.orm import Session

class RealDB:
    def __init__(self):
        pass
    
    def get_or_create_player(self, username):
        """
        Get or create a player by username.
        Returns a dictionary with player information.
        """
        with get_db() as db:
            # Try to find existing player
            player = db.query(DBPlayer).filter(DBPlayer.username == username).first()
            
            if player:
                # Return existing player data
                return {
                    "username": player.username,
                    "id": player.id,
                    "wins": getattr(player, 'wins', 0),
                    "losses": getattr(player, 'losses', 0)
                }
            else:
                # Create new player - need to create with proper fields
                new_player = DBPlayer(username=username, email=f"{username}@example.com")
                db.add(new_player)
                db.flush()
                player_id = new_player.id
                return {
                    "username": username,
                    "id": player_id,
                    "wins": 0,
                    "losses": 0
                }
