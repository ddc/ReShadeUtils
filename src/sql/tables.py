# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, event, text


Base = declarative_base()


class Configs(Base):
    __tablename__ = "configs"
    id = Column(Integer, Sequence("configs_pk_seq"), primary_key=True, nullable=False, unique=True, autoincrement=True)
    use_dark_theme = Column(Integer, nullable=False, server_default=text("1"))
    check_program_updates = Column(Integer, nullable=False, server_default=text("1"))
    show_info_messages = Column(Integer, nullable=False, server_default=text("1"))
    check_reshade_updates = Column(Integer, nullable=False, server_default=text("1"))
    update_shaders = Column(Integer, nullable=False, server_default=text("1"))
    create_screenshots_folder = Column(Integer, nullable=False, server_default=text("1"))
    program_version = Column(String(10), nullable=True)
    reshade_version = Column(String(10), nullable=True)


class Games(Base):
    __tablename__ = "games"
    id = Column(Integer, Sequence("games_pk_seq"), primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    architecture = Column(String(255), nullable=False)
    api = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)


@event.listens_for(Configs.__table__, "after_create")
def receive_after_create(target, connection, **kw):
    connection.execute(
        """CREATE TRIGGER IF NOT EXISTS before_insert_configs
            BEFORE INSERT ON configs
            BEGIN
                SELECT CASE
                    WHEN (SELECT count(*) FROM configs)IS 1 THEN
                    RAISE(ABORT, 'CANNOT INSERT INTO CONFIGS TABLE ANYMORE')
                END;
            END;
    """
    )
