#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.databases.databases import Databases


class GamesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    ################################################################################
    def get_games(self):
        sql = "SELECT * from games ORDER BY LOWER(name) ASC;"
        databases = Databases(self.main)
        return databases.select(sql)

    ################################################################################
    def get_game_by_path(self, path: str):
        sql = f"""SELECT * from games where path = '{path}' ORDER BY LOWER(name) ASC;"""
        databases = Databases(self.main)
        return databases.select(sql)

    ################################################################################
    def get_game_by_name(self, game_name: str):
        sql = f"""SELECT * from games where name = '{game_name}' ORDER BY LOWER(name) ASC;"""
        databases = Databases(self.main)
        return databases.select(sql)

    ################################################################################
    def insert_game(self, gamesObj: object):
        sql = f"""INSERT INTO games(
            name,
            architecture,
            api,
            path
            )VALUES(
            '{gamesObj.game_name}',
            '{gamesObj.architecture}',
            '{gamesObj.api}',
            '{gamesObj.path}'
            );"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_game(self, gamesObj: object):
        sql = f"""UPDATE games SET
                name = '{gamesObj.game_name}',
                architecture = '{gamesObj.architecture}',
                api = '{gamesObj.api}'
                WHERE id = {gamesObj.id};"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_game_path(self, gamesObj: object):
        sql = f"""UPDATE games SET
                path = '{gamesObj.path}'
                WHERE id = {gamesObj.id};"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_game_architecture(self, gamesObj: object):
        sql = f"""UPDATE games SET
                architecture = '{gamesObj.architecture}'
                WHERE id = {gamesObj.id};"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_game_api(self, gamesObj: object):
        sql = f"""UPDATE games SET
                api = '{gamesObj.api}'
                WHERE id = {gamesObj.id};"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def delete_game(self, game_id: int):
        sql = f"""DELETE from games where id = {game_id};"""
        databases = Databases(self.main)
        databases.execute(sql)
