from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    game_player_id = Column(Integer, ForeignKey("game_players.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, default=0)     # board index; define your mapping
    is_home = Column(Boolean, default=True)   # still at home yard
    is_finished = Column(Boolean, default=False)

    game_player = relationship("GamePlayer", back_populates="tokens")