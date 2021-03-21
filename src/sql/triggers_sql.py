#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.sql.sqlite3_connection import Sqlite3


class TriggersSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def create_triggers(self):
        sql = """CREATE TRIGGER IF NOT EXISTS before_insert_configs
                BEFORE INSERT ON configs
                BEGIN
                    SELECT CASE
                        WHEN (SELECT count(*) FROM configs)IS 1 THEN
                        RAISE(ABORT, 'CANNOT INSERT INTO CONFIGS TABLE ANYMORE')
                    END;
                END;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)
