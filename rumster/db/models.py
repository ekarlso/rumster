from sqlalchemy import Column, Integer, Unicode, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from oslo.db.sqlalchemy import models
from oslo.utils import timeutils

from rumster.db import base
from rumster.db import types


player_series = Table(
    "player_series", base.BASE.metadata,
    Column("player_id", types.UUID, ForeignKey("players.id")),
    Column("series_id", types.UUID, ForeignKey("series.id")),
)


class Player(base.BASE, models.TimestampMixin):
    __tablename__ = "players"
    name = Column(Unicode)
    email = Column(Unicode(100), nullable=False)


class Series(base.BASE, models.TimestampMixin):
    __tablename__ = "series"

    players = relationship("Player", secondary=player_series, backref="series")
    rounds = relationship("Round", backref="series")


class Round(base.BASE, models.TimestampMixin):
    __tablename__ = "rounds"

    series_id = Column(types.UUID(), ForeignKey("series.id"))


class RoundStats(base.BASE):
    """Stats for one round"""
    __tablename__ = "round_stats"

    round_id = Column(types.UUID(), ForeignKey("rounds.id"))
    player_id = Column(types.UUID, ForeignKey("players.id"))
