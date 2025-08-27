from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Move(Base):
    __tablename__= "moves"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id", ondelete="SET NULL"), nullable=True)
    dice_value = Column(Integer, nullable=False)
    new_position = Column(Integer)  # after move
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game", back_populates="moves")