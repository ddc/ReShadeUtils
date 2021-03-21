#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.utils import messages
from src.sql.sqlite3_connection import Sqlite3
from src.sql.initial_tables_sql import InitialTablesSql
from src.sql.triggers_sql import TriggersSql


class UpdateTablesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def update_config_table(self):
        sqlite3 = Sqlite3(self.main)
        sql = """DROP TRIGGER if exists before_insert_configs;
                DROP TABLE if exists configs_old;
                ALTER TABLE configs RENAME TO configs_old;"""
        sqlite3.executescript(sql)

        initial_tables_sql = InitialTablesSql(self.main)
        it = initial_tables_sql.create_initial_tables()
        if it is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            return

        sql = "SELECT * from configs_old"
        rs_configs_old = sqlite3.select(sql)

        sql = "INSERT INTO configs (id) VALUES (1);"
        sqlite3.executescript(sql)

        sql = "SELECT * from configs"
        rs_configs = sqlite3.select(sql)

        sql = ""
        for col in rs_configs_old[0].keys():
            if col != "id".lower():
                if col in rs_configs[0].keys():
                    sql += f"UPDATE configs SET {col} = '{rs_configs_old[0].get(col)}' WHERE id = 1;"
        sql += "DROP TABLE if exists configs_old;"
        sqlite3.executescript(sql)

        triggers_sql = TriggersSql(self.main)
        tr = triggers_sql.create_triggers()
        if tr is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
