from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class GamePlayer(Base):
    __tablename__ = "game_players"
    __table_args__ = (
        UniqueConstraint("game_id", "player_id", name="uq_game_player"),
        UniqueConstraint("game_id", "color", name="uq_game_color"),  # color unique per game
    )

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    color = Column(String(10), nullable=False)  # red|blue|green|yellow
    is_winner = Column(Boolean, default=False)

    game = relationship("Game", back_populates="players")
    player = relationship("Player", back_populates="games")
    tokens = relationship("Token", back_populates="game_player", cascade="all, delete-orphan")