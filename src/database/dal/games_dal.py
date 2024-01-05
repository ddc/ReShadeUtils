# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.sql import collate, asc
from src.database.db_utils import DBUtils
from src.database.models.games_model import Games


class GamesDal:
    def __init__(self, db_session, log):
        self.log = log
        self.columns = [x for x in Games.__table__.columns]
        self.db_utils = DBUtils(db_session, log)

    def insert_game(self, games_obj):
        stmt = Games(
            name=games_obj.game_name,
            architecture=games_obj.architecture,
            api=games_obj.api,
            path=games_obj.path)
        self.db_utils.add(stmt)

    def get_games(self):
        stmt = sa.select(*self.columns).order_by(asc(collate(Games.name, "NOCASE")))
        results = self.db_utils.fetchall(stmt)
        return results

    def get_game_by_path(self, game_path):
        stmt = sa.select(*self.columns).where(Games.path == game_path).order_by(asc(collate(Games.name, "NOCASE")))
        results = self.db_utils.fetchall(stmt)
        return results

    def get_game_by_name(self, game_name):
        stmt = sa.select(*self.columns).where(Games.name == game_name).order_by(asc(collate(Games.name, "NOCASE")))
        results = self.db_utils.fetchall(stmt)
        return results

    def update_game(self, games_obj):
        stmt = sa.update(Games).where(Games.id == games_obj.id).values(
            name=games_obj.game_name,
            architecture=games_obj.architecture,
            api=games_obj.api
        )
        self.db_utils.execute(stmt)

    def update_game_path(self, game_id, game_path):
        stmt = sa.update(Games).where(Games.id == game_id).values(path=game_path)
        self.db_utils.execute(stmt)

    def update_game_architecture(self, game_id, game_architecture):
        stmt = sa.update(Games).where(Games.id == game_id).values(architecture=game_architecture)
        self.db_utils.execute(stmt)

    def update_game_api(self, game_id, game_api):
        stmt = sa.update(Games).where(Games.id == game_id).values(api=game_api)
        self.db_utils.execute(stmt)

    def delete_game(self, game_id):
        stmt = sa.delete(Games).where(Games.id == game_id)
        self.db_utils.execute(stmt)
