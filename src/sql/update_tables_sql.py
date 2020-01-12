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
    def update_tables(self):
        databases = Databases(self.main)
        configs_table_columns = ["id",
                            "use_dark_theme",
                            "update_shaders",
                            "check_program_updates",
                            "check_reshade_updates",
                            "silent_reshade_updates",
                            "reset_reshade_files",
                            "create_screenshots_folder",
                            "program_version",
                            "reshade_version"]

        games_table_columns = ["id",
                            "name",
                            "architecture",
                            "api",
                            "path"]

        configs_table_vars = str(configs_table_columns)[1:-1]
        games_table_vars = str(games_table_columns)[1:-1]

        sql = """DROP TRIGGER if exists "before_insert_configs";
                DROP TABLE if exists "configs_old";
                DROP TABLE if exists "games_old";
                ALTER TABLE "configs" RENAME TO "configs_old";
                ALTER TABLE "games" RENAME TO "games_old";"""
        databases.execute(sql)

        initialTablesSql = InitialTablesSql(self.main)
        it = initialTablesSql.create_initial_tables()
        if it is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)

        sql = f"""INSERT INTO "configs" ({configs_table_vars}) 
                SELECT {configs_table_vars} FROM "configs_old";
            
                INSERT INTO "games" ({games_table_vars})
                    SELECT {games_table_vars} FROM "games_old";
                
                DROP TABLE if exists "configs_old";
                DROP TABLE if exists "games_old";
            """
        databases.execute(sql)

        triggersSql = TriggersSql(self.main)
        tr = triggersSql.create_triggers()
        if tr is not None:
            err_msg = messages.error_create_sql_config_msg
            self.log.error(err_msg)
            print(err_msg)
