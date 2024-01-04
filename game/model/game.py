from __future__ import annotations

from sqlalchemy import Column, Integer, String

from db.database import Base
from sqlalchemy.dialects.mysql import JSON


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    players = Column(JSON, nullable=False)
    movements_played = Column(Integer, nullable=False, default=0)
    next_turn = Column(String(50))
    board: list[list[str | None]] = Column(JSON, nullable=False)
    winner = Column(String(50), nullable=True)
