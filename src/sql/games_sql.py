#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.sql.sqlite3_connection import Sqlite3


class GamesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def get_games(self):
        sql = "SELECT * from games ORDER BY LOWER(name) ASC;"
        sqlite3 = Sqlite3(self.main)
        return sqlite3.select(sql)


    def get_game_by_path(self, path: str):
        sql = f"""SELECT * from games where path = '{path}' ORDER BY LOWER(name) ASC;"""
        sqlite3 = Sqlite3(self.main)
        return sqlite3.select(sql)


    def get_game_by_name(self, game_name: str):
        sql = f"""SELECT * from games where name = '{game_name}' ORDER BY LOWER(name) ASC;"""
        sqlite3 = Sqlite3(self.main)
        return sqlite3.select(sql)


    def insert_game(self, games_obj):
        sql = f"""INSERT INTO games(
            name,
            architecture,
            api,
            path
            )VALUES(
            '{games_obj.game_name}',
            '{games_obj.architecture}',
            '{games_obj.api}',
            '{games_obj.path}'
            );"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_game(self, games_obj):
        sql = f"""UPDATE games SET
                name = '{games_obj.game_name}',
                architecture = '{games_obj.architecture}',
                api = '{games_obj.api}'
                WHERE id = {games_obj.id};"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_game_path(self, games_obj):
        sql = f"""UPDATE games SET
                path = '{games_obj.path}'
                WHERE id = {games_obj.id};"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_game_architecture(self, games_obj):
        sql = f"""UPDATE games SET
                architecture = '{games_obj.architecture}'
                WHERE id = {games_obj.id};"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_game_api(self, games_obj):
        sql = f"""UPDATE games SET
                api = '{games_obj.api}'
                WHERE id = {games_obj.id};"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def delete_game(self, game_id: int):
        sql = f"""DELETE from games where id = {game_id};"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)
