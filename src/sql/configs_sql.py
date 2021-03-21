#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.sql.sqlite3_connection import Sqlite3


class ConfigsSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log


    def get_configs(self):
        sql = "SELECT * from configs where id = 1;"
        sqlite3 = Sqlite3(self.main)
        return sqlite3.select(sql)


    def set_default_configs(self):
        sql = """DELETE from configs;
                INSERT INTO configs(id) VALUES (1);"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_dark_theme(self, configs_obj):
        sql = f"""UPDATE configs SET
                use_dark_theme = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_shaders(self, configs_obj):
        sql = f"""UPDATE configs SET
                update_shaders = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_check_program_updates(self, configs_obj):
        sql = f"""UPDATE configs SET
                check_program_updates = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_check_resahde_updates(self, configs_obj):
        sql = f"""UPDATE configs SET
                check_reshade_updates = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_silent_reshade_updates(self, configs_obj):
        sql = f"""UPDATE configs SET
                silent_reshade_updates = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_create_screenshots_folder(self, configs_obj):
        sql = f"""UPDATE configs SET
                create_screenshots_folder = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_reshade_version(self, configs_obj):
        sql = f"""UPDATE configs SET
                reshade_version = '{configs_obj.reshade_version}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_reset_reshade_files(self, configs_obj):
        sql = f"""UPDATE configs SET
                reset_reshade_files = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_custom_config(self, configs_obj):
        sql = f"""UPDATE configs SET
                use_custom_config = '{configs_obj.status}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)


    def update_program_version(self, configs_obj):
        sql = f"""UPDATE configs SET
                program_version = '{configs_obj.program_version}'
                WHERE id = 1;"""
        sqlite3 = Sqlite3(self.main)
        sqlite3.executescript(sql)
