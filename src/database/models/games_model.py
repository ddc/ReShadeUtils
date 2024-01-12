# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class GamesBase(DeclarativeBase):
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default="CURRENT_TIMESTAMP")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default="CURRENT_TIMESTAMP")


class Games(GamesBase):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    architecture: Mapped[str] = mapped_column()
    api: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
