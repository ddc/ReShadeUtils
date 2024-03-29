# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.constants import variables


class GamesBase(DeclarativeBase):
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, server_default="CURRENT_TIMESTAMP")
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, server_default="CURRENT_TIMESTAMP")


class Games(GamesBase):
    __tablename__ = "games"
    __table_args__ = (
        sa.CheckConstraint(f"architecture in {variables.ALL_ARCHITECTURES}", name="check_architecture_names"),
        sa.CheckConstraint(f"api in {variables.ALL_APIS}", name="check_api_names"),
        sa.CheckConstraint(f"dll in {variables.ALL_DLL_NAMES}", name="check_dll_names"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    architecture: Mapped[str] = mapped_column()
    api: Mapped[str] = mapped_column()
    dll: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column(unique=True)
