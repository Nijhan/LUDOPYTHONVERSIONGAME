from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator, List, Optional, Dict, Any
import json

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.bxjmqkpdfuqrzpcevvrz:zSDUjdsAZT4xmwEh@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database session context manager
@contextmanager
def get_db() -> Generator:
    """Get database session with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Player management functions
def create_player(db, name: str, color: str, game_id: int = None) -> int:
    """Create a new player and return player ID"""
    from .models import Player
    
    player = Player(name=name, color=color, game_id=game_id)
    db.add(player)
    db.flush()  # Flush to get the ID without committing
    return player.id

def get_player(db, player_id: int) -> Optional[Dict[str, Any]]:
    """Get player by ID"""
    from .models import Player
    
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        return {
            'id': player.id,
            'name': player.name,
            'color': player.color,
            'game_id': player.game_id,
            'position': player.position,
            'is_winner': player.is_winner
        }
    return None

def update_player_position(db, player_id: int, positions: List[int]):
    """Update player token positions"""
    from .models import Player
    
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        player.position = ','.join(map(str, positions))
        db.commit()

def mark_player_as_winner(db, player_id: int):
    """Mark player as winner"""
    from .models import Player
    
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        player.is_winner = True
        db.commit()

# Game management functions
def create_game(db, player_count: int = 4) -> int:
    """Create a new game and return game ID"""
    from .models import Game
    
    game = Game(player_count=player_count)
    db.add(game)
    db.flush()
    return game.id

def get_game(db, game_id: int) -> Optional[Dict[str, Any]]:
    """Get game by ID"""
    from .models import Game
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if game:
        return {
            'id': game.id,
            'player_count': game.player_count,
            'current_player': game.current_player,
            'status': game.status,
            'created_at': game.created_at
        }
    return None

def update_game_status(db, game_id: int, status: str):
    """Update game status"""
    from .models import Game
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if game:
        game.status = status
        db.commit()

def update_current_player(db, game_id: int, current_player: int):
    """Update current player turn"""
    from .models import Game
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if game:
        game.current_player = current_player
        db.commit()

def get_players_in_game(db, game_id: int) -> List[Dict[str, Any]]:
    """Get all players in a specific game"""
    from .models import Player
    
    players = db.query(Player).filter(Player.game_id == game_id).all()
    return [
        {
            'id': player.id,
            'name': player.name,
            'color': player.color,
            'position': player.position,
            'is_winner': player.is_winner
        }
        for player in players
    ]

def save_game_state(db, game_id: int, players_data: List[Dict[str, Any]]):
    """Save complete game state including all player positions"""
    from .models import Player
    
    for player_data in players_data:
        player = db.query(Player).filter(Player.id == player_data['id']).first()
        if player:
            player.position = player_data['position']
            player.is_winner = player_data.get('is_winner', False)
    
    db.commit()

def get_active_games(db) -> List[Dict[str, Any]]:
    """Get all active games (not finished)"""
    from .models import Game
    
    games = db.query(Game).filter(Game.status != 'finished').all()
    return [
        {
            'id': game.id,
            'player_count': game.player_count,
            'current_player': game.current_player,
            'status': game.status,
            'created_at': game.created_at
        }
        for game in games
    ]
