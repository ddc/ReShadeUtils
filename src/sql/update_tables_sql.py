#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.utils import messages
from src.databases.databases import Databases
from src.sql.initial_tables_sql import InitialTablesSql
from src.sql.triggers_sql import TriggersSql


class UpdateTablesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    ################################################################################
    def update_config_table(self):
        databases = Databases(self.main)
        sql = """DROP TRIGGER if exists before_insert_configs;
                DROP TABLE if exists configs_old;
                ALTER TABLE configs RENAME TO configs_old;"""
        databases.execute(sql)

        initialTablesSql = InitialTablesSql(self.main)
        it = initialTablesSql.create_initial_tables()
        if it is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)
            return

        sql = "SELECT * from configs_old"
        rs_configs_old = databases.select(sql)

        sql = "INSERT INTO configs (id) VALUES (1);"
        databases.execute(sql)

        sql = "SELECT * from configs"
        rs_configs = databases.select(sql)

        sql = ""
        for col in rs_configs_old[0].keys():
            if col != "id".lower():
                if col in rs_configs[0].keys():
                    sql += f"UPDATE configs SET {col} = '{rs_configs_old[0].get(col)}' WHERE id = 1;"
        sql += "DROP TABLE if exists configs_old;"
        databases.execute(sql)

        triggersSql = TriggersSql(self.main)
        tr = triggersSql.create_triggers()
        if tr is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)
