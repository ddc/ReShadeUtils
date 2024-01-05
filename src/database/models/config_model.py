# -*- coding: utf-8 -*-
import constants
from datetime import datetime
from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import text


class ConfigBase(DeclarativeBase):
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Config(ConfigBase):
    __tablename__ = "config"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    program_version: Mapped[str] = mapped_column(nullable=True, server_default=constants.VERSION)
    reshade_version: Mapped[str] = mapped_column(nullable=True)
    use_dark_theme: Mapped[Boolean] = mapped_column(Boolean, server_default="0")
    check_program_updates: Mapped[Boolean] = mapped_column(Boolean, server_default="1")
    show_info_messages: Mapped[Boolean] = mapped_column(Boolean, server_default="1")
    check_reshade_updates: Mapped[Boolean] = mapped_column(Boolean, server_default="1")
    update_shaders: Mapped[Boolean] = mapped_column(Boolean, server_default="1")
    create_screenshots_folder: Mapped[Boolean] = mapped_column(Boolean, server_default="1")
