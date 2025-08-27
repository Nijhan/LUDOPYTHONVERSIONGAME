from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    status = Column(String(20), default="waiting", nullable=False)  # waiting|active|finished
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    players = relationship("GamePlayer", back_populates="game", cascade="all, delete-orphan")
    moves = relationship("Move", back_populates="game", cascade="all, delete-orphan")