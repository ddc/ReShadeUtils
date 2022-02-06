# |*****************************************************
# * Copyright         : Copyright (C) 2022
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# -*- coding: utf-8 -*-
from src.sql.tables import Games
from sqlalchemy.sql import collate, asc


class GamesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log
        self.table = Games.__table__
        self.database = main.database


    def get_games(self):
        sql = self.table.select().order_by(asc(collate(self.table.columns.name, "NOCASE")))
        return self.database.select(sql)


    def get_game_by_path(self, path):
        sql = self.table.select().\
            where(self.table.columns.path == path).\
            order_by(asc(collate(self.table.columns.name, "NOCASE")))
        return self.database.select(sql)


    def get_game_by_name(self, game_name):
        sql = self.table.select().\
            where(self.table.columns.name == game_name).\
            order_by(asc(collate(self.table.columns.name, "NOCASE")))
        return self.database.select(sql)


    def insert_game(self, games_obj):
        sql = self.table.insert().values(
            name=games_obj.game_name,
            architecture=games_obj.architecture,
            api=games_obj.api,
            path=games_obj.path)
        return self.database.execute(sql)


    def update_game(self, games_obj):
        sql = self.table.update().values(
            name=games_obj.game_name,
            architecture=games_obj.architecture,
            api=games_obj.api).\
            where(self.table.columns.id == games_obj.id)
        return self.database.execute(sql)


    def update_game_path(self, games_obj):
        sql = self.table.update().\
            values(path=games_obj.path).\
            where(self.table.columns.id == games_obj.id)
        return self.database.execute(sql)


    def update_game_architecture(self, games_obj):
        sql = self.table.update().\
            values(architecture=games_obj.architecture).\
            where(self.table.columns.id == games_obj.id)
        return self.database.execute(sql)


    def update_game_api(self, games_obj):
        sql = self.table.update().\
            values(api=games_obj.api).\
            where(self.table.columns.id == games_obj.id)
        return self.database.execute(sql)


    def delete_game(self, game_id):
        sql = self.table.delete().where(self.table.columns.id == game_id)
        return self.database.execute(sql)
