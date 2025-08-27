from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    game_players = relationship("GamePlayer", back_populates="player")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="waiting")
    current_player_turn = Column(Integer, default=0)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)
    
    game_players = relationship("GamePlayer", back_populates="game")
    winner = relationship("Player", foreign_keys=[winner_id])

class GamePlayer(Base):
    __tablename__ = "game_players"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    color = Column(String, nullable=False)
    player_order = Column(Integer, nullable=False)
    token_positions = Column(JSON, default=[0, 0, 0, 0])
    is_finished = Column(Boolean, default=False)
    
    game = relationship("Game", back_populates="game_players")
    player = relationship("Player", back_populates="game_players")