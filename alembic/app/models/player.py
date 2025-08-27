from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    games = relationship("GamePlayer", back_populates="player", cascade="all, delete-orphan")

# Relationship-This defines a relationship between your Player model and another model (in this case, GamePlayer).
# Gameplayer-In many game databases, GamePlayer is a join/association table that connects Game and Player.
# back_populates="player-This links the relationship both ways."
# Cascade-This defines what happens when you delete or modify a Player